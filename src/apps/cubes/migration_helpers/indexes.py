BTREE = 'BTREE'
HASH = 'HASH'


class BuildIndexes(object):
    INDEX = ''

    def __init__(self, db_name=''):
        self.INDEX = ''
        self.db_name = db_name

    def create_index(self, field_name, index_type=BTREE):
        self.INDEX += "CREATE INDEX {db_name}_{field_name} USING {index_type} ON `{db_name}` (`{field_name}`); ".format(
            db_name=self.db_name,
            field_name=field_name,
            index_type=index_type
        )

    def __str__(self):
        return str(self.INDEX)
