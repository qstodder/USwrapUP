#!/usr/bin/python3

import os
import numpy as np
import pandas as pd
import pylab
import matplotlib.pyplot as plt
import datetime as datetime

f = 'mar 1 to apr 26 all hoods.csv'                     # datasheet: in the form of "semiRawExample" EXCEPT i inserted each hood's offset where "max val" usually is
topPath = 'C:/Users/fm-student6/Desktop/US/Hoods/'     # directary where datasheet store, and where plot pic folders will be placed
xls = pd.read_csv(topPath+f)
dayNum = 57                         # CHANGE THIS EACH TIME - number of days covered with data

## ---------- Nick, here's your path splitting code if you want to use it instead 
# pathToks = filePath.split('/')
# topPath = '' if len(pathToks) > 1 else '.'      
# for i in range(1, len(pathToks) - 1):
#     topPath += '/' + pathToks[i]
#     topPath += pathToks[i] + '/'
# # topPath += '/'

fumeLables = xls.iloc[7, 1:].values.tolist()        # hood identifyer
timestamp = xls.iloc[7:, 0].values.tolist()         
data = xls.iloc[8:, 1:].astype(float)               # just the data
OffVal = xls.iloc[5, 1:].astype(float)              # grab the offsets (I put these in the row where max val usually is... will probably have to change this)
lastWk = xls.iloc[4036:, 1:].astype(float)          # last 7 days of data (to determine if hood's in use based on just recent values)

# ------------ Determine if in use or not ------------
leftOpen, closed, inUse = [], [], []              # create subsets
leftOpen.append(timestamp)                        # add column of timestamps as the to the first column of subset
closed.append(timestamp)
inUse.append(timestamp)

notInUse = 0
leftOpenCount=0
for i, column in enumerate(data.columns):
    data.iloc[:,i] -= OffVal.iloc[i]        # apply offset to data
    lastWk.iloc[:,i] -= OffVal.iloc[i]      # check standard deviation of last 7 days (to see what's left currently left open)
    d = lastWk.iloc[:,i]                   
    # print(np.std(d))
    temp = []                               # creating a temp array to eliminate all the gross headers, and also convert data to a list
    temp[1:] = data.iloc[:,i].tolist()      # append just the data
    temp.insert(0, fumeLables[i])           # insert in the hood identifyer string at the top
    if np.std(d)<1:      
        notInUse += 1                       # hood is being used if standard dev. is greater than 1
        if np.mean(d)>5:                    # hood is open if % open is greater than 5%
            leftOpen.append(temp)
            leftOpenCount += 1
        else: closed.append(temp)           
    else: inUse.append(temp)
print("not in use: " + str(notInUse))
print("left open: " + str(leftOpenCount))

# ----------- Hoods in Use: sort into good and bad -----------
good, bad = [], []
good.append(timestamp)
bad.append(timestamp)

bc, gc = 0,0            # bad count and good count
durration = []          # to determine how long it's been open
tot_hours = dayNum*24
for c in range(len(inUse)):
    if c == 0: continue
    count = 0           # temp var to determine how long it's been open
    for r in range(len(inUse[0])):
        if r < 3: continue
        # if current height is equal to the previous two heights, and is also greater than 5%
        elif inUse[c][r] == inUse[c][r-1] and inUse[c][r-1] == inUse[c][r-2] and inUse[c][r]>5: count += 1
    if count > 0: 
        bad.append(inUse[c])
        bc += 1
        durration.append(round(count/tot_hours*100))      # supposed to be percentage of openness
    else: 
        good.append(inUse[c])
        gc += 1

print("bad: " + str(bc))
print("good: " + str(gc))
print(len(durration))

# # ---------------------- WRITE TO FILE -----------------------
# rows = [''] * len(leftOpen[0])                      # Left Open
# for i, col in enumerate(leftOpen):
#     for j, row in enumerate(col):
#         if i > 0:
#             rows[j] = ','.join([rows[j], str(row)])
#         else:
#             rows[j] = str(row)

# res = '\n'.join(rows)
# with open(topPath+'leftOpen.csv', 'w') as o:
#     o.write(res)

# rows = [''] * len(closed[0])                        # closed
# for i, col in enumerate(closed):
#     for j, row in enumerate(col):
#         if i > 0:
#             rows[j] = ','.join([rows[j], str(row)])
#         else:
#             rows[j] = str(row)

# res = '\n'.join(rows)
# with open(topPath+'closed.csv', 'w') as o:
#     o.write(res)

# rows = [''] * len(good[0])                          # good
# for i, col in enumerate(good):
#     for j, row in enumerate(col):
#         if i > 0:
#             rows[j] = ','.join([rows[j], str(row)])
#         else:
#             rows[j] = str(row)

# res = '\n'.join(rows)
# with open(topPath+'good.csv', 'w') as o:
#     o.write(res)

# rows = [''] * len(bad[0])                           # bad
# for i, col in enumerate(bad):
#     for j, row in enumerate(col):
#         if i > 0:
#             rows[j] = ','.join([rows[j], str(row)])
#         else:
#             rows[j] = str(row)

# res = '\n'.join(rows)
# with open(topPath+'bad.csv', 'w') as o:
#     o.write(res)

# ## ---- For plot development: ------
# # x_vals = np.linspace(0,dayNum,len(bad[0])-1)
# # fig = pylab.gcf()
# # ax = pylab.subplot(111)
# # ax.plot(x_vals,bad[1][1:])
# # ax.set_title(bad[1][0])
# # ax.set_ylim(-2,102)
# # ax.set_xlabel("Days since 3/1"+ ' open ' + str(durration[0]) + "% of time")
# # plt.show()

# # ------- Create and Save Graphs for Bad Hoods -----------
# badPath = topPath + "bad Hoods/"
# if not os.path.exists(badPath): os.makedirs(badPath)

# x_vals = np.linspace(0,dayNum,len(bad[0])-1)
# for i in range(len(bad)):
#     if i == 0: continue
#     fig = pylab.gcf()
#     ax = pylab.subplot(111)
#     ax.plot(x_vals,bad[i][1:])
#     ax.set_title(bad[i][0])
#     ax.set_ylim(-2,102)
#     ax.set_xlabel("Days since 3/1")
#     plt.savefig(badPath + 'FH_' + str(i) + ' open ' + str(durration[i-1]) + "% of time.png", dpi=300, bbox_inches='tight')
#     pylab.clf()

# # ------- Create and Save Graphs for Good Hoods -----------
# goodPath = topPath + "good Hoods/"
# if not os.path.exists(goodPath): os.makedirs(goodPath)

# x_vals = np.linspace(0,dayNum,len(good[0])-1)
# for i in range(len(good)):
#     if i == 0: continue
#     fig = pylab.gcf()
#     ax = pylab.subplot(111)
#     ax.plot(x_vals,good[i][1:])
#     ax.set_title(good[i][0])
#     ax.set_ylim(-2,102)
#     ax.set_xlabel("Days since 3/1")
#     plt.savefig(goodPath + 'FH_' + str(i) + '.png', dpi=300, bbox_inches='tight')
#     pylab.clf()

