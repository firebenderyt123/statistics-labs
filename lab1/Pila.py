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

class Furier(Function): # least square method
	
	def calc(self, iters = 100):
		# iters - count of furier iterations to calc function better 

		self.x[0] = self.x0
		for k in range(1, self.N):
			self.x[k] = self.x[k-1] + self.dx
			for n in range(1, iters):
				self.y[k] += (-1)**(n+1) / n * sin(n * self.x[k])
			self.y[k] *= 2


pila = Pila(100, -pi, pi)
pila.calc()
pila.renderPlot(2, 2, 1, color = '--r') # 2 cols, 2 rows, pos 1 (top left)
pila.renderPlot(2, 2, 2, color = '--r') # 2 cols, 2 rows, pos 2 (top right)
y1 = pila.getY()

furier = Furier(100, -pi, pi)
furier.calc(100)
furier.renderPlot(2, 2, 3, color = '-b') # 2 cols, 2 rows, pos 3 (bottom left)
furier.renderPlot(2, 2, 2, color = '-b') # 2 cols, 2 rows, pos 2 (top right)
y2 = furier.getY()

sumEps = 0
for i in range(len(y1)):
	sumEps += abs(abs(y1[i]) - abs(y2[i]))

print(sumEps / len(y1)) # average eps

furier.setParams(100, -4*pi, 4*pi)
furier.calc(100)
furier.renderPlot(2, 2, 4, color = '-b') # 2 cols, 2 rows, pos 4 (bottom right)

pila.showPlot()

# Results
# if use 100  iters for calc furier we get avg eps = 0.02538184..
# else if use 1000 iters for calc furier   avg eps = 0.00257003..
# else if use 10000 iters for calc furier  avg eps = 0.00025704..
# else if use 100000 iters for calc furier avg eps = 0.00002570..

# So here all depends of accuracy that we want to get.
# The more iterations the better the accuracy
