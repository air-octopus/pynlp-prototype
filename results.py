import sqlite3 as sql
import matplotlib.pyplot as plt

from util import listutil


def show__wflen_distribution(db):
    c = db.cursor()
    ooo = listutil.count_same_elements(o[0] for o in c.execute('SELECT LENGTH(wf) FROM wfs'))
    ooo = list(ooo)
    ooo.sort(key=lambda x: x[0])

    xx = [o[0] for o in ooo]
    yy = [o[1] for o in ooo]

    plt.plot(xx, yy)
    plt.show()


# ----------------------------------------------------------------------------------------------------------------------
#
def show__protoaffixes_distribution(db):
    c = db.cursor()

    # for len in range(1, afxlen):
        # ooo = c.execute('SELECT afx, freq FROM proto_afx WHERE LENGTH(afx)=:afxlen ORDER BY freq DESC', {'afxlen': len})
    ooo = c.execute('SELECT afx, freq FROM proto_postfixes ORDER BY freq DESC')

    # xx = [o[0] for o in ooo]
    yy = [o[1] for o in ooo]
    plt.plot(yy)

    plt.show()


