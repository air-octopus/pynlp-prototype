# Процедуры подготовки данных (чтение файлов, представление в виде массива слов...)

import strutil

# ----------------------------------------------------------------------------------------------------------------------
# Загрузка файла и представление его в виде массива слов.
# Все символы не относящиеся к словам (знаки препинания, цифры,...) удаляются.
# Все слова переводятся в нижний регистр
def load_file(file_name):
    s = open(file_name).read()

    s = s.replace('\n', ' ')
    s = s.replace('.', ' ')
    s = s.replace(',', ' ')
    s = s.replace(':', ' ')
    s = s.replace(';', ' ')
    s = s.replace('?', ' ')
    s = s.replace('!', ' ')
    s = s.replace('-', ' ')
    s = s.replace('"', ' ')
    s = s.replace('(', ' ')
    s = s.replace(')', ' ')
    s = s.replace('0', ' ')
    s = s.replace('1', ' ')
    s = s.replace('2', ' ')
    s = s.replace('3', ' ')
    s = s.replace('4', ' ')
    s = s.replace('5', ' ')
    s = s.replace('6', ' ')
    s = s.replace('7', ' ')
    s = s.replace('8', ' ')
    s = s.replace('9', ' ')
    s = s.replace('I', ' ')
    s = s.replace('V', ' ')
    s = s.replace('X', ' ')
    s = s.replace('L', ' ')
    s = s.replace('C', ' ')
    s = s.replace('M', ' ')
#    s = s.replace('  ', ' ')
#    s = s.replace('  ', ' ')
#    s = s.replace('  ', ' ')
#    s = s.replace('  ', ' ')
    s = s.lower()

    dat = [ sub for sub in s.split(' ') if sub != '']
    return dat


# ----------------------------------------------------------------------------------------------------------------------
# Сохранение массива слов в базу данных
def store_wordforms_to_db(db, text_words):
    wfs = dict()
    for wf in text_words:
        strutil.str_store_to_dict(wfs, wf)

    c = db.cursor()
    c.execute('DROP TABLE IF EXISTS wfs')
    c.execute(
        '''CREATE TABLE IF NOT EXISTS wfs
         (
               id       INTEGER PRIMARY KEY
             , wf       TEXT
             , usage    INTEGER
         )
        ''')
    c.execute('CREATE INDEX idx_wfs_001 ON wfs (wf)')
    c.execute('CREATE INDEX idx_wfs_002 ON wfs (LENGTH(wf))')
    c.executemany('INSERT INTO wfs VALUES (NULL,?,?)', (wf for wf in wfs.items()))

    db.commit()



