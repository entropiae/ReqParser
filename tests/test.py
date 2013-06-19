import sys
import unittest
import urlparse

import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reqparser import reqparser

# Transform lambdas
in_range = lambda x: 0 < x < 5
lower = lambda x: x.lower()
comma_split = lambda x: x.split(',')
state_filter = lambda x: set(x).intersection(['italy', 'france', 'uk'])
str_to_bool = lambda x: x.lower() in ['1', 'true']

# Check lambdas
in_type_lst = lambda x: x in ['bdg', 'vis', 'dur']
month_check = lambda x: 0 < x <= 12
perc_check = lambda x: 0 <= x <= 100

ignore_months = lambda args: 'type' in args and args['type'] == 'dur'


class ParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def log(self):
        print 'Performing {0}()'.format(self.id().split('.')[-1])

    @staticmethod
    def get_dict(request):
        return dict(urlparse.parse_qsl(request))

    def test_unlisted_fields(self):
        # Original field not listed in a add_field directive have to be copied with no mod
        self.log()

        r = reqparser.ReqParser()
        r.add_field('contract', transform_ops=[lower], required=True, default='standard')
        r.add_field('default_bool', transform_ops=str_to_bool, required=False, default=False)
        r.add_field('start_month', transform_ops=int, check_ops=month_check, ignore_if=ignore_months)
        r.add_field('default_int', transform_ops=int, required=True, default=3)
        r.add_field('percentage', transform_ops=int, check_ops=perc_check)

        request = ParserTest.get_dict('contract=standard&unlisted=text&start_month=13&percentage=1&other_field=1')
        parsed_request = r.from_dict(request)

        self.assertIn('unlisted', parsed_request)
        self.assertEqual(parsed_request['unlisted'], 'text')

        self.assertIn('other_field', parsed_request)
        self.assertEqual(parsed_request['other_field'], '1')

    def test_default_value(self):
        self.log()

        r = reqparser.ReqParser()
        r.add_field('cat', transform_ops=[int], check_ops=[in_range])
        r.add_field('default_bool', transform_ops=str_to_bool, required=False, default=False)
        r.add_field('start_month', transform_ops=int, check_ops=month_check, ignore_if=ignore_months)
        r.add_field('default_int', transform_ops=int, required=True, default=3)
        r.add_field('percentage', transform_ops=int, check_ops=perc_check)
        r.add_field('default_string', transform_ops=int, required=True, default='default!')

        request = ParserTest.get_dict('cat=3&start_month=13&percentage=1')
        parsed_request = r.from_dict(request)

        self.assertIn('default_bool', parsed_request)
        self.assertEqual(parsed_request['default_bool'], False)

        self.assertIn('default_int', parsed_request)
        self.assertEqual(parsed_request['default_int'], 3)

        self.assertIn('default_string', parsed_request)
        self.assertEqual(parsed_request['default_string'], 'default!')

    def test_priority(self):
        pass

    def test_attribute_methods(self):
        self.log()

        r = reqparser.ReqParser()
        r.add_field('contract', transform_ops=['lower'], required=True, default='standard')
        r.add_field('cat', transform_ops='upper')
        r.add_field('percentage', transform_ops=int, check_ops=perc_check)

        request = ParserTest.get_dict('cat=lower&contract=UPPER&percentage=1')
        parsed_request = r.from_dict(request)

        self.assertIn('contract', parsed_request)
        self.assertEqual(parsed_request['contract'], 'upper')

        self.assertIn('cat', parsed_request)
        self.assertEqual(parsed_request['cat'], 'LOWER')

        self.assertIn('percentage', parsed_request)
        self.assertEqual(parsed_request['percentage'], 1)

    def test_method_list(self):
        pass


if __name__ == '__main__':
    unittest.main()
