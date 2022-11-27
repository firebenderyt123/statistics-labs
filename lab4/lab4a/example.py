from math import * 
import numpy as np 
import matplotlib.pyplot as plt 
import scipy.stats as stat 
 
# Open the file with read only permit 
text_file = open("data/Example.csv", "r")
lin = text_file.readlines() 
text_file.close() 
 
D1Size=len(lin)-1 
DataTemp=np.zeros((D1Size,3)) 
Age=np.zeros((D1Size,1)) 
 
for i in range(1,D1Size): 
	data=lin[i].split(';') 
	Age[i]=int(data[1]) 
	print(data) 
	DataTemp[i,1] = float(data[2])
	DataTemp[i,2] = float(data[3])

DataTempN=sorted(DataTemp[:,1]) 
DataTempN[0]=DataTempN[1] 
 
MeanTempN=np.mean(DataTempN) 
stdTempN=np.std(DataTempN) 
TN_min=min(DataTempN) 
TN_max=max(DataTempN) 
 
print('Average temperature of healthy person h is  '+str(MeanTempN)) 
print('with standard deviation   '+str(stdTempN)) 
print('All the data on normal temperature is between  '+str(TN_min)+' and  '+ str(TN_max)) 

histT,bT=np.histogram(DataTempN,8,density=True) 
plt.hist(DataTempN,bins=bT,density=True) 
plt.show()

mTN,sTN = stat.norm.fit(DataTempN) 
mTF,sTF = stat.norm.fit(DataTempF) 
 
xx=np.linspace(0.99*TN_min,1.1*TF_max,100) 
yTN=stat.norm.pdf(xx,loc=mTN,scale=sTN) 
yTF=stat.norm.pdf(xx,loc=mTF,scale=sTF) 
 
plt.plot(xx,yTN,'-b') 
plt.plot(xx,yTF,'-r') 
plt.show() 

