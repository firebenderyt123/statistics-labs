# Part 1

from math import *
import numpy as np
import matplotlib.pyplot as plt

class Analysis:

	_N = 1000
	_D = np.array([900, 100]) # исправный подшипник, неисправный подшипник

	_Ki = np.zeros(3, dtype='O') #input data

	_conditions = np.array(['good', 'bad']) # good bad types

	# K1 - вибрация
	# K11 - вибрация в диапазоне 0.25-0.5
	# K12 - вибрация в диапазоне 0.5-0.75
	# K13 - вибрация в диапазоне > 0.75

	_K1_states = np.array([
		[0.25, 0.5],
		[0.5, 0.75],
		[0.75, float('inf')]
	])

	_PrK1 = np.array([
		np.array([ # good
			0.7,
			0.2,
			0.1
		]),
		np.array([ # bad
			0.05,
			0.15,
			0.8
		])
	])


	# K2 - температура
	# K21 - температура в диапазоне 50-70 С
	# K22 - температура в диапазоне 70-90 С
	# K23 - температура в диапазоне > 90 С

	_K2_states = np.array([
		[50, 70],
		[70, 90],
		[90, float('inf')]
	])

	_PrK2 = np.array([
		np.array([ # good
			0.8,
			0.1,
			0.1
		]),
		np.array([ # bad
			0.07,
			0.08,
			0.85
		])
	])

	# K3 - загрязнение смазки
	# K31 - в пределах нормы
	# K32 – повышенное

	_K3_states = np.array(['normal', 'high'])

	_PrK3 = np.array([
		np.array([ # good
			0.9,
			0.1
		]),
		np.array([ # bad
			0.3,
			0.7
		])
	])

	_result = None

	def __init__(self, K1, K2, K3):
		self._Ki[0] = K1
		self._Ki[1] = K2
		self._Ki[2] = K3

	def getResults(self):
		return self._result

	def _getPrK(self, index, conditionId):
		if (index == 0):
			return self._getPrK1(self._Ki[index], conditionId)
		elif (index == 1):
			return self._getPrK2(self._Ki[index], conditionId)
		elif (index == 2):
			return self._getPrK3(self._Ki[index], conditionId)

	def _getPrK1(self, K1, conditionId):
		for i in range(np.size(self._K1_states)):
			if (K1 >= self._K1_states[i][0] and K1 < self._K1_states[i][1]):
				return self._PrK1[conditionId][i]

	def _getPrK2(self, K2, conditionId):
		for i in range(np.size(self._K2_states)):
			if (K2 >= self._K2_states[i][0] and K2 < self._K2_states[i][1]):
				return self._PrK2[conditionId][i]

	def _getPrK3(self, K3, conditionId):
		for i in range(np.size(self._K3_states)):
			if (K3 == self._K3_states[i]):
				return self._PrK3[conditionId][i]

	def calc(self):
		PrK_D = np.ones(np.size(self._conditions))
		for i in range(np.size(self._conditions)):
			for j in range(np.size(self._Ki)):
				PrK_D[i] *= self._getPrK(j, i)

		PrD = np.zeros(np.size(self._conditions))
		for i in range(np.size(PrD)):
			PrD[i] = self._D[i] / self._N

		denominator = 0
		for j in range(np.size(self._conditions)):
			denominator += PrD[j] * PrK_D[j]

		PrD_K = np.zeros(np.size(self._conditions))
		for i in range(np.size(PrD)):
			PrD_K[i] = PrD[i] * PrK_D[i] / denominator

		self._result = PrD_K
		return self._result

	def printInfo(self):
		print('--------')
		print('Дано: ')
		for i in range(np.size(self._K1_states)):
			if (self._Ki[0] >= self._K1_states[i][0] and self._Ki[0] < self._K1_states[i][1]):
				print(f' вибрации в диапазоне {self._K1_states[i][0]}-{self._K1_states[i][1]} (признак K1[{i}])')
				break
		for i in range(np.size(self._K2_states)):
			if (self._Ki[1] >= self._K2_states[i][0] and self._Ki[1] < self._K2_states[i][1]):
				print(f' температуре в диапазоне {self._K2_states[i][0]}-{self._K2_states[i][1]} (признак K2[{i}])')
				break
		for i in range(np.size(self._K3_states)):
			if (self._Ki[2] == self._K3_states[i]):
				print(f' загрязнение смазки: "{self._K3_states[i]}" (признак K3[{i}])')
				break

	def printResult(self):
		print('--------')
		print(f'Вероятность исправного состояния (D1):   {round(self._result[0]*100, 2)} %')
		print(f'Вероятность неисправного состояния (D2): {round(self._result[1]*100, 2)} %')

	def drawPlot(self, results):
		x = [1, 2]
		y = [round(results[0]*100, 2), round(results[1]*100,2)] 
		 
		plt.bar(x, y)
		plt.rcParams.update({'text.color': "w"})
		plt.text(x[0], y[0]/2, 'Исправное состояние', ha='center') 
		plt.text(x[0], y[0]/3, y[0],ha='center') 
		plt.text(x[1], y[1]/2, 'Неисправное состояние', ha='center') 
		plt.text(x[1], y[1]/3, y[1], ha='center')
		plt.xlabel('Диагнозы') 
		plt.ylabel('Вероятность диагноза') 
		plt.show()

if __name__ == '__main__':
	anal = Analysis(0.6, 80, 'high')
	anal.calc()
	anal.printInfo()
	anal.printResult()
	anal.drawPlot(anal.getResults())