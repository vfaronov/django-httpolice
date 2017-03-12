# pylint: disable=redefined-outer-name

from django.test import Client, override_settings
import pytest

import django_httpolice


def notice_ids(obj):
    return [notice.id for notice in obj.notices]


@pytest.fixture
def client(request):                # pylint: disable=unused-argument
    django_httpolice.backlog.clear()
    return Client()


def test_backlog(client):
    client.get('/api/v1/words/?query=er', HTTP_ACCEPT='application/json')
    client.get('/api/v1/words/?query=er', HTTP_ACCEPT='text/plain')
    [exch1, exch2] = django_httpolice.backlog

    assert not notice_ids(exch1)
    assert notice_ids(exch1.request) == []
    assert len(exch1.responses) == 1
    assert not notice_ids(exch1.responses[0])

    assert not notice_ids(exch2)
    assert notice_ids(exch2.request) == []
    assert len(exch2.responses) == 1
    assert notice_ids(exch2.responses[0]) == [1038]     # "Bad JSON body"

    resp = client.get('/httpolice/')
    assert b'Bad JSON body' in resp.content


# Because attributes such as `httpolice.Request.target`
# are currently *not* part of the HTTPolice public API,
# we avoid inspecting them directly;
# instead, we try to trigger particular notices related to them.

def test_request_uri(client):
    client.get('/api/v1/words/?query=[whatever]')
    [exch1] = django_httpolice.backlog
    assert notice_ids(exch1.request) == [1045]          # "Bad request target"


def test_request_method(client):
    client.delete('/api/v1/words/', data=b'fqwfqwf', content_type='text/plain')
    [exch1] = django_httpolice.backlog
    assert notice_ids(exch1.request) == [1059]   # "DELETE request with a body"


def test_request_headers(client):
    client.get('/api/v1/words/', HTTP_LOCATION='http://example.com/')
    [exch1] = django_httpolice.backlog
    # "Request with a Location header"
    assert notice_ids(exch1.request) == [1063]


def test_response_to_head(client):
    client.head('/api/v1/words/')
    [exch1] = django_httpolice.backlog
    assert not notice_ids(exch1.responses[0])


def test_read_request_data(client):
    client.post('/api/v1/words/',
                data=b'foo bar baz', content_type='text/plain')


def test_streaming_response(client):
    client.get('/api/v1/words/')
    [exch1] = django_httpolice.backlog
    # No notice 1038 because we don't read the response body.
    assert not notice_ids(exch1.responses[0])


def test_silence_globally(client):
    with override_settings(HTTPOLICE_SILENCE=[]):
        client.get('/api/v1/words/?query=er', HTTP_ACCEPT='application/json')
        [exch1] = django_httpolice.backlog
        assert notice_ids(exch1.request) == [1070]  # "No User-Agent header"
        # "200 response with no Date header"
        assert notice_ids(exch1.responses[0]) == [1110]


def test_silence_locally(client):
    with override_settings(HTTPOLICE_SILENCE=[]):
        client.get('/api/v1/words/?query=er', HTTP_ACCEPT='application/json',
                   HTTP_HTTPOLICE_SILENCE='1070, 1110 resp')
        [exch1] = django_httpolice.backlog
        assert not notice_ids(exch1.request)
        assert not notice_ids(exch1.responses[0])


def test_disabled(client):
    with override_settings(HTTPOLICE_ENABLE=False):
        client.get('/api/v1/words/')
        assert not django_httpolice.backlog
        resp = client.get('/httpolice/')
        assert resp.status_code == 404


def test_raise(client):
    with override_settings(HTTPOLICE_RAISE='error'):
        with pytest.raises(django_httpolice.ProtocolError):
            client.get('/api/v1/words/?query=er')
        assert len(django_httpolice.backlog) == 1


def test_raise_comment(client):
    # Disable silencing notice 1110 ("<status> response with no Date header").
    with override_settings(HTTPOLICE_SILENCE=[]):
        with override_settings(HTTPOLICE_RAISE='error'):
            client.get('/api/v1/words/')        # 1110 is only a comment
        with override_settings(HTTPOLICE_RAISE='comment'):
            with pytest.raises(django_httpolice.ProtocolError):
                client.get('/api/v1/words/')


def test_no_raise_when_silenced(client):
    with override_settings(HTTPOLICE_RAISE='error'):
        client.get('/api/v1/words/?query=er',
                   HTTP_HTTPOLICE_SILENCE='1038 resp')
