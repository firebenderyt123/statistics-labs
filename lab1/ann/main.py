from math import *
import numpy as np
import matplotlib.pyplot as plt
N=1000
x=np.zeros(N,float)
y=np.zeros(N,float)
x0=-pi
xn=pi
dx=(xn-x0)/N
x[0]=x0
for n in range(1, N):
	x[n] = x[n-1] + dx
	if x[n] >= -pi and x[n] <= pi:
		y[n] = x[n]
plt.plot(x,y,'-b')
# for n in range(1,N):
#     x[n]=x[n-1]+dx
#     if ((x[n]>-pi) and (x[n]<=pi)):
#         y[n]= x[n]
#     elif ((x[n]>pi) and (x[n]<2*pi)):
#         y[n]= x[n-1]
#     elif ((x[n]>2*pi) and (x[n]<3*pi)):
#         y[n]= x[n]
#     elif ((x[n]>3*pi) and (x[n]<4*pi)):
#         y[n]= x[n]
Nf=N
b=np.zeros(Nf,float)
z=np.zeros(Nf,float)
# to find Fourie coeff
# for k in range(1,Nf):
#     if k % 2 == 0: # even
#         b[k]=-2/k
#     else: # odd
#         b[k]=2/k
# for n in range(1,N):
#     z[n]=b[1]*sin(x[n])
#     for k in range(2,Nf):
#         z[n]=z[n]+b[k]*sin(k*x[n])
iters = 100
x=np.zeros(N,float)
y=np.zeros(N,float)
x[0]=x0
for k in range(1, N):
	x[k] = x[k-1] + dx
	for n in range(1, iters):
		y[k] += (-1)**(n+1) / n * sin(n * x[k])
	y[k] *= 2
plt.plot(x,y,'-r')
plt.grid()
plt.show()