# Методы морфологического анализа
import strutil


# ----------------------------------------------------------------------------------------------------------------------
# Построение таблицы N-грамм
# Схема:
# * берем словоформы из таблицы wfs
# * составляем массив N-грамм
# * заносим в таблицу ngramms
def create_ngramms_table(db):
    cngr = db.cursor()
    cngr.execute('DROP TABLE IF EXISTS ngramms')
    cngr.execute(
        '''CREATE TABLE IF NOT EXISTS ngramms
         (
               id       INTEGER PRIMARY KEY
             , ngr      TEXT
             , wf_id    INTEGER
         )
        '''
    )
    cngr.execute('CREATE INDEX idx_ngramms_001 ON ngramms (ngr)')

    cwf = db.cursor()

    def wfs():
        yield from cwf.execute('SELECT id, wf FROM wfs')

    def ngramms():
        for wf_id, wf in wfs():
            for ngr in strutil.str_build_n_gramms(wf):
                yield ngr, wf_id

    cngr.executemany('INSERT INTO ngramms VALUES (NULL,?,?)', ngramms())

    db.commit()


# ----------------------------------------------------------------------------------------------------------------------
# функция определяет предполагаемые основы слов (общие части) и (прото)аффиксы -- то,
# что осталось после удаления предполагаемых основ
# \return   -- кортеж ([preffixes], 'base', [suffixes])
def extract_proto_morphemes(s1, s2):
    from strutil import str_convolution_max, str_split_by_equal

    sh, conv = str_convolution_max(s1, s2)      # Определяем смещение наилучшего совмещения строк
    ss1, ss2 = str_split_by_equal(s1, s2, sh)   # Разбиваем строки на интервалыодинаковых и разных подстрок

    assert len(ss1) == len(ss2), "Unexpected str_split_by_equal(...) result"
    if len(ss1) <= 0:
        return [], '', []

    # def map_func(sub1, sub2):
    #     return (len(sub1[1]), sub1[0]) if sub1[1] == sub2[1] else (0, 0)

    # ищем индекс самого длинного совпадающего куска
    # после выполнения proto_root_pos будет содержать индекс основы
    proto_root_pos, stub = max(
        map(
            lambda sub1, sub2:
                (sub1[0], len(sub1[1])) if sub1[1] == sub2[1] else (0, 0),
            enumerate(ss1), enumerate(ss2)
        ),
        key=lambda x:
            x[1])

    proto_prefixes = \
        [
              ''.join(ss1[:proto_root_pos])
            , ''.join(ss2[:proto_root_pos])
        ]
    proto_suffixes = \
        [
              ''.join(ss1[proto_root_pos + 1:])
            , ''.join(ss2[proto_root_pos + 1:])
        ]
    proto_prefixes = [o for o in proto_prefixes if o != '']
    proto_suffixes = [o for o in proto_suffixes if o != '']

    return \
        (
            # прото-префиксы
            proto_prefixes,
            # прото-основа
            ss1[proto_root_pos],
            # прото-суффиксы
            proto_suffixes
        )

