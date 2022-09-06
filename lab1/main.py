from math import *
import numpy as np
from Function import Function

class MFunc(Function):

	def calc(self):
		self.x[0] = self.x0
		
		for n in range(1, self.N):
			self.x[n] = self.x[n-1] + self.dx
			if self.x[n] >= -pi and self.x[n] < 0:
				self.y[n] = -0.5
			elif self.x[n] >= 0 and self.x[n] < pi:
				self.y[n] = 0.5

class Furier(Function):

	def calc(self, iters = 100):
		# iters - count of furier iterations to calc function better 
		b = np.zeros(iters, np.longdouble)
		
		for k in range(1, iters):
			if k % 2 == 0: # even
				b[k] = 0
			else: # odd
				b[k] = 2 / pi / k

		self.x[0] = self.x0
		for n in range(1, self.N):
			self.x[n] = self.x[n-1] + self.dx
			for k in range(1, iters):
				self.y[n] += b[k] * sin(k * self.x[n])

func = MFunc(100, -pi, pi)
func.calc()
func.renderPlot(2, 2, 1, color = '--r') # 2 cols, 2 rows, pos 1 (top left)
func.renderPlot(2, 2, 2, color = '--r') # 2 cols, 2 rows, pos 2 (top right)
y1 = func.getY()

furier = Furier(100, -pi, pi)
furier.calc(5000)
furier.renderPlot(2, 2, 3, color = '-b') # 2 cols, 2 rows, pos 3 (bottom left)
furier.renderPlot(2, 2, 2, color = '-b') # 2 cols, 2 rows, pos 2 (top right)
y2 = furier.getY()

sumEps = 0
for i in range(len(y1)):
	sumEps += abs(abs(y1[i]) - abs(y2[i]))

print(sumEps / len(y1)) # average eps


furier.setParams(100, -4*pi, 4*pi)
furier.calc(5000)
furier.renderPlot(2, 2, 4, color = '-b') # 2 cols, 2 rows, pos 4 (bottom right)

func.showPlot()

# Results
# if use 100  iters for calc furier we get avg eps = 0.01307929..
# else if use 1000 iters for calc furier   avg eps = 0.00581806..
# else if use 10000 iters for calc furier  avg eps = 0.00508181..
# else if use 100000 iters for calc furier avg eps = 0.00500818..

# So optimal iters is 1000-10000, because can't get avg eps less than 0.005