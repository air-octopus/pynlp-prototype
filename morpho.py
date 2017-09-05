# Методы морфологического анализа

#import Levenshtein
#import pyxdameraulevenshtein

from util import strutil
from util import listutil

import graphemat


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


def create_ngramms_beg_table(db):
    cngr = db.cursor()
    cngr.execute('DROP TABLE IF EXISTS ngramms_beg')
    cngr.execute(
        '''CREATE TABLE IF NOT EXISTS ngramms_beg
         (
               id       INTEGER PRIMARY KEY
             , ngr      TEXT
             , wf_id    INTEGER
         )
        '''
    )
    cngr.execute('CREATE INDEX idx_ngramms_beg_001 ON ngramms_beg (ngr)')

    wfs = db.cursor().execute('SELECT id, wf FROM wfs')

    def ngramms():
        for wf_id, wf in wfs:
            for ngrlen in range(1, len(wf)+1):
                yield wf[:ngrlen], wf_id

    cngr.executemany('INSERT INTO ngramms_beg VALUES (NULL,?,?)', ngramms())

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
# Найти словоформы по начальной n-грамме
# DB requirements:
#       существуют и проинициализированы таблицы wfs и ngramms_beg
# DB results:
#       NONE
def get_wordform_by_nramm_beg(db, ngr):
    # cursor_ngr = db.cursor()
    query = 'SELECT DISTINCT wfs.id, wfs.wf FROM wfs, ngramms_beg WHERE wfs.id=ngramms_beg.wf_id AND ngramms_beg.ngr=:ngr'
    yield from db.cursor().execute(query, {'ngr': ngr})


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
def build_afx_info(wfpairs):
    l1 = []
    for wfp in wfpairs:
        l1.append('{' + wfp[0] + ',' + wfp[1] + '}')
    return ' '.join(l1)


# ----------------------------------------------------------------------------------------------------------------------
# Построение таблицы прото-аффиксов и прото-основ
def build_proto_affixes_table(db, comparison_threshould):
    cursor_wfs = db.cursor()
    cursor_bas = db.cursor()
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

    def wf_splitter_preffix(wf, afxlen):
        return wf[afxlen:], wf[:afxlen]

    def wf_splitter_postfix(wf, afxlen):
        pos = len(wf)- afxlen
        return wf[:pos], wf[pos:]

    postfixes_counter = listutil.ObjectCounterTagged(lambda: [])

    # принимаем словоформу, выделяем из нее предполагаемый аффикс и проверяем наличие остатка в общем массиве словоформ
    # splitter -- процедура разделения словоформы на аффикс и остаток
    def check_affix(wf, afxlen, splitter, counter):
        base, afx = splitter(wf, afxlen)
        for base_id in cursor_bas.execute('SELECT id FROM wfs WHERE wf=:wf LIMIT 1', {'wf': base}):
            counter.add(afx).append((wf, base))

    # # найти словоформы-кандидаты для поиска прото-аффиксов
    # def get_candidates(wf, afxlen):
    #     ngrlen = len(wf) - afxlen
    #     for ngr in strutil.str_build_n_gramms_fix_len(wf, ngrlen):
    #         for candidate_id, candidate in get_wordform_by_nramm(db, ngr):
    #             # dldist = pyxdameraulevenshtein.damerau_levenshtein_distance(candidate, wf)
    #             if candidate == wf: continue
    #             # if dldist > comparison_threshould: continue
    #             yield candidate_id, candidate
    #
    # affixes_counter = listutil.ObjectCounterTagged(lambda: [])
    affixes = []

    for afxlen in range(1, int(max_wf_len/3)):
        print('afxlen: ', afxlen)
        wfs = wfs_gen()
        for (wf_id, wf, freq) in wfs:
            check_affix(wf, afxlen, wf_splitter_postfix, postfixes_counter)

        #     candidates = set(get_candidates(wf, afxlen))
        #     for candidate_id, candidate in candidates:
        #         proto_morphemes = extract_proto_morphemes(wf, candidate)
        #         # new_affixes = (
        #         #       (proto_morphemes[0][0], 1, wf_id)
        #         #     , (proto_morphemes[0][2], 2, wf_id)
        #         #     # , (proto_morphemes[1][0], 1, candidate_id)
        #         #     # , (proto_morphemes[1][2], 2, candidate_id)
        #         # )
        #
        #         if proto_morphemes[1][0] != '' or proto_morphemes[1][2] != '':
        #             continue
        #
        #         affixes.append((proto_morphemes[0][0], 1, wf_id, candidate_id, wf, candidate))
        #         affixes.append((proto_morphemes[0][2], 2, wf_id, candidate_id, wf, candidate))
        #
        #         # new_affixes = [afx for afx in new_affixes if len(afx[0]) == afxlen]
        #         # for afx in new_affixes:
        #         #     affixes.add(afx[0]).append((wf, candidate))
        #
        #         # affixes.extend(new_affixes)
        #         # cursor_afx.executemany('INSERT INTO proto_afx VALUES(NULL,?,?,?)', new_affixes)
        #         pass
        #
        # affixes = [afx for afx in affixes if len(afx[0]) == afxlen]
        # for afx in affixes:
        #     affixes_counter.add(afx[0]).append((afx[4], afx[5]))
        cursor_afx.executemany('INSERT INTO proto_afx VALUES(NULL,?,?,?)',
                               (
                                   (
                                       afx[0],
                                       afx[1],
                                       build_afx_info(afx[2])
                                   )
                                   for afx in postfixes_counter.elements()
                               ))
        db.commit()
        affixes.clear()
        postfixes_counter.clear()

    db.commit()

    pass


