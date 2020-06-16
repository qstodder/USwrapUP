
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


xls = pd.ExcelFile('C:/Users/fm-student6/Desktop/US/Bldg Thermal Temp Correlations/Correllation Data - Sum.xlsx')
data = xls.parse(sheet_name = "All")
temp = data['avgTemp']
hum = data['avgHum']
htw = data['HTWtot']
chw = data['CHWtot']
elec = data.elecTot

# get enthalpy
enth = []
for i in range(len(temp)):
    t = temp.iloc[i] + 459.67
    h = hum.iloc[i]/100
    E = psy.state("DBT", t, "RH", h, 14.7)
    enth.append(E[1])


# quadratic regressions
enth_w = np.append(np.linspace(0,15,50).tolist(), enth)
chw_w = np.append(np.linspace(min(chw), min(chw), 50).tolist(), chw)
Efit = np.polyfit(enth_w, chw_w, 2)
# enth_lin = np.linspace(min(enth), max(enth), len(enth))
enth_lin = np.linspace(10, 50, len(chw_w))
fit = Efit[0]*enth_lin**2 + Efit[1]*enth_lin + Efit[2]
CMean = np.mean(chw_w)
ssreg = sum([(Chat_i - CMean)**2 for Chat_i in fit])
sstot = sum([(Ci-CMean)**2 for Ci in chw_w])
r_sq = ssreg/sstot
print("chw " + str(r_sq))

temp_w = np.append(temp, np.linspace(79, 100, 100).tolist())
htw_w = np.append(htw, np.linspace(min(htw), min(htw), 100).tolist())
Hfit = np.polyfit(temp_w, htw_w, 2)
# H_lin = np.linspace(min(temp), max(temp), 200)
H_lin = np.linspace(40, 87, len(htw_w))
H_hat = Hfit[0]*H_lin**2 + Hfit[1]*H_lin + Hfit[2]
HMean = np.mean(htw_w)
ssreg = sum([(Hhat_i - HMean)**2 for Hhat_i in H_hat])
sstot = sum([(Hi-HMean)**2 for Hi in htw_w])
r_sq = ssreg/sstot
print("htw " + str(r_sq))

enth_wh = np.append(enth, np.linspace(37,45,100).tolist())
EHfit = np.polyfit(enth_wh, htw_w, 2)
H_linE = np.linspace(10, 40, 200)
H_hatE = EHfit[0]*H_linE**2 + EHfit[1]*H_linE + EHfit[2]



print(elec[temp == min(temp)])
minElec = min(elec[temp==min(temp)])

temp_we = np.append(np.linspace(40,50,100).tolist(), temp)
elec_w = np.append(np.linspace(minElec, minElec, 100).tolist(), elec)
ETfit = np.polyfit(temp_we, elec_w, 2)
E_lin = np.linspace(40, 80, len(elec_w))
Ehat = ETfit[0]*E_lin**2 + ETfit[1]*E_lin + ETfit[2]
EMean = np.mean(elec_w)
ssreg = sum([(Ehat_i - EMean)**2 for Ehat_i in Ehat])
sstot = sum([(ei-EMean)**2 for ei in elec_w])
r_sq = ssreg/sstot

print(ETfit[2])
print(ETfit[1])
print(ETfit[0])
print(min(elec))
print(max(elec))
print(r_sq)


# log fits
Elog = np.polyfit(np.log(enth), chw, 1)
Elfit = Elog[0]*np.log(enth_lin) + Elog[1]

Hlog = np.polyfit(np.log(temp), htw, 1)
Hlfit = Hlog[0]*np.log(H_lin) + Hlog[1]

fig1, axs = plt.subplots(3,1)
axs[0].scatter(temp, chw)
axs[1] = plt.subplot(3,1,2)
axs[1].scatter(enth, chw)
axs[1].plot(enth_lin, fit, color='red')
# axs[1].plot(enth_lin, Elfit, color='green')
axs[2] = plt.subplot(3,1,3)
axs[2].scatter(temp*hum, chw)
# fig1.suptitle('CHW vs Temp and/or Hum')
axs[0].set_title('CHW vs temp')
axs[1].set_title('CHW vs enthalpy')
axs[2].set_title('CHW vs temp*hum')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

fig2, axs1 = plt.subplots(3,1,constrained_layout=True)
axs1[0].scatter(temp, htw)
axs1[0].plot(H_lin, H_hat, color='red')
# axs1[0].plot(H_lin, Hlfit, color='green')
axs1[1] = plt.subplot(3,1,2)
axs1[1].scatter(enth, htw)
axs1[1].plot(H_linE, H_hatE, color='red')
axs1[2] = plt.subplot(3,1,3)
axs1[2].scatter(temp*hum, htw)
# fig2.suptitle('HTW vs Temp and/or Hum')
axs1[0].set_title('HTW vs temp')
axs1[1].set_title('HTW vs enthalpy')
axs1[2].set_title('HTW vs temp*hum')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

fig3, axs2 = plt.subplots(3,1,constrained_layout=True)
axs2[0].scatter(temp, elec)
axs2[0].plot(E_lin, Ehat, color='red')
# axs2[0].plot(H_lin, Hlfit, color='green')
axs2[1] = plt.subplot(3,1,2)
axs2[1].scatter(enth, elec)
# axs2[1].plot(H_linE, H_hatE, color='red')
axs2[2] = plt.subplot(3,1,3)
axs2[2].scatter(temp*hum, elec)
# fig3.suptitle('elec vs Temp and/or Hum')
axs2[0].set_title('elec vs temp')
axs2[1].set_title('elec vs enthalpy')
axs2[2].set_title('elec vs temp*hum')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()


