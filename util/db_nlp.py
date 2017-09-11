import util.db_common as cmn


# ----------------------------------------------------------------------------------------------------------------------
# класс для работы с таблицей словоформ
class db_wordforms:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()
        self.columns = [
            ('id'  , 'INTEGER PRIMARY KEY')
          , ('wf'  , 'TEXT')
          , ('freq', 'INTEGER')
        ]

    # Создать чиятую таблицу словоформ
    def clean(self):
        cmn.create_clean_table(self.cursor, self.columns)
        self.cursor.execute('CREATE INDEX idx_wfs_001 ON wfs (wf)')
        self.cursor.execute('CREATE INDEX idx_wfs_002 ON wfs (LENGTH(wf))')

    # Добавить словоформы в таблицу
    def add_wordforms(self, wfs):
        # not implemented
        pass

    # Получть словоформы
    def wordforms(self, order = '', count = 0, cursor = None):
        sql = 'SELECT id, wf, freq FROM wfs'
        if order != '':
            sql += ' ORDER BY ' + order
        if count > 0:
            sql += ' LIMIT' + count

        if cursor is None:
            cursor = self.cursor

        yield from cursor.execute(sql)

