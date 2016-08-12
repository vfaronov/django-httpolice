import json
import unittest

from django.core.urlresolvers import reverse
from django.test import Client

import example_app.views


class ExampleTestCase(unittest.TestCase):

    def test_query_json(self):
        response = Client().get(reverse(example_app.views.words),
                                {'query': u'er'},
                                HTTP_ACCEPT='application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['matches'],
                         ['intermediary', 'otherwise', 'shatters'])

    def test_query_plain(self):
        response = Client().get(reverse(example_app.views.words),
                                {'query': u'er'})
        self.assertEqual(response.content,
                         b'intermediary\notherwise\nshatters\n')

    def test_add_word(self):
        Client().post(reverse(example_app.views.words),
                      data='foo bar baz', content_type='text/plain')
        self.assertTrue(u'bar' in example_app.views.all_words)

    def test_all_words(self):
        response = Client().get(reverse(example_app.views.words))
        self.assertTrue(response.streaming)     # pylint: disable=no-member
