import numpy as np
from numpy import exp, sqrt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import fsolve
from scipy import stats as stat

healthy_dataset = "./data/Hospital_12_visitorsTemp.csv"
flu_dataset = "./data/Hospital_12_FluTemp.csv"

edge = 37

def histogram(df, stat = 'density', kde = True):
	sns.histplot(df, stat = stat, kde = kde, element="step")
	plt.axvline(edge, 0, 1, color="k")
	plt.show()

def integral(start, stop, num, loc, scale):
	tN = np.linspace(start, stop, num)
	yTN = stat.norm.pdf(tN, loc = loc, scale = scale)
	return np.trapz(yTN, tN)

def func(x0, mTN, sTN, mTF, sTF): 
    F1 = 1/sqrt(2*np.pi*sTN)*exp(-(x0-mTN)**2/2/sTN)
    F2 = 1/sqrt(2*np.pi*sTF)*exp(-(x0-mTF)**2/2/sTF)
    y = F1 / F2 - (C21*P2)/(C12*P1)
    return y #F1/F2-(C21*P2)/(C12*P1) 


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

histogram([healthy_df['Healthy_T'], flu_df['Sick_T']])

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

Pr11 = integral(0.99*healthy_min, edge, 100, healthy_mean, healthy_std)
Pr12 = integral(edge, 1.1*sick_max, 100, healthy_mean, healthy_std)
Pr21 = integral(0.99*healthy_min, edge, 100, sick_mean, sick_std)
Pr22 = integral(edge, 1.1*sick_max, 100, sick_mean, sick_std)
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
print('The risk is  ' + str(R))
print('The apriory risk for 1st mistake is ' + str(C12 * P1))
print('The apriory risk for 2nd mistake is ' + str(C21 * P2), '\n')

x00 = fsolve(func, -1, args=(healthy_mean, healthy_std, sick_mean, sick_std))
print(healthy_mean, sick_mean)
print(x00)