from math import *
import numpy as np
from Function import Function

class Pila(Function):

	def calc(self):
		self.x[0] = self.x0
		
		for n in range(1, self.N):
			self.x[n] = self.x[n-1] + self.dx
			if self.x[n] >= -pi and self.x[n] <= pi:
				self.y[n] = self.x[n]

class LSM(Function): # least square method

	def calc(self, y):
		sumX, sumY, sumX2, sumXY = 0, 0, 0, 0

		self.x[0] = self.x0
		for n in range(1, self.N):
			self.x[n] = self.x[n-1] + self.dx

		for n in range(1, self.N):
			sumX += self.x[n]
			sumY += y[n]
			sumXY+= self.x[n] * y[n]
			sumX2+= self.x[n]**2

		a = (self.N * sumXY - sumX * sumY) / (self.N * sumX2 - sumX**2)
		b = sumY - a * sumX / self.N

		for n in range(1, self.N):
			self.y[n] = a * self.x[n] + b
			

pila = Pila(100, -pi, pi)
pila.calc()
pila.renderPlot(2, 2, 1, color = '--r') # 2 cols, 2 rows, pos 1 (top left)
pila.renderPlot(2, 2, 2, color = '--r') # 2 cols, 2 rows, pos 2 (top right)
x1 = pila.getX()
y1 = pila.getY()

lsm = LSM(100, -pi, pi)
lsm.calc(y1)
lsm.renderPlot(2, 2, 3, color = '-b') # 2 cols, 2 rows, pos 3 (bottom left)
lsm.renderPlot(2, 2, 2, color = '-b') # 2 cols, 2 rows, pos 2 (top right)
y2 = lsm.getY()

sumEps = 0
for i in range(len(y1)):
	sumEps += abs(abs(y1[i]) - abs(y2[i]))

print(sumEps / len(y1)) # average eps


lsm.setParams(100, -4*pi, 4*pi)
lsm.calc(y1)
lsm.renderPlot(2, 2, 4, color = '-b') # 2 cols, 2 rows, pos 4 (bottom right)

pila.showPlot()