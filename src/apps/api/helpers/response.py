import json
import logging
trace = logging.getLogger('trace')


class ResponseGenerator():

    def __init__(self, api_name, path, attribute_keys, sub_struct=None, struct_count=0):
        self.resp = dict()
        self.struct = dict()
        self.struct[api_name] = {}
        self.struct[api_name]['current_report'] = ''
        self.struct[api_name]['current_report'] = {str(k): sub_struct for k in range(0, struct_count) if sub_struct}
        self.api_name = api_name
        self.path = path
        attrib_vals = path.split('/')[3:-1]
        # trace.info('attrib: {}'.format(attribute_keys))
        # trace.info('attrib: {}'.format(attrib_vals))
        self.attributes = {k: v for k, v in zip(attribute_keys, attrib_vals)}

    def add_el(self, sub_struct, parent_key):
        """
        >>> r = ResponseGenerator('testAPI', '32432325252/subscriptions/all/active/all/daily/all/all/2010-03-15/2010-03-29/', ['client', 'api', 'package', 'state', 'group', 'interval', 'territory', 'platform', 'start_date', 'end_date'])
        >>> r.struct
        >>> r.add_el({'test': 'one'}, 'current_report')
        >>> r.add_el({'two': '2'}, 'current_report')
        >>> r.add_el({'three': '3'}, 'current_report')
        >>> r.set_report_template()
        >>> r.get_dict_response()
        >>> 1
        """
        keys = find_key(parent_key, self.struct)
        if not keys:
            print 'parent not found'
        parent = self.struct
        try:
            for k in range(0, len(keys)-1, 1):
                parent = parent.get(keys[k], None)
        except Exception as e:
            print e.args

        i = len(parent[parent_key])
        if not i:
            parent[parent_key] = {i: sub_struct}
        else:
            parent[parent_key].update({i: sub_struct})
        # print ' STRUCT: {}'.format(self.struct)

    def set_report_template(self):
        self.struct[self.api_name]['current_report']['attributes'] = self.attributes

    def get_dict_response(self):
        return self.struct

    def get_json_response(self):
        return json.dumps(self.resp)


def find_key(key, d):
    for k, v in d.items():
        if k == key:
            return [k]
        if isinstance(v, dict):
            p = find_key(key, v)
            if p:
                return [k] + p
        elif k == key:
            return [k]
