import time
import numpy as np
import matplotlib.pyplot as plt
from pandas import *
from matplotlib import mlab

df = pandas.DataFrame()
df.groupby()


df = df.set_index('STNAME')
def fun(item):
    if item[0]<'M':
        return 0
    if item[0]<'Q':
        return 1
    return 2

for group, frame in df.groupby(fun):
    print('There are ' + str(len(frame)) + ' records in group ' + str(group) + ' for processing.')



np.random.seed(int(time.time()))

mu = 200
sigma = 25
# x = np.random.normal(mu, sigma, size=1000000)
x = np.random.exponential(1, size=1000000)

# fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(8, 4))
fig, ax0 = plt.subplots(ncols=1, figsize=(8, 4))

ax0.hist(x, 200, normed=1, histtype='stepfilled', facecolor='g', alpha=0.75)
# ax0.set_title('stepfilled')

# # Create a histogram by providing the bin edges (unequally spaced).
# bins = [100, 150, 180, 195, 205, 220, 250, 300]
# ax1.hist(x, bins, normed=1, histtype='bar', rwidth=0.8)
# ax1.set_title('unequal bins')

fig.tight_layout()
plt.show()