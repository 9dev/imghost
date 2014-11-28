from django.test import TestCase

from utils import *

class OEmbedTests(TestCase):

    def test_del_none(self):
        
        input = {
            'something': 'something',
            'sth_else': None,
            'lorem_ipsum': None,
        }
        
        output = {
            'something': 'something',
        }
        
        result = del_none(input)
        self.assertEqual(result, output)

    def test_get_size(self):
        
        sizes = [
            [100, 100],
            [200, 200],
            [300, 300],
        ]
        
        maxw = 150
        maxh = 300
        
        output = [100, 100]
        
        result = get_size(sizes, maxw, maxh)

        self.assertEqual(result, output)
