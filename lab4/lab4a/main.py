import numpy as np
from numpy import exp, sqrt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import fsolve
from scipy import stats

healthy_dataset = "./data/Hospital_12_visitorsTemp.csv"
flu_dataset = "./data/Hospital_12_FluTemp.csv"

edge = 37

def integral(start, stop, num, loc, scale):
	tN = np.linspace(start, stop, num)
	yTN = stats.norm.pdf(tN, loc = loc, scale = scale)
	return np.trapz(yTN, tN)

def func(x0, mTN, sTN, mTF, sTF, C21_P2, C12_P1):
    F1 = 1/sqrt(2*np.pi*sTN)*exp(-(x0-mTN)**2/2/sTN)
    F2 = 1/sqrt(2*np.pi*sTF)*exp(-(x0-mTF)**2/2/sTF)
    y = F1 / F2 - C21_P2/C12_P1
    # y = x0*x0-4
    return y


def normal_from_library(array, min, max, draw = True, label='normal'):
	dd, p = stats.norm.fit(array)
	x = np.linspace(min, max, 100)
	y = stats.norm.pdf(x, loc = dd, scale = p)
	if draw:
		sns.lineplot(x=x, y=y, label=label)
	return x, y, dd, p

def gamma_from_library(array, min, max, draw = True, label='gamma'):
	a, dd, p = stats.gamma.fit(array)
	x = np.linspace(min, max, 100)
	y = stats.gamma.pdf(x, a = a, loc = dd, scale = p)
	if draw:
		sns.lineplot(x=x, y=y, label=label)
	return x, y, a, dd, p

def rayleigh_from_library(array, min, max, draw = True, label='rayleigh'):
	dd, p = stats.rayleigh.fit(array)
	x = np.linspace(min, max, 100)
	y = stats.rayleigh.pdf(x, dd, p)
	if draw:
		sns.lineplot(x=x, y=y, label=label)
	return x, y, dd, p

def chisquare_from_library(array, min, max, draw = True, label='chisquare'):
	df, dd, p = stats.chi2.fit(array)
	x = np.linspace(min, max, 100)
	y = stats.chi2.pdf(x, df, loc = dd, scale = p)
	if draw:
		sns.lineplot(x=x, y=y, label=label)
	return x, y, df, dd, p


healthy_df = pd.read_csv(healthy_dataset, sep = ";")
healthy_df = healthy_df.rename(columns = {
	"Temp": "Healthy_T"
})

flu_df = pd.read_csv(flu_dataset, sep = ";")
flu_df = flu_df.rename(columns = {
	"Temp": "Sick_T"
})

print('Healthy:', healthy_df.head(), '\n')
print(healthy_df.describe(), '\n\n')
print('Sick:', flu_df.head(), '\n')
print(flu_df.describe(), '\n\n')

N_H = len(healthy_df['Healthy_T'])
N_S = len(flu_df['Sick_T'])
k_H = round(N_H**0.5)
k_S = round(N_S**0.5)
histH, bH = np.histogram(healthy_df['Healthy_T'], k_H, density = True) 
histS, bS = np.histogram(flu_df['Sick_T'], k_S, density = True) 


sns.histplot(
	healthy_df['Healthy_T'],
	bins = bH,
	stat = 'density',
	element="step"
)
sns.histplot(
	flu_df['Sick_T'],
	bins = bS,
	stat = 'density',
	element="step"
)
plt.axvline(edge, 0, 1, color="k")

'''
температура тіла менша за 37оС – не хвора людина;
температура тіла вища  за 37оС – хвора людина. 

Pr11 та Pr22  –  правильні  рішення
Pr12, Pr21  –  помилкова тривога та пропуск дефекту відповідно
'''

healthy_mean = healthy_df['Healthy_T'].mean()
healthy_std = healthy_df['Healthy_T'].std()
healthy_min = healthy_df['Healthy_T'].min()
healthy_max = healthy_df['Healthy_T'].max()

sick_mean = flu_df['Sick_T'].mean()
sick_std = flu_df['Sick_T'].std()
sick_min = flu_df['Sick_T'].min()
sick_max = flu_df['Sick_T'].max()


H_x, H_y, Hn_dd, Hn_p = normal_from_library(
	array = healthy_df['Healthy_T'],
	min = healthy_min,
	max = healthy_max
)
H_x, H_y, Hg_a, Hg_dd, Hg_p = gamma_from_library(
	array = healthy_df['Healthy_T'],
	min = healthy_min,
	max = healthy_max
)
H_x, H_y, Hr_dd, Hr_p = rayleigh_from_library(
	array = healthy_df['Healthy_T'],
	min = healthy_min,
	max = healthy_max
)
H_x, H_y, Sc_df, Hc_dd, Hc_p = chisquare_from_library(
	array = healthy_df['Healthy_T'],
	min = healthy_min,
	max = healthy_max
)

S_x, S_y, Sn_dd, Sn_p = normal_from_library(
	array = flu_df['Sick_T'],
	min = sick_min,
	max = sick_max
)
S_x, S_y, Sg_a, Sg_dd, Sg_p = gamma_from_library(
	array = flu_df['Sick_T'],
	min = sick_min,
	max = sick_max
)
S_x, S_y, Sr_dd, Sr_p = rayleigh_from_library(
	array = flu_df['Sick_T'],
	min = sick_min,
	max = sick_max
)
S_x, S_y, Sc_df, Sc_dd, Sc_p = chisquare_from_library(
	array = flu_df['Sick_T'],
	min = sick_min,
	max = sick_max
)

'''
Самое адекватное было норм распред по этому вот так вот дальше
'''

Pr11 = integral(0.99*healthy_min, edge, 100, Hn_dd, Hn_p)
Pr12 = integral(edge, 1.1*sick_max, 100, Hn_dd, Hn_p)
Pr21 = integral(0.99*healthy_min, edge, 100, Sn_dd, Sn_p)
Pr22 = integral(edge, 1.1*sick_max, 100, Sn_dd, Sn_p)
print('Probablity of correct decision for healthy person is '+ str(Pr11)) 
print('Probablity of the mistake of 1st type "the healthy person with high temperature" is  '+ 
str(Pr12)) 
print('Probablity of correct decision for ill person is  '+ str(Pr22)) 
print('Probablity of the mistake of 2nd type "the ill person with low temperature" is  '+ str(Pr21))
print(Pr11 + Pr12, Pr21 + Pr22, '\n')


'''
 	!!! NEED TO BE CHECKED !!!
'''

C12 = 40  #  the cost of the mistake of 1st type 
C21 = 40 #  the cost of the mistake of 2nd type 
 
P2 = 0.1
P1 = 0.21
R = C12 * P1 * Pr12 + C21 * P2 * Pr21
R2 = C12 * P2 * Pr12 + C21 * P1 * Pr21
print('The risk is R2 ' + str(R2))
print('The risk is  ' + str(R))
print('The apriory risk for 1st mistake is ' + str(C12 * P1))
print('The apriory risk for 2nd mistake is ' + str(C21 * P2), '\n')

x00 = fsolve(func, 36.2, args=(Hn_dd, Hn_p, Sn_dd, Sn_p, C21 * P2, C12 * P1))
print(healthy_mean, sick_mean)
print(x00)

plt.show()