import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from psypy import psyIP as psy

f = 'CHWGen.xlsx'
filePath = 'C:/Users/fm-student6/Desktop/US/Bldg Thermal Temp Correlations/'
# data = pd.read_csv(filePath+f)
xls = pd.ExcelFile(filePath+f)

data = xls.parse(sheet_name = 'CHWGen')
tonAvg = data.DlyAvg
tonPk = data.DlyPeak
tonSum = data.DlySum
temp = data.avgTemp
hum = data.avgHum

hrly = xls.parse(sheet_name = 'Hourly')
temp_hr = hrly.HrlyTemp
hum_hr = hrly.HrlyHum

# calculate enthalpy
enth = []
for i, t in enumerate(temp):
    h = hum.iloc[i]/100
    t += 459.67
    E = psy.state("DBT", t, "RH", h, 14.7)
    enth.append(E[1])

enth_hr = []
for i, t in enumerate(temp_hr):
    h = hum_hr.iloc[i]/100
    t += 459.67
    P = 14.7
    C8=-1.0440397*10**4
    C9=-1.1294650*10**1
    C10=-2.7022355*10**-2
    C11=1.2890360*10**-5
    C12=-2.4780681*10**-9
    C13=6.5459673
    Pw = h*np.exp(C8/t+C9+C10*t+C11*t**2+C12*t**3+C13*np.log(t))
    W = 0.621945*Pw/(P-Pw)
    DBT=t-459.67
    H =  0.240*DBT+W*(1061+0.444*DBT)
    # E = psy.state("DBT", t, "RH", h, P)
    enth_hr.append(H)

# get max daily enthalpy
# MaxEnth = max(enth_hr[i*24:(i*24+23)] for i in range(365))
MaxEnth = []
for i in range(365):
    m = max(enth_hr[i*24:(i*24+23)])
    MaxEnth.append(m)

enthlin = np.linspace(min(enth), max(enth), 200)
enthlin_max = np.linspace(min(MaxEnth), max(MaxEnth), 200)    

Afit = np.polyfit(enth, tonAvg, 2)
Ahat = Afit[0]*enthlin**2 + Afit[1]*enthlin + Afit[2]

Pfit = np.polyfit(MaxEnth, tonPk, 2)
Phat = Pfit[0]*enthlin_max**2 + Pfit[1]*enthlin_max + Pfit[2]

Sfit = np.polyfit(enth, tonSum, 2)
Shat = Sfit[0]*enthlin**2 + Sfit[1]*enthlin + Sfit[2]

print(Afit[2])
print(Afit[1])
print(Afit[0])

print(Pfit[2])
print(Pfit[1])
print(Pfit[0])

print(Sfit[2])
print(Sfit[1])
print(Sfit[0])

print(max(temp))
print(max(enth))
print(max(tonAvg))
print(max(tonPk))
print(max(tonSum))

print(max(MaxEnth))

fig, ax = plt.subplots(3,1,constrained_layout=True)
ax[0].scatter(enth, tonAvg)
ax[0].plot(enthlin, Ahat, color='red')
ax[0].set_title('Average Daily Tonnage')
ax[1].scatter(MaxEnth, tonPk)
ax[1].plot(enthlin_max, Phat, color='red')
ax[1].set_title('Peak Daily Tonnage')
ax[2].scatter(enth, tonSum)
ax[2].plot(enthlin, Shat, color='red')
ax[2].set_title('Total Daily Tonnage [ton-hr]')


## COMPARISON GRAPHS - normal load to COVID load

f = 'CHWGen_COVID.xlsx'
filePath = 'C:/Users/fm-student6/Desktop/US/Bldg Thermal Temp Correlations/'
xls = pd.ExcelFile(filePath+f)

data = xls.parse(sheet_name = 'CHWGen_COVID')
met_CVD = data.Met
met_pk_CVD = data.MetPk
temp_CVD = data.avgTemp
hum_CVD = data.avgHum

