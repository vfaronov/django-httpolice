# -*- coding: utf-8; -*-

import json

from django.http import HttpResponse, StreamingHttpResponse


def greet(request):
    name = request.GET.get('name')
    format_ = request.GET.get('format', 'json')
    if format_ == 'json':
        content = json.dumps({'hello': name})
        content_type = 'application/json'
    elif format_ == 'plain':
        content = 'Hello %s!\n' % name
        content_type = 'application/json'       # oops!
    return HttpResponse(content, content_type=content_type)


def stream_greeting(request):
    n = int(request.GET.get('n', 1))
    if request.method == 'POST':
        greeting = request.read()
    else:
        greeting = b'<hello>Hi there!</hello>'
    return StreamingHttpResponse([greeting] * n, content_type='text/xml')
