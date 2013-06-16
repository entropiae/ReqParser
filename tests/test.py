import sys
import unittest

import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reqparser import reqparser

class ParserTest(unittest.TestCase):

    def setUp(self):
        self.r = reqparser.ReqParser()

    def tearDown(self):
        pass

    def test_unlisted_fields(self):
        upper = dict((x, x.upper()) for x in ('reqparser', 'test', 'class'))
        args = self.r.from_dict(upper)
        self.assertIn('reqparser', args)
        self.assertIn('test', args)
        self.assertIn('class', args)

if __name__ == '__main__':
    unittest.main()




#def add_fields(self, name, transform_ops=[], check_ops=[], required=True, default=None, ignore_if=None, priority=50):