from collections import Counter
import logging
trace = logging.getLogger('trace')

class Mapper():

    def __init__(self, struct):
        self.struct = struct
        # trace.info('STRUCT CREATED: {}\n'.format(self.struct))

    def map_to_struct(self, data, parent_key='current_report', loc=None):
        """
        >>> m = Mapper({'subscriptions': {'current_report': {0: {'start': '', 'end': '', 'name': '', 'new': 0, 'average': 0, 'total': 0}, 1: {'start': '', 'end': '', 'name': '', 'new': 0, 'average': 0, 'total': 0}, 'attributes': {'group': 'all', 'end_date': '2010-03-29', 'package': 'all', 'interval': 'daily', 'client': '32432325252', 'platform': 'all', 'state': 'active', 'api': 'subscriptions', 'territory': 'all', 'start_date': '2010-03-15'}}}})
        >>> data = Counter({'total': 25, 'new': 5, 'average': 4, 'churn': 0, 'churn_pct': 0, 'name': 'test', 'start': '2014-01-01', 'end': '2014-01-10'})
        >>> m.map_to_struct(data, parent_key='current_report', loc=0)
        >>> data = Counter({'total': 55, 'new': 45, 'average': 77, 'churn': 0, 'churn_pct': 0, 'name': 'test', 'start': '2014-01-10', 'end': '2014-01-11'})
        >>> m.map_to_struct(data, parent_key='current_report', loc=1)
        >>>
        """
        loc = str(loc)
        # trace.info('\n\n------parent-key: {} loc: {}'.format(parent_key, loc))

        keys = self.find_keys(parent_key, self.struct)
        if not keys:
            print 'parent not found'

        parent = self.struct
        #try:
        for k in range(0, len(keys)-1, 1):
            parent = parent.get(keys[k], None)
        #except Exception:
        #    raise

        # trace.info('STRUCT: {} type: {}'.format(self.struct, type(self.struct)))
        # trace.info('DATA TO MAP: {} type: {} loc: {}\n'.format(data, type(data), loc))
        # trace.info('PARENT STRUCT: {}\n'.format(parent))

        group = False
        for k, v in data.iteritems():
            if isinstance(v, dict):
                group = True
                break
        if group:
            for k, v in data.iteritems():

                # k gets updated for all intervals - following is the soln.
                c = dict()
                c.update(parent[parent_key].get(str(loc), None))
                # trace.info('LOC: {} struct: {}----- \n{}={}'.format(loc, c, k, v))
                c[k] = v
                parent[parent_key][str(loc)] = c




                # print k, v
                # if isinstance(v, dict):
                #     # print k, v
                #     # dc = Counter(v)
                #
                #     # trace.info('---{} loc: {}, k: {},  dc: {} struct: {}'.format(data['start'], loc, k, dc, parent[parent_key][loc][k])) if loc == '1' and k == 'windows' else ''
                #
                #     # sc = Counter(parent[parent_key][str(loc)][k])
                #     #
                #     # trace.info('---sc: {}'.format(sc))
                #     #
                #     # sc.update(dc)
                #     # print sc, type(sc)
                #     # parent[parent_key][str(loc)][k] = dict(sc)
                #     # print 'RES: ', parent[parent_key][loc][k], type(parent[parent_key][loc][k]), '\n'
                #
                #
                #
                #     c = dict()
                #     c.update(parent[parent_key].get(str(loc), None))
                #     trace.info('LOC: {} struct: {}----- \n{}={}'.format(loc, c, k, v))
                #     c[k] = v
                #     parent[parent_key][str(loc)] = c
                #
                # else:
                #     try:

                #         c = dict()
                #         c.update(parent[parent_key].get(str(loc), None))
                #         c[k] = v  # if c[k] == '' else '??'
                #         parent[parent_key][str(loc)] = c
                #     except Exception:
                #         trace.exception('\n\n')
        else:
            struct = Counter(parent[parent_key][str(loc)])
            parent[parent_key][str(loc)] = dict(struct + data)
        # print 'RES STRUCT: ', self.struct, type(self.struct)




    def get_struct(self):
        return self.struct

    def find_keys(self, key, d):
        for k, v in d.items():
            if k == key:
                return [k]
            if isinstance(v, dict):
                p = self.find_keys(key, v)
                if p:
                    return [k] + p
            elif k == key:
                return [k]
