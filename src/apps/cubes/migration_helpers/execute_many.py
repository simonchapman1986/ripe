

def execute_many(db_cls, sql):
    _s = sql.split(';')
    for s in _s:
        print s
        if len(s)>1:
            db_cls.execute('{sql};'.format(sql=s))
