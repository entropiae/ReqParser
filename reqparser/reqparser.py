 # -*- coding: utf-8 -*-
from collections import namedtuple


class ReqParser(object):
    field = namedtuple('Field', ['name', 'transform_ops', 'check_ops', 'required', 'default', 'ignore_if', 'priority'])
    check = namedtuple('Check', ['name', 'op'])

    def __init__(self):
        self.reset()

    def reset(self):
        self.fields = []
        self.checks = []
        self.errors = []

    def add_field(self, name, transform_ops=[], check_ops=[], required=True, default=None, ignore_if=None, priority=50):
        self.fields.append(ReqParser.field(name, transform_ops, check_ops, required, default, ignore_if, priority))

    def add_check(self, name, op):
        self.checks.append(ReqParser.check(name, op))

    def log_error(self, field, msg):
        self.errors.append((field, msg))

    def from_dict(self, args, named=False):
        # Field in source dict and not in field_list will be copied in final dict
        fields_name = [field.name for field in self.fields]
        parsed_req = dict((k, v) for k, v in args.iteritems() if k not in fields_name)

        for field in sorted(self.fields, key=lambda field: field.priority):
            if field.name in args and args[field.name]:
                # TODO
                # Introdurre la possibilita di passare una singola callback invece di una lista:
                # http://stackoverflow.com/questions/624926/how-to-detect-whether-a-python-variable-is-a-function
                # Introdurre la possibilità di chiamare funzioni membro (es, str.lower()). Usare hasattr/getattr
                try:
                    parsed_req[field.name] = reduce(lambda x, y: y(x), field.transform_ops, args[field.name])
                except Exception as e:
                    self.log_error(field.name, '{0} - {1}'.format(e.__class__.__name__, e.message))
                    break
            else:
                if field.default is not None:
                    parsed_req[field.name] = field.default
                elif field.ignore_if is not None and field.ignore_if(args):
                    pass
                elif field.required:
                    self.log_error(field.name, 'Required field not found or empty')

            if not all(op(args[field.name]) for op in field.ops):
                self.log_error(field.name, 'Check on field failed')

        for check in self.checks:
            if not check.op(parsed_req):
                self.log_error((check.name, 'Check failed'))

        if named:
            tpl = namedtuple('Request', parsed_req.keys())
            parsed_req = tpl(**parsed_req)

        return parsed_req
