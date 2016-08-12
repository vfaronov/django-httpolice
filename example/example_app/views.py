# -*- coding: utf-8; -*-

import json

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, StreamingHttpResponse


all_words = [u'absentee', u'babying', u'bankrupt', u'cottonwood',
             u'disqualified', u'furled', u'gullies', u'indomitably',
             u'intermediary', u'Johann', u'legations', u'monopoly',
             u'ordaining', u'otherwise', u'poignant', u'shatters',
             u'tactically', u'Tao', u'torquing', u'wean']


@require_http_methods(['GET', 'HEAD', 'POST'])
def words(request):
    if request.method == 'POST':
        return add_words(request)
    elif request.GET.get('query'):
        return search_words(request)
    else:
        return stream_words()


def add_words(request):
    n = 0
    for word in request.read().decode().split():
        if word not in all_words:
            all_words.append(word)
            n += 1
    return HttpResponse(u'Added %d words\n' % n, content_type='text/plain')


def search_words(request):
    query = request.GET['query']
    matches = [word for word in all_words if query in word]
    if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
        content = json.dumps({'matches': matches})
    else:
        content = u''.join(word + u'\n' for word in matches).encode()
    return HttpResponse(content,
                        content_type='application/json')        # oops!


def stream_words():
    return StreamingHttpResponse(
        (word.encode() + b'\n' for word in all_words),
        content_type='application/json')
