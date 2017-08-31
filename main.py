import os
import sqlite3 as sql

import time
import matplotlib.pyplot as plt

from util import listutil

import results
import graphemat
import morpho

# import Levenshtein

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

db = sql.connect('.temp/lingua.db')

# graphemat.store_wordforms_to_db(db, graphemat.load_file('data/utf8_test_003.txt'))
#
# morpho.create_ngramms_table(db)



# TODO: Вывести параметр для сравнения в настройки (???)
morpho.build_proto_affixes_table(db, 2)
#
# c = db.cursor()


# results.show__wflen_distribution(db)
