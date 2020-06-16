import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from psypy import psyIP as psy

f = 'CHWGen_COVID.xlsx'
filePath = 'C:/Users/fm-student6/Desktop/US/Bldg Thermal Temp Correlations/'
xls = pd.ExcelFile(filePath+f)

data = xls.parse(sheet_name = 'CHWGen_COVID')
met = data.Met
ion = data.ionEEM
bldg = data.BldgLoad
met_pk = data.MetPk
ion_pk = data.ionPk
bldg_pk = data.bldgPk
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

MaxEnth = []
for i in range(44):
    m = max(enth_hr[i*24:(i*24+23)])
    MaxEnth.append(m)

enthlin = np.linspace(min(enth), max(enth), len(met))  
enthlin_max = np.linspace(min(MaxEnth), max(MaxEnth), len(met_pk))      

## Average load vs avg enth
Afit = np.polyfit(enth, met, 2)
Ahat = Afit[0]*enthlin**2 + Afit[1]*enthlin + Afit[2]
Mean = np.mean(met)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Ahat])
sstot = sum([(i-Mean)**2 for i in met])
ssres = sum([(y - Ahat[i])**2 for i, y in enumerate(met)])
MET_r_sq = 1 - ssres/sstot

Pfit = np.polyfit(enth, ion, 2)
Phat = Pfit[0]*enthlin**2 + Pfit[1]*enthlin + Pfit[2]
Mean = np.mean(ion)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Phat])
sstot = sum([(i-Mean)**2 for i in ion])
ssres = sum([(y - Phat[i])**2 for i, y in enumerate(ion)])
ION_r_sq = 1- ssres/sstot

Sfit = np.polyfit(enth, bldg, 2)
Shat = Sfit[0]*enthlin**2 + Sfit[1]*enthlin + Sfit[2]
Mean = np.mean(bldg)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Shat])
sstot = sum([(i-Mean)**2 for i in bldg])
ssres = sum([(y - Shat[i])**2 for i, y in enumerate(bldg)])
BLDG_r_sq = 1- ssres/sstot

## peak load vs peak enth
Afit_Pk = np.polyfit(MaxEnth, met_pk, 2)
Ahat_Pk = Afit_Pk[0]*enthlin_max**2 + Afit_Pk[1]*enthlin_max + Afit_Pk[2]
Mean = np.mean(met_pk)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Ahat_Pk])
sstot = sum([(i-Mean)**2 for i in met_pk])
ssres = sum([(y - Ahat_Pk[i])**2 for i, y in enumerate(met_pk)])
MET_pk_r_sq = 1 - ssres/sstot

Pfit_Pk = np.polyfit(MaxEnth, ion_pk, 2)
Phat_Pk = Pfit_Pk[0]*enthlin_max**2 + Pfit_Pk[1]*enthlin_max + Pfit_Pk[2]
Mean = np.mean(ion_pk)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Phat_Pk])
sstot = sum([(i-Mean)**2 for i in ion_pk])
ssres = sum([(y - Phat_Pk[i])**2 for i, y in enumerate(ion_pk)])
ION_pk_r_sq = 1- ssres/sstot

Sfit_Pk = np.polyfit(MaxEnth, bldg_pk, 2)
Shat_Pk = Sfit_Pk[0]*enthlin_max**2 + Sfit_Pk[1]*enthlin_max + Sfit_Pk[2]
Mean = np.mean(bldg_pk)
ssreg = sum([(hat_i - Mean)**2 for hat_i in Shat_Pk])
sstot = sum([(i-Mean)**2 for i in bldg_pk])
ssres = sum([(y - Shat_Pk[i])**2 for i, y in enumerate(bldg_pk)])
BLDG_pk_r_sq = 1- ssres/sstot

fig, ax = plt.subplots(3,1,constrained_layout=True)
ax[0].scatter(enth, met)
ax[0].plot(enthlin, Ahat, color='red')
ax[0].set_title('Metsys Tonnage')
ax[1].scatter(enth, ion)
ax[1].plot(enthlin, Phat, color='red')
ax[1].set_title('ionEEM Tonnage')
ax[2].scatter(enth, bldg)
ax[2].plot(enthlin, Shat, color='red')
ax[2].set_title('Bldg Load Tonnage [ton-hr]')

fig1, ax1 = plt.subplots(3,1,constrained_layout=True)
ax1[0].scatter(MaxEnth, met_pk)
ax1[0].plot(enthlin_max, Ahat_Pk, color='red')
ax1[0].set_title('Metsys Peak Tonnage')
ax1[1].scatter(MaxEnth, ion_pk)
ax1[1].plot(enthlin_max, Phat_Pk, color='red')
ax1[1].set_title('ionEEM Peak Tonnage')
ax1[2].scatter(MaxEnth, bldg_pk)
ax1[2].plot(enthlin_max, Shat_Pk, color='red')
ax1[2].set_title('Bldg Load Peak Tonnage [ton-hr]')


# print(Afit[2])
# print(Afit[1])
# print(Afit[0])
print(MET_r_sq)

# print(Pfit[2])
# print(Pfit[1])
# print(Pfit[0])
print(ION_r_sq)

# print(Sfit[2])
# print(Sfit[1])
# print(Sfit[0])
print(BLDG_r_sq)

# print(max(temp))

# print(Afit[2])
# print(Afit[1])
# print(Afit[0])
print(MET_pk_r_sq)

# print(Pfit[2])
# print(Pfit[1])
# print(Pfit[0])
print(ION_pk_r_sq)

# print(Sfit[2])
# print(Sfit[1])
# print(Sfit[0])
print(BLDG_pk_r_sq)

## COMPARISON GRAPHS - different load sources
fig2, ax2 = plt.subplots(2,1,constrained_layout=True)
ax2[1].plot(enthlin_max, Ahat_Pk, label='CUP Metasys')
ax2[1].plot(enthlin_max, Phat_Pk, label='ionEEM')
ax2[1].plot(enthlin_max, Shat_Pk, label='Bldg Load')
ax2[1].set_title('Souce Comparison: Peak Tonnage')
ax2[1].set_xlabel("Max Daily Enthalpy")
ax2[1].set_ylabel("Peak Daily Tonnage")
ax2[1].legend()
ax2[0].set_xlabel("Avg Daily Enthalpy")
ax2[0].set_ylabel("Avg Daily Tonnage")
ax2[0].set_title('Souce Comparison: Average Tonnage')
ax2[0].plot(enthlin, Ahat, label='CUP Metasys')
ax2[0].plot(enthlin, Phat, label='ionEEM')
ax2[0].plot(enthlin, Shat, label='Bldg Load')
ax2[0].legend()



plt.show()