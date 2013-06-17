import sys
import unittest
import urlparse

import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reqparser import reqparser

in_range = lambda x: 0 < x < 5
in_type_lst = lambda x: x in ['bdg', 'vis', 'dur']
month_check = lambda x: 0 < x <= 12
perc_check = lambda x: 0 <= x <= 100
lower = lambda x: x.lower()
comma_split = lambda x: x.split(',')

state_filter = lambda x: x


ignore_months = lambda args: 'type' in args and args['type'] == 'dur'


class ParserTest(unittest.TestCase):

    def setUp(self):
        r = reqparser.ReqParser()
        r.add_field('cat', transform_ops=[int], check_ops=[in_range])
        r.add_field('type', transform_ops='lower', check_ops=in_type_lst, priority=40)
        r.add_field('start_month', transform_ops=int, check_ops=month_check, ignore_if=ignore_months)
        r.add_field('end_month', transform_ops=int, check_ops=month_check)
        r.add_field('percentage', transform_ops=int, check_ops=perc_check)
        #r.add_field('state', transform_ops=[lower, comma_split, state_filter], check_ops=list_len)
        #r.add_field('debug', transform_ops=str_to_bool, required=False, default=False)
        #r.add_field('detail', transform_ops=str_to_bool, required=True, default=True)
        #r.add_field('contract', transform_ops=[lower], required=True, default='standard')
        self.r = r

    @staticmethod
    def get_dict(request):
        return dict(urlparse.parse_qsl(request))

    def test_unlisted_fields(self):
        request = ParserTest.get_dict('cat=3&type=BDG&start_month=10&end_month=11&fields=copy&percentage=50&state=italy,france,germany&debug=true&detail=1&contract=standard')
        parsed_req = self.r.from_dict(request)
        self.assertIn('fields', parsed_req)
        self.assertEqual(parsed_req['fields'], 'copy')
        print self.r.errors

if __name__ == '__main__':
    unittest.main()
