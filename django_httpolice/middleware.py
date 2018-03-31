# -*- coding: utf-8; -*-

import collections

import django.utils.encoding

from django_httpolice.common import ProtocolError, get_setting


backlog = collections.deque(maxlen=get_setting('BACKLOG'))


class HTTPoliceMiddleware(object):

    """Captures and checks HTTP exchanges, saving them for later review."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not get_setting('ENABLE'):
            return response

        # Importing `httpolice` can execute a lot of code,
        # so we only do it when it's really time for action.
        import httpolice

        req_method = _force_text(request.method)
        req_headers = httpolice.helpers.headers_from_cgi(request.META)
        req_target = _force_text(request.path)
        if request.META.get('QUERY_STRING'):
            req_target += u'?' + _force_text(request.META['QUERY_STRING'])

        try:
            # This can raise `django.http.request.RawPostDataException`, saying
            # "You cannot access body after reading from request's data stream"
            req_body = request.body
        except Exception:
            # ...but `RawPostDataException` is not documented in Django API,
            # so catch everything.
            req_body = None

        # A ``Content-Type`` of ``text/plain`` is automatically added
        # to requests that have none (such as GET requests).
        if req_body == b'' and req_method in [u'GET', u'HEAD', u'DELETE']:
            req_headers = [entry for entry in req_headers
                           if entry != (u'Content-Type', b'text/plain')]

        req = httpolice.Request(
            scheme=_force_text(request.scheme),
            method=req_method,
            target=req_target,
            version=None,
            header_entries=req_headers,
            body=req_body,
        )

        if req_method == u'HEAD':
            # Body is automatically stripped from responses to HEAD,
            # but not at this point in the response lifecycle.
            resp_body = b''
        elif response.streaming:
            resp_body = None        # Unknown.
        else:
            resp_body = response.content

        resp = httpolice.Response(
            version=None,
            status=response.status_code,
            reason=_force_text(response.reason_phrase),
            header_entries=[
                (_force_text(name), value)
                for (name, value) in response.items()],
            body=resp_body,
        )

        exchange = httpolice.Exchange(req, [resp])
        exchange.silence(get_setting('SILENCE'))
        httpolice.check_exchange(exchange)
        backlog.append(exchange)

        raise_on = get_setting('RAISE')
        if raise_on:
            min_severity = httpolice.Severity[raise_on]
            if any(notice.severity >= min_severity for notice in resp.notices):
                raise ProtocolError(exchange)

        return response


def _force_text(s):
    return django.utils.encoding.force_text(s, encoding='iso-8859-1')
