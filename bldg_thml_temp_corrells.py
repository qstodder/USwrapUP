
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seabornInstance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression as linreg
import statsmodels.formula.api as sm
from scipy import stats
from sklearn import metrics
from psypy import psyIP as psy


xls = pd.ExcelFile('C:/Users/fm-student6/Desktop/US/Bldg Thermal Temp Correlations/Correllation Data.xlsx')
htw = xls.parse(sheet_name = "Dly HTW")
chw = xls.parse(sheet_name = "Dly CHW")
elec = xls.parse(sheet_name = "Dly Elec")
climate = xls.parse(sheet_name = "Dly Climate")
temp = climate['avgTemp']
hum = climate['avgHum']

enth = []
for i in range(len(temp)):
    t = temp.iloc[i] + 459.67
    h = hum.iloc[i]/100
    E = psy.state("DBT", t, "RH", h, 14.7)
    enth.append(E[1])
enth_chw = np.append(np.linspace(0,15,50), enth)
temp_htw = np.append(temp, np.linspace(79, 100, 100)
temp_elec = np.append(np.linspace(40,50,100), temp)

chwNames = chw.columns.values.tolist()
htwNames = htw.columns.values.tolist()
elecNames = elec.columns.values.tolist()

# c = chw.iloc[:,2]
# print(type(c))
# print(type(temp))
# print(type(hum))
# bldg1 = pd.DataFrame({'CHW': chw.iloc[:,2], 'Temp': temp, 'Hum': hum})
# # print(bldg1.head())
# model = sm.ols('CHW ~ 1 + Temp + Hum', data = bldg1).fit(disp=0)
# # print(model.summary())
# a0, a1, a2 = model.params.Intercept, model.params.Temp, model.params.Hum
# b = chwNames[2]

c_intcpt, c_1, c_2, c_r2 = [], [], [], []
c_maxs, c_mins = [], []

for i, c in enumerate(chwNames):
    if i == 0: continue
    minVal = min(chw.iloc[:,i])
    chw_w = np.append(np.linspace(minVal,minVal,50).tolist(), chw.iloc[:,i])
    cFit = np.polyfit(enth_chw, chw_w, 2)
    cMean = np.mean(chw_w)
    cHat = cFit[0]*enth_chw**2 + cFit[1]*enth_chw + cFit[2]
    ssreg = sum([(cHat_i - cMean)**2 for cHat_i in cHat])
    sstot = sum([(ci - cMean)**2 for ci in chw_w])
    if sstot != 0: r_sq = ssreg/sstot
    else: r_sq = 0
# add model params to lists
    c_intcpt.append(cFit[2])
    c_1.append(cFit[1])
    c_2.append(cFit[0])
    c_r2.append(r_sq)
    c_mins.append(minVal)
    c_maxs.append(max(chw.iloc[:,i]))

    # print(chwNames[i])
    # print(ssreg)
    # print(sstot)
    # print(r_sq)

h_intcpt, h_1, h_2, h_r2 = [], [], [], []
h_maxs, h_mins = [], []

for i, h in enumerate(htwNames):
    if i == 0: continue
    minVal = min(htw.iloc[:,i])
    htw_w = np.append(htw.iloc[:,i], np.linspace(minVal,minVal,100).tolist())
    hFit = np.polyfit(temp_htw, htw_w, 2)
    hMean = np.mean(htw_w)
    hHat = hFit[0]*temp_htw**2 + hFit[1]*temp_htw + hFit[2]
    ssreg = sum([(hHat_i - hMean)**2 for hHat_i in hHat])
    sstot = sum([(hi - hMean)**2 for hi in htw_w])
    if sstot != 0: r_sq = ssreg/sstot
    else: r_sq = 0
# add model params to lists
    h_intcpt.append(hFit[2])
    h_1.append(hFit[1])
    h_2.append(hFit[0])
    h_r2.append(r_sq)
    h_mins.append(minVal)
    h_maxs.append(max(htw.iloc[:,i]))

e_intcpt, e_1, e_2, e_r2 = [], [], [], []
e_maxs, e_mins = [], []

for i, e in enumerate(elecNames):
    if i == 0: continue
    minVal = min(elec.[:,i])
    elec_w = np.append(elec.iloc[:,i], np.linspace(minVal,minVal,100).tolist())
    eFit = np.polyfit(temp_elec, elec_w, 2)
    eMean = np.mean(elec_w)
    eHat = eFit[0]*temp_elec**2 + eFit[1]*temp_elec + eFit[2]
    ssreg = sum([(eHat_i - eMean)**2 for eHat_i in eHat])
    sstot = sum([(ei - eMean)**2 for ei in elec_w])
    if sstot != 0: r_sq = ssreg/sstot
    else: r_sq = 0
# add model params to lists
    e_intcpt.append(eFit[2])
    e_1.append(eFit[1])
    e_2.append(eFit[0])
    e_r2.append(r_sq)
    e_mins.append(minVal)
    e_maxs.append(max(elec.iloc[:,i]))

with open('C:/Users/fm-student6/Desktop/US/Bldg Thermal Temp Correlations/CHWresults.csv', 'w') as CHWresults:
    res = '\n'.join([
        ','.join([a for a in chwNames if a != 'date']),
        ','.join([str(a) for a in c_intcpt]),
        ','.join([str(a) for a in c_1]),
        ','.join([str(a) for a in c_2]),
        ','.join([str(a) for a in c_mins]),
        ','.join([str(a) for a in c_maxs]),
        ','.join([str(a) for a in c_r2]),
    ])

    CHWresults.write(res)
    print("done")

with open('C:/Users/fm-student6/Desktop/US/Bldg Thermal Temp Correlations/HTWresults.csv', 'w') as HTWresults:
    res = '\n'.join([
        ','.join([a for a in htwNames if a != 'date']),
        ','.join([str(a) for a in h_intcpt]),
        ','.join([str(a) for a in h_1]),
        ','.join([str(a) for a in h_2]),
        ','.join([str(a) for a in h_mins]),
        ','.join([str(a) for a in h_maxs]),
        ','.join([str(a) for a in h_r2]),
    ])

    HTWresults.write(res)

# bhat = a0 + a1*temp + a2*hum

# fig, ax = plt.subplots()
# ax.scatter(temp, blg1, label = "temp")
# ax.scatter(hum,blg1, label = "hum")
# ax.legend()
# ax.set_xlabel("temp/hum")
# ax.set_ylabel("daily mmbtu")
# plt.show()
