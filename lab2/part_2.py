from math import *
import numpy as np
import matplotlib.pyplot as plt
from Analysis import Analysis

class Modification(Analysis):

	_aprioriResult = None

	def getAprioriResults(self):
		return self._aprioriResult

	def aprioriCalc(self):
		PrK_D = np.ones(np.size(self._conditions))
		for i in range(np.size(self._conditions)):
			for j in range(np.size(self._Ki)):
				PrK_D[i] *= 1 / np.size(self._Ki)  # 1 of 3 params

		PrD = np.zeros(np.size(self._conditions))		
		for i in range(np.size(PrD)):
			PrD[i] = 1 / np.size(self._conditions) # good or bad

		denominator = 0
		for j in range(np.size(self._conditions)):
			denominator += PrD[j] * PrK_D[j]

		PrD_K = np.zeros(np.size(self._conditions))
		for i in range(np.size(PrD)):
			PrD_K[i] = PrD[i] * PrK_D[i] / denominator

		self._aprioriResult = PrD_K
		return self._aprioriResult

	def printAprioriResult(self):
		# When we have no data
		print('--------')
		print(f'Априорная вероятность исправного состояния (D1):   {round(self._aprioriResult[0]*100, 2)} %')
		print(f'Априорная вероятность неисправного состояния (D2): {round(self._aprioriResult[1]*100, 2)} %')

	def printProbabilityResult(self):
		# When we have some data
		print('--------')
		print(f'Условная вероятность исправного состояния (D1):   {round(self._result[0]*100, 2)} %')
		print(f'Условная вероятность неисправного состояния (D2): {round(self._result[1]*100, 2)} %')

	def drawPlot(self, results):
		plt.rcParams.update({'text.color': "w"})
		fig, ax = plt.subplots(1, 2)
		for i in range(len(results)):
			x = [1, 2]
			y = [round(results[i][0]*100, 2), round(results[i][1]*100,2)] 

			ax[i].bar(x, y)
			ax[i].text(x[0], y[0]/2, 'Исправное состояние', ha='center') 
			ax[i].text(x[0], y[0]/3, y[0],ha='center') 
			ax[i].text(x[1], y[1]/2, 'Неисправное состояние', ha='center') 
			ax[i].text(x[1], y[1]/3, y[1], ha='center')
			ax[i].set_xlabel('Диагнозы')
			ax[i].set_ylabel('Вероятность диагноза')
		plt.show()

if __name__ == '__main__':
	modification = Modification(0.8, 80, 'high')
	modification.aprioriCalc()
	modification.calc()
	modification.printInfo()
	modification.printAprioriResult()
	modification.printProbabilityResult()
	modification.drawPlot([modification.getAprioriResults(), modification.getResults()])