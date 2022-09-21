import matplotlib.pyplot as plt
import numpy as np

class Diagnoser:

	_diagnoses = ['Aскаридоз', 'Гепатит', 'Камни в почках']

	# contains coefs that calc from statistics' data
	_ascariasis = np.zeros((6,4))
	_hepatitis  = np.zeros((6,4))
	_stones     = np.zeros((6,4))

	_counts = [
		0, # ascariasis
		0, # hepatitis
		0  # stones 
	]
	_total_pacients = 0

	# params (replace if else to loop)
	_age = [
		[0, 20],
		[20, 40],
		[40, 60],
		[60, float('inf')]
	]
	_nausea = ['no', 'yes']
	_yellowishness = ['eye', 'skin', 'no']
	_right_side_pain = ['no', 'yes']
	_liver_enlargement = ['no', 'yes']
	_appetite = ['no', 'yes']


	def __init__(self):
		self.calcStatistics()

	# load databases
	def _loadAscariasis(self):
		with open("db/Ascariasis_var2.csv", "r") as f:
			return f.readlines()

	def _loadHepatitis(self):
		with open("db/Hepatitis_var2.csv", "r") as f:
			return f.readlines()

	def _loadStones(self):
		with open("db/Stones_var2.csv", "r") as f:
			return f.readlines()


	#calc statistics data
	def calcStatistics(self):
		self._statisticsAscariasis()
		self._statisticsHepatitis()
		self._statisticsStones()
		for i in range(len(self._counts)):
			self._total_pacients += self._counts[i]

	def getStatistics(self):
		return [
			self._ascariasis,
			self._hepatitis,
			self._stones
		]

	def _statisticsAscariasis(self):
		lines = self._loadAscariasis()
		for i in range(1, len(lines)):
			line = lines[i].replace('\n', '').split(';')
			
			for i, age in enumerate(self._age):
				if (int(line[0]) >= age[0] and int(line[0]) < age[1]):
					self._ascariasis[0,i] += 1
					break

			for i, nausea in enumerate(self._nausea):
				if (line[1] == nausea):
					self._ascariasis[1,i] += 1
					break

			for i, yellowishness in enumerate(self._yellowishness):
				if (line[2] == yellowishness):
					self._ascariasis[2,i] += 1
					break

			for i, right_side_pain in enumerate(self._right_side_pain):
				if (line[3] == right_side_pain):
					self._ascariasis[3,i] += 1
					break

			for i, liver_enlargement in enumerate(self._liver_enlargement):
				if (line[4] == liver_enlargement):
					self._ascariasis[4,i] += 1
					break

			for i, appetite in enumerate(self._appetite):
				if (line[5] == appetite):
					self._ascariasis[5,i] += 1
					break
		self._counts[0] = len(lines)-1
		self._ascariasis /= len(lines)-1

	def _statisticsHepatitis(self):
		lines = self._loadHepatitis()
		for i in range(1, len(lines)):
			line = lines[i].replace('\n', '').split(';')
			
			for i, age in enumerate(self._age):
				if (int(line[0]) >= age[0] and int(line[0]) < age[1]):
					self._hepatitis[0,i] += 1
					break

			for i, nausea in enumerate(self._nausea):
				if (line[1] == nausea):
					self._hepatitis[1,i] += 1

			for i, yellowishness in enumerate(self._yellowishness):
				if (line[2] == yellowishness):
					self._hepatitis[2,i] += 1
					break

			for i, right_side_pain in enumerate(self._right_side_pain):
				if (line[3] == right_side_pain):
					self._hepatitis[3,i] += 1
					break

			for i, liver_enlargement in enumerate(self._liver_enlargement):
				if (line[4] == liver_enlargement):
					self._hepatitis[4,i] += 1
					break

			for i, appetite in enumerate(self._appetite):
				if (line[5] == appetite):
					self._hepatitis[5,i] += 1
					break
		self._counts[1] = len(lines)-1
		self._hepatitis /= len(lines)-1

	def _statisticsStones(self):
		lines = self._loadStones()
		for i in range(1, len(lines)):
			line = lines[i].replace('\n', '').split(';')
			
			for i, age in enumerate(self._age):
				if (int(line[0]) >= age[0] and int(line[0]) < age[1]):
					self._stones[0,i] += 1
					break

			for i, nausea in enumerate(self._nausea):
				if (line[1] == nausea):
					self._stones[1,i] += 1
					break

			for i, yellowishness in enumerate(self._yellowishness):
				if (line[2] == yellowishness):
					self._stones[2,i] += 1
					break

			for i, right_side_pain in enumerate(self._right_side_pain):
				if (line[3] == right_side_pain):
					self._stones[3,i] += 1
					break

			for i, liver_enlargement in enumerate(self._liver_enlargement):
				if (line[4] == liver_enlargement):
					self._stones[4,i] += 1
					break

			for i, appetite in enumerate(self._appetite):
				if (line[5] == appetite):
					self._stones[5,i] += 1
					break
		self._counts[2] = len(lines)-1
		self._stones /= len(lines)-1

	# probabilities
	def getDiagnose(self, age, nausea, yellowishness,
	right_side_pain, liver_enlargement, appetite):
		PrK_D1 = 1 # ascariasis
		PrK_D2 = 1 # hepatitis
		PrK_D3 = 1 # stones

		for i, m_age in enumerate(self._age):
			if (age >= m_age[0] and age < m_age[1]):
				PrK_D1 *= self._ascariasis[0,i]
				PrK_D2 *= self._hepatitis[0,i]
				PrK_D3 *= self._stones[0,i]
				break

		for i, m_nausea in enumerate(self._nausea):
			if (nausea == m_nausea):
				PrK_D1 *= self._ascariasis[1,i]
				PrK_D2 *= self._hepatitis[1,i]
				PrK_D3 *= self._stones[1,i]
				break

		for i, m_yellowishness in enumerate(self._yellowishness):
			if (yellowishness == m_yellowishness):
				self._stones[2,i] += 1
				PrK_D1 *= self._ascariasis[2,i]
				PrK_D2 *= self._hepatitis[2,i]
				PrK_D3 *= self._stones[2,i]
				break

		for i, m_right_side_pain in enumerate(self._right_side_pain):
			if (right_side_pain == m_right_side_pain):
				self._stones[3,i] += 1
				PrK_D1 *= self._ascariasis[3,i]
				PrK_D2 *= self._hepatitis[3,i]
				PrK_D3 *= self._stones[3,i]
				break

		for i, m_liver_enlargement in enumerate(self._liver_enlargement):
			if (liver_enlargement == m_liver_enlargement):
				self._stones[4,i] += 1
				PrK_D1 *= self._ascariasis[4,i]
				PrK_D2 *= self._hepatitis[4,i]
				PrK_D3 *= self._stones[4,i]
				break

		for i, m_appetite in enumerate(self._appetite):
			if (appetite == m_appetite):
				self._stones[5,i] += 1
				PrK_D1 *= self._ascariasis[5,i]
				PrK_D2 *= self._hepatitis[5,i]
				PrK_D3 *= self._stones[5,i]
				break
		
		PrD1 = self._counts[0] / self._total_pacients
		PrD2 = self._counts[1] / self._total_pacients
		PrD3 = self._counts[2] / self._total_pacients
		# PrD1, PrD2, PrD3 = 1, 1, 1
		# print(PrD1, PrD2, PrD3)
		diagnoses = [
			PrK_D1 * PrD1 / (PrK_D1 * PrD1 + PrK_D2 * PrD2 + PrK_D3 * PrD3),
			PrK_D2 * PrD2 / (PrK_D1 * PrD1 + PrK_D2 * PrD2 + PrK_D3 * PrD3),
			PrK_D3 * PrD3 / (PrK_D1 * PrD1 + PrK_D2 * PrD2 + PrK_D3 * PrD3)
		]
		self.printDiagnose(diagnoses)
		return diagnoses

	def printDiagnose(self, results):
		max_res = np.argmax(results)
		print('\n\n-------- Диагноз --------')
		print(f'Диагноз: {self._diagnoses[max_res]} ({round(results[max_res] * 100, 2)}%)')
		print('\n-------- Вероятности болезней --------')
		for result in results:
			print(f'Диагноз: {result} ({round(result * 100, 2)}%)')
		print('\n')

	def drawPlot(self, diagnoses):
		x = []
		y = diagnoses

		for i in range(len(self._diagnoses)):
			x.append(i)

		plt.bar(x, y)
		for i, diagnose in enumerate(diagnoses):
			print(x[i], y[i], self._diagnoses[i], 'center')
			plt.text(x[i], y[i]/2, self._diagnoses[i], ha='center')
			plt.text(x[i], y[i]/3, str(round(diagnose * 100, 2)) + '%', ha='center')
		plt.xlabel('Диагнозы')
		plt.ylabel('Вероятность диагноза')
		plt.show()

if __name__ == '__main__':
	diagnoser = Diagnoser()
	statistics = diagnoser.getStatistics()
	print(statistics)
	diagnoses = diagnoser.getDiagnose(19, 'yes', 'skin', 'yes', 'yes', 'no')
	diagnoser.drawPlot(diagnoses)


	# check is data valid or not

	# for arr in statistics:
	# 	for arr_2 in arr:
	# 		result = 0
	# 		for elem in arr_2:
	# 			result += elem
	# 		print(result)
	#
	# data = 0
	# for i in diagnose:
	# 	data += i
	# print(data)