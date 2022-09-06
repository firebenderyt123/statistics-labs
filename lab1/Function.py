from math import *
import numpy as np
import matplotlib.pyplot as plt

# np.longdouble - 18 signs after dot

class Function:

	N: int = 100
	x: []
	y: []
	x0: np.longdouble
	dx: np.longdouble

	def __init__(self, N = 100, x0 = 0, xn = 10):
		self.setParams(N, x0, xn)

	def setParams(self, N = 100, x0 = 0, xn = 10):
		# N - count of dots on graph
		# x0, xn - start and end of the function's range [x0, xn)
		self.N = N
		self.x0 = x0
		self.dx = (xn - x0) / N
		self.nullCoords()

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def nullCoords(self):
		self.x = np.zeros(self.N, np.longdouble)
		self.y = np.zeros(self.N, np.longdouble)

	def calc(self):
		self.x[0] = self.x0
		for n in range(1, self.N):
			self.x[n] = self.x[n-1] + self.dx
			self.y[n] = self.x[n]**2 * sin(self.x[n]) # here we input our function's formula

	def renderPlot(self, cols = 1, rows = 1, pos = 1, color = '--r'):
		plt.subplot(cols, rows, pos)
		plt.plot(self.x, self.y, color)

	def showPlot(self):
		plt.grid()
		plt.show()
		plt.clf() # clear plot

if __name__ == '__main__':
	func = Function(100, 0, 10)
	func.calc()
	func.renderPlot()
	func.showPlot()