hrly_CVD = xls.parse(sheet_name = 'Hourly')
temp_hr_CVD = hrly_CVD.HrlyTemp
hum_hr_CVD = hrly_CVD.HrlyHum


# calculate enthalpy
enth_CVD = []
for i, t in enumerate(temp_CVD):
    h = hum_CVD.iloc[i]/100
    t += 459.67
    E = psy.state("DBT", t, "RH", h, 14.7)
    enth_CVD.append(E[1])

enth_hr_CVD = []
for i, t in enumerate(temp_hr_CVD):
    h = hum_hr_CVD.iloc[i]/100
    t += 459.67
    P = 14.7
    C8=-1.0440397*10**4
    C9=-1.1294650*10**1
    C10=-2.7022355*10**-2
    C11=1.2890360*10**-5
    C12=-2.4780681*10**-9
    C13=6.5459673
    Pw = h*np.exp(C8/t+C9+C10*t+C11*t**2+C12*t**3+C13*np.log(t))
    W = 0.621945*Pw/(P-Pw)
    DBT=t-459.67
    H =  0.240*DBT+W*(1061+0.444*DBT)
    # E = psy.state("DBT", t, "RH", h, P)
    enth_hr_CVD.append(H)

MaxEnth_CVD = []
for i in range(44):
    m = max(enth_hr_CVD[i*24:(i*24+23)])
    MaxEnth_CVD.append(m)

# fig, ax4 = plt.subplots()
# N = ax4.scatter(MaxEnth, tonPk, label='2019', facecolors='none', edgecolors='tab:orange')
# C = ax4.scatter(MaxEnth_CVD, met_pk_CVD, label='COVID-19')
# ax4.legend()
# ax4.set_title("COVID to Normal Peak Tonnage Comparison")
# ax4.set_xlabel("Enthalpy")
# ax4.set_ylabel("Peak Tonnage")
# plt.show()

enthlin_CVD = np.linspace(15, 40, len(met_CVD))  
enthlin_max_CVD = np.linspace(15, 40, len(met_pk_CVD))      

# weighted enth vectors
enth_CVDw = np.append(np.linspace(15, 20, 100).tolist(), enth_CVD)
met_CVDw = np.append(np.linspace(min(met_CVD),min(met_CVD),100).tolist(), met_CVD)

MaxEnth_CVDw = np.append(np.linspace(15, 20, 100).tolist(), MaxEnth_CVD)
met_pk_CVDw = np.append(np.linspace(min(met_pk_CVD),min(met_pk_CVD),100).tolist(), met_pk_CVD)

## Average load vs avg enth
Afit_CVD = np.polyfit(enth_CVD, met_CVD, 2)
Ahat_CVD = Afit_CVD[0]*enthlin_CVD**2 + Afit_CVD[1]*enthlin_CVD + Afit_CVD[2]
Mean = np.mean(met_CVD)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Ahat_CVD])
sstot = sum([(i-Mean)**2 for i in met_CVD])
ssres = sum([(y - Ahat[i])**2 for i, y in enumerate(met_CVD)])
MET_r_sq_CVD = 1 - ssres/sstot

## peak load vs peak enth 
Afit_Pk_CVD = np.polyfit(MaxEnth_CVD, met_pk_CVD, 2)
Ahat_Pk_CVD = Afit_Pk_CVD[0]*enthlin_max_CVD**2 + Afit_Pk_CVD[1]*enthlin_max_CVD + Afit_Pk_CVD[2]
Mean = np.mean(met_pk_CVD)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Ahat_Pk_CVD])
sstot = sum([(i-Mean)**2 for i in met_pk_CVD])
ssres = sum([(y - Ahat_Pk_CVD[i])**2 for i, y in enumerate(met_pk_CVD)])
MET_pk_r_sq_CVD = 1 - ssres/sstot


