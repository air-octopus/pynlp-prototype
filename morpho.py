# Методы морфологического анализа

#import Levenshtein
#import pyxdameraulevenshtein

from util import strutil
from util import listutil


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
# Найти словоформы по n-грамме
# DB requirements:
#       существуют и проинициализированы таблицы wfs и ngramms
# DB results:
#       NONE
def get_wordform_by_nramm(db, ngr):
    cursor_ngr = db.cursor()
    query = 'SELECT DISTINCT wfs.id, wfs.wf FROM wfs, ngramms WHERE wfs.id=ngramms.wf_id AND ngramms.ngr=:ngr'
    # for o in cursor_ngr.execute(query, {'ngr': ngr}):
    yield from cursor_ngr.execute(query, {'ngr': ngr})


# ----------------------------------------------------------------------------------------------------------------------
# функция определяет предполагаемые основы слов (общие части) и (прото)аффиксы -- то,
# что осталось после удаления предполагаемых основ
# \return   -- кортеж ([preffixes], 'base', [suffixes])
# (
#   (prefix1, base, suffix1)
#   (prefix2, base, suffix2)
# )
def extract_proto_morphemes(s1, s2):
    sh, conv = strutil.str_convolution_max(s1, s2)      # Определяем смещение наилучшего совмещения строк
    ss1, ss2 = strutil.str_split_by_equal(s1, s2, sh)   # Разбиваем строки на интервалыодинаковых и разных подстрок

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

    return \
        (
              (''.join(ss1[:proto_root_pos]), ss1[proto_root_pos], ''.join(ss1[proto_root_pos + 1:]))
            , (''.join(ss2[:proto_root_pos]), ss2[proto_root_pos], ''.join(ss2[proto_root_pos + 1:]))
        )

    # proto_prefixes = \
    #     [
    #           ''.join(ss1[:proto_root_pos])
    #         , ''.join(ss2[:proto_root_pos])
    #     ]
    # proto_suffixes = \
    #     [
    #           ''.join(ss1[proto_root_pos + 1:])
    #         , ''.join(ss2[proto_root_pos + 1:])
    #     ]
    # proto_prefixes = [o for o in proto_prefixes if o != '']
    # proto_suffixes = [o for o in proto_suffixes if o != '']
    #
    # return \
    #     (
    #         # прото-префиксы
    #         proto_prefixes,
    #         # прото-основа
    #         ss1[proto_root_pos],
    #         # прото-суффиксы
    #         proto_suffixes
    #     )


# ----------------------------------------------------------------------------------------------------------------------
# Построение таблицы прото-аффиксов и прото-основ
def build_proto_affixes_table(db, comparison_threshould):
    cursor_wfs = db.cursor()
#     cursor_ngr = db.cursor()
    cursor_afx = db.cursor()

    cursor_afx.execute('DROP TABLE IF EXISTS proto_afx')
    cursor_afx.execute(
        # '''CREATE TABLE IF NOT EXISTS proto_afx
        #  (
        #        id       INTEGER PRIMARY KEY
        #      , afx      TEXT
        #      , type     INTEGER
        #      , wf_id    INTEGER
        #  )
        # '''
        '''CREATE TABLE IF NOT EXISTS proto_afx
         (
               id       INTEGER PRIMARY KEY
             , afx      TEXT
             , freq     INTEGER
             , info     TEXT
         )
        '''
    )

    max_wf_len = 0
    for wf_len in cursor_wfs.execute('SELECT LENGTH(wf) FROM wfs ORDER BY LENGTH(wf) DESC LIMIT 1'):
        max_wf_len = wf_len[0]

    wfs_gen = lambda: cursor_wfs.execute('SELECT id, wf, freq FROM wfs ORDER BY LENGTH(wf) DESC')

    def build_afx_info(wfpairs):
        l1 = []
        for wfp in wfpairs:
            l1.append('{' + wfp[0] + ',' + wfp[1] + '}')
        return ' '.join(l1)

    # найти словоформы-кандидаты для поиска прото-аффиксов
    def get_candidates(wf, afxlen):
        ngrlen = len(wf) - afxlen
        for ngr in strutil.str_build_n_gramms_fix_len(wf, ngrlen):
            for candidate_id, candidate in get_wordform_by_nramm(db, ngr):
                # dldist = pyxdameraulevenshtein.damerau_levenshtein_distance(candidate, wf)
                if candidate == wf: continue
                # if dldist > comparison_threshould: continue
                yield candidate_id, candidate

    affixes_counter = listutil.ObjectCounterTagged(lambda: [])
    affixes = []

    for afxlen in range(1, max_wf_len):
        print('afxlen: ', afxlen)
        wfs = wfs_gen()
        for (wf_id, wf, freq) in wfs:
            candidates = set(get_candidates(wf, afxlen))
            for candidate_id, candidate in candidates:
                proto_morphemes = extract_proto_morphemes(wf, candidate)
                # new_affixes = (
                #       (proto_morphemes[0][0], 1, wf_id)
                #     , (proto_morphemes[0][2], 2, wf_id)
                #     # , (proto_morphemes[1][0], 1, candidate_id)
                #     # , (proto_morphemes[1][2], 2, candidate_id)
                # )

                if proto_morphemes[1][0] != '' or proto_morphemes[1][2] != '':
                    continue

                affixes.append((proto_morphemes[0][0], 1, wf_id, candidate_id, wf, candidate))
                affixes.append((proto_morphemes[0][2], 2, wf_id, candidate_id, wf, candidate))

                # new_affixes = [afx for afx in new_affixes if len(afx[0]) == afxlen]
                # for afx in new_affixes:
                #     affixes.add(afx[0]).append((wf, candidate))

                # affixes.extend(new_affixes)
                # cursor_afx.executemany('INSERT INTO proto_afx VALUES(NULL,?,?,?)', new_affixes)
                pass

        affixes = [afx for afx in affixes if len(afx[0]) == afxlen]
        for afx in affixes:
            affixes_counter.add(afx[0]).append((afx[4], afx[5]))
        cursor_afx.executemany('INSERT INTO proto_afx VALUES(NULL,?,?,?)',
                               (
                                   (
                                       afx[0],
                                       afx[1],
                                       build_afx_info(afx[2])
                                   )
                                   for afx in affixes_counter.elements()
                               ))
        db.commit()
        affixes.clear()
        affixes_counter.clear()

    db.commit()

    pass



########################################################################################################################
