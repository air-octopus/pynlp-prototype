import sqlite3 as sql
import itertools
#import Levenshtein

import strutil
import graphemat
import morpho

import os

os.makedirs('.temp', exist_ok=True)


# import pandas as pd
# purchase_1 = pd.Series({'Name': 'Chris',
# 'Item Purchased': 'Dog Food',
# 'Cost': 22.50})
# purchase_2 = pd.Series({'Name': 'Kevyn',
# 'Item Purchased': 'Kitty Litter',
# 'Cost': 2.50})
# purchase_3 = pd.Series({'Name': 'Vinod',
# 'Item Purchased': 'Bird Seed',
# 'Cost': 5.00})
# df = pd.DataFrame([purchase_1, purchase_2, purchase_3], index=['Store 1', 'Store 1', 'Store 2'])
# df.head()
# print(df)
#
# df['Store 1'].


# print(strutil.str_convolution_max('abcd', 'oabqde'))
#
# print(strutil.str_split_by_equal('rabcdefgh', 'abcqpmgyli', 1))
#
# ttt = morpho.extract_proto_morphemes('rabcdefgh', 'abcqpmgyli')
#
# print(strutil.str_build_n_gramms_fix_len('abcdefghij', 3))
#
# print(strutil.str_build_n_gramms('abcde'))

text = graphemat.load_file('data/test_003.txt')

wfs = dict()
for wf in text:
    strutil.str_store_to_dict(wfs, wf)



db = sql.connect('.temp/lingua.db')
c = db.cursor()

c.execute('DROP TABLE IF EXISTS wfs')
c.execute('''CREATE TABLE IF NOT EXISTS wfs
             (
                   id       INTEGER PRIMARY KEY
                 , wf       TEXT
                 , usage    INTEGER
             )
          ''')

c.executemany('INSERT INTO wfs VALUES (NULL,?,?)', (wf for wf in wfs.items()))

db.commit()

# ngramms = dict
#
# wfs