# ----------------------------------------------------------------------------------------------------------------------
# Построение таблицы прото-постфиксов
def build_proto_postfixes_table(db):
    cursor_wfs = db.cursor()
    cursor_afx = db.cursor()

    cursor_afx.execute('DROP TABLE IF EXISTS proto_postfixes')
    cursor_afx.execute(
        '''CREATE TABLE IF NOT EXISTS proto_postfixes
         (
               id       INTEGER PRIMARY KEY
             , afx      TEXT
             , freq     INTEGER
             , info     TEXT
         )
        '''
    )
    cursor_afx.execute('CREATE INDEX idx_proto_postfixes_001 ON proto_postfixes (afx)')
    cursor_afx.execute('CREATE INDEX idx_proto_postfixes_002 ON proto_postfixes (LENGTH(afx))')
    cursor_afx.execute('CREATE INDEX idx_proto_postfixes_003 ON proto_postfixes (freq)')

    affixes = listutil.ObjectCounterTagged(lambda: [])

    max_wf_len = graphemat.get_max_wfs_len(db)
    wfs_gen = lambda: cursor_wfs.execute('SELECT id, wf, freq FROM wfs ORDER BY wf ASC')

    for wf_id, wf, freq in wfs_gen():
        wf_len = len(wf)
        ngr = wf[:int((wf_len+1)/2)]

        wf_affixes = dict()

        for candidate_id, candidate in get_wordform_by_nramm_beg(db, ngr):
            candidate_len = len(candidate)
            if wf_len < 3: continue
            if candidate <= wf: continue
            if candidate_len > 2*wf_len+1: continue

            base, afx1, afx2 = strutil.str_extract_same_beg(wf, candidate)

            afx1_len = len(afx1)
            afx2_len = len(afx2)
            base_len = len(base)

            if afx1_len + 3 > base_len: afx1 = ''
            if afx2_len + 3 > base_len: afx2 = ''

            if afx1 != '':
                second_parts = wf_affixes.get(afx1, [])
                second_parts.append(candidate)
                wf_affixes[afx1] = second_parts
            if afx2 != '':
                affixes.add(afx2).append((candidate, wf))

        for afx, candidates in wf_affixes.items():
            afx_tag = affixes.add(afx)
            for candidate in candidates:
                afx_tag.append((wf, candidate))

    cursor_afx.executemany('INSERT INTO proto_postfixes VALUES(NULL,?,?,?)',
                           (
                               (
                                   afx[0],
                                   afx[1],
                                   build_afx_info(afx[2])
                               )
                               for afx in affixes.elements()
                           ))
    db.commit()
    affixes.clear()


# ----------------------------------------------------------------------------------------------------------------------
# Представление длинных сложных постфиксов в видепоследовательности нескольких более коротких
def decompose_postfixes(db):
    cursor_afx = db.cursor()
    data = cursor_afx.execute('SELECT afx FROM proto_postfixes ORDER BY LENGTH(afx) ASC')
    affixes = list(afx[0] for afx in data)
    affixes_set = set(affixes)
    affixes_new = []

    for afx in affixes:
        components = strutil.str_decompose(afx, affixes, False)
        if len(components) > 0:
            affixes_set = affixes_set - {afx}

    pass


# ----------------------------------------------------------------------------------------------------------------------
# Построение таблицы постфиксов
def build_postfixes_table(db):
    build_proto_postfixes_table(db)

########################################################################################################################