## redo 2019 data for 20-40 load
enthlin = np.linspace(15, 40, len(tonAvg))  
enthlin_max = np.linspace(15, 40, len(tonPk))  
Ahat = Afit[0]*enthlin**2 + Afit[1]*enthlin + Afit[2]
Phat = Pfit[0]*enthlin_max**2 + Pfit[1]*enthlin_max + Pfit[2]

## COMPARISON GRAPH
fig1, ax1 = plt.subplots(1,1,constrained_layout=True)
# ax1[0].plot(enthlin_CVD, Ahat_CVD, label='COVID-19')
# ax1[0].plot(enthlin, Ahat, color='tab:orange', label='2019')
# ax1[0].set_title('Average Daily Tonnage vs Average Daily Enthalpy')
# ax1[0].legend()
ax1.plot(enthlin_max_CVD, Ahat_Pk_CVD, label='COVID-19')
ax1.plot(enthlin_max, Phat, color='tab:orange', label='2019')
ax1.set_title('Peak Daily Tonnage vs Peak Daily Enthalpy')
ax1.legend()
# plt.show()

fig, ax4 = plt.subplots()
# ax4.scatter(MaxEnth_CVD, met_pk_CVD, facecolors='none', edgecolors='b')
# ax4.plot(enthlin_max, Phat, color='tab:orange', label='2019', zorder=1)
ax4.scatter(MaxEnth, tonPk, label='2019', facecolors='none', edgecolors='tab:orange', zorder=2)
# ax4.plot(enthlin_max_CVD, Ahat_Pk_CVD, label='COVID-19', zorder=3)
ax4.scatter(MaxEnth_CVD, met_pk_CVD, label='COVID-19', zorder=4)
ax4.plot(25, 5000, color='tab:orange', zorder = 1)
ax4.set_title("COVID to Normal Peak Tonnage Comparison")
ax4.set_xlabel("Max Daily Enthalpy")
ax4.set_ylabel("Peak Daily Tonnage")
# ax4.plot([20], [5000])
# ax4.legend((N, C), ('2019', 'COVID-19'))
ax4.legend()
plt.show()

# topPath = 'C:/Users/fm-student6/Desktop/US/Bldg Thermal Temp Correlations/'
# rows = [''] * len(MaxEnth)                     
# for j, e in enumerate(MaxEnth):
#     rows[j] = ','.join([rows[j], str(e), str(tonPk[j])])
# res = '\n'.join(rows)
# with open(topPath+'2019_chw.csv', 'w') as o:
#     o.write(res)

# rows = [''] * len(MaxEnth_CVD)                     
# for j, e in enumerate(MaxEnth_CVD):
#     rows[j] = ','.join([rows[j], str(e), str(met_pk_CVD[j])])
# res = '\n'.join(rows)
# with open(topPath+'covid_chw.csv', 'w') as o:
#     o.write(res)

## Average load vs avg enth
Afit_CVD = np.polyfit(enth_CVDw, met_CVDw, 2)
Ahat_CVD = Afit_CVD[0]*enthlin_CVD**2 + Afit_CVD[1]*enthlin_CVD + Afit_CVD[2]
Mean = np.mean(met_CVD)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Ahat_CVD])
sstot = sum([(i-Mean)**2 for i in met_CVD])
ssres = sum([(y - Ahat[i])**2 for i, y in enumerate(met_CVD)])
MET_r_sq_CVD = 1 - ssres/sstot

## peak load vs peak enth 
Afit_Pk_CVD = np.polyfit(MaxEnth_CVDw, met_pk_CVDw, 2)
Ahat_Pk_CVD = Afit_Pk_CVD[0]*enthlin_max_CVD**2 + Afit_Pk_CVD[1]*enthlin_max_CVD + Afit_Pk_CVD[2]
Mean = np.mean(met_pk_CVD)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Ahat_Pk_CVD])
sstot = sum([(i-Mean)**2 for i in met_pk_CVD])
ssres = sum([(y - Ahat_Pk_CVD[i])**2 for i, y in enumerate(met_pk_CVD)])
MET_pk_r_sq_CVD = 1 - ssres/sstot