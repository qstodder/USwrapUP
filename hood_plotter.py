#!/usr/bin/python3

import os
import numpy as np
import pandas as pd
import pylab
import matplotlib.pyplot as plt
import datetime as datetime

f = 'apr opperational.csv'
filePath = 'C:/Users/fm-student6/Desktop/US/Hoods/'
xls = pd.read_csv(filePath+f)

# Want to get the path to file (not including file name) for outputting stuff...
# pathToks = filePath.split('/')
# topPath = '' if len(pathToks) > 1 else '.'      # If calling from that directory, make sure pointing to the current directory, not the root directory
# for i in range(1, len(pathToks) - 1):
#     topPath += '/' + pathToks[i]
#     topPath += pathToks[i] + '/'
# # topPath += '/'
# outPath = topPath + '/'
outPath = filePath + '/plots/'
if not os.path.exists(outPath): os.makedirs(outPath)

fumeLables = xls.iloc[7, 1:].values.tolist()
# datetime = xls.iloc[8:, 0].values.tolist()
data = xls.iloc[8:, 1:].astype(float)
OffVal = xls.iloc[5,1:].astype(float)

# print(data.iloc[0:10, 0:2])
# print(datetime[2])
# print(type(fumeLables))

# for i, col in enumerate(data.columns):
#     # print(type(data.iloc[1,i]))
#     # print(data.iloc[1,i])
#     data.iloc[:,i] -= OffVal.iloc[i]
    
x_ticks = np.arange(0,50, 3)
x_vals = np.linspace(0,50,len(data.iloc[:,3]))

start = datetime.datetime.strptime("2020-03-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-04-19", "%Y-%m-%d")
date_array = (start + datetime.timedelta(days=x) for x in range(0, (end-start).days) if (x%3 == 0))

print(x_ticks)
print(len(x_vals))
print(len(data.iloc[:,3]))

for i in range(len(fumeLables)):
    fig = pylab.gcf()
    ax = pylab.subplot(111)
    ax.plot(x_vals,data.iloc[:,i])
    ax.set_title(fumeLables[i])
    ax.set_ylim(-2,102)
    # plt.xticks(x_ticks, date_array, rotation = 20)
    # plt.show()
    ax.set_xlabel("Days since 3/1")
    plt.savefig(outPath + 'FH_' + str(i) + '.png', dpi=300, bbox_inches='tight')
    pylab.clf()


# first_dataIndex = 1 # In principle the first row is informational (the name of the columns, for each sheet), not data

# outPath = topPath + '/'
# # We're going to want to place all the plots for a single sheet in its own directory...
# if not os.path.exists(outPath): os.makedirs(outPath)

# # Might want to identify the regions where it's day vs night and highlight them differently on the plot...
# dates, times, doys = map(np.array, ([], [], []))
# for timeStamp in datetime:
#     # Need to convert timestamps to usable x range: day of year, for plotting.
#     date = timeStamp.strftime("%m/%d/%Y")
#     hr, mn, sec = map(float, (timeStamp.strftime("%H"), timeStamp.strftime("%M"), timeStamp.strftime("%S")))
#     dates, times = (np.append(dates, date), np.append(times, timeStamp.strftime("%H:%M")))      # Really don't care about the seconds field: in principle for this stuff it's always a 0.
#     fractionalDay = (hr + mn/60. + sec/3600.)/24.
#     doy = pd.Period(date).dayofyear + fractionalDay # pd.Period always assumes month comes before day, which is also the case for our dates.
#     doys = np.append(doys, doy)

# # Night time is considered 9 pm to 7 am, according to how Quiana has processed previous things
# fdsOnly = doys % 1  # just the fractional part
# wh_night = np.where((fdsOnly >= 21/24.) | (fdsOnly <= 7/24.))[0]
# wh_day = np.where((fdsOnly < 21/24.) & (fdsOnly > 7/24.))[0]
# # When using pylab.fill_between during plotting, the "where" argument needs a list of bools for each index (rather than the indices
# # themselves) whether to fill for that point or not
# bool_wh_night = np.zeros(len(fdsOnly))
# bool_wh_night[wh_night] = 1

# # Now, make doys relative to first in the list, so can plot 'days since first date'
# doys_adjusted = doys - doys[0]

# for fumeIndex in range(len(fumeLabels)):        # the first in list should be the first fume hood column (not timestamps)

#     fumeHood = fumeLabels[fumeIndex]
#     fumeData = np.array(data[fumeHood][first_dataIndex:], dtype=np.float64) # In principle the first two rows are informational, not data; Make sure it gets converted to be an array of floats, not objects
    
#     fumeAvg, fumeStdev = (np.mean(fumeData), np.std(fumeData))

#     fig = pylab.gcf()
#     ax = pylab.subplot(111)
#     ax.plot(doys_adjusted, fumeData, color='b', alpha=0.8)
#     # Plot the individual markers too, to see the invidual samples
#     #ax.plot(doys_adjusted, fumeData, marker='.', markersize=0.3, linewidth=0, color='r')

#     # Plot the average, and fill between 1 sigma bounds
#     ax.axhline(fumeAvg, color='c', alpha=0.7, linestyle='--', label='Mean %.1f' %fumeAvg)
#     ax.fill_between(doys_adjusted, fumeAvg - fumeStdev, fumeAvg + fumeStdev, color='c', alpha=0.2, label=r'1-$\sigma$ bounds')

#     ax.fill_between(doys_adjusted, -2, 102, where=bool_wh_night, color='k', alpha=0.1, label='Nighttime')

#     # after drawing the fill between, it rescales the axes such that the fill between doesn't span the entire y range. So, reset
#     # the range to what found prior to filling...
#     ax.set_ylim(-2,102)

#     ax.set_xlabel('Days since %s' %str(timeStamps.loc[first_dataIndex]))
#     ax.legend(loc='upper right', bbox_to_anchor=(1.05, 1.11), fontsize=8)

#     fig.text(0.08, 0.45, 'Sash height %', rotation='vertical', va='center')
#     # Set the aspect ratio so that it matches the paper template we're using...
#     # Had to change to what figure needed to be resized to, once Jake made up the template.
#     #fig.set_figwidth(11.)
#     fig.set_figwidth(10.1)
#     #fig.set_figheight(4.25)
#     fig.set_figheight(2.4)
#     fig.subplots_adjust(hspace=0.32)
#     # shutil.rmtree(outPath, ignore_errors=False, onerror=handleRemoveReadonly)
#     pylab.savefig(outPath + fumeHood + '.png', dpi=300, bbox_inches='tight')
#     pylab.clf()
    