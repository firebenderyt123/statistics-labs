import pandas as pd
import numpy as np
from scipy import stats
from scipy import special as spec
import seaborn as sns
import matplotlib.pyplot as plt

# def normal_approximation(min, max, Mx, Sx, ax = plt, draw = True):
# 	x = np.linspace(min, max, 100)
# 	y = (1 / (np.sqrt(2 * np.pi) * Sx)) * np.exp(-0.5 * (1 / Sx * (x - Mx))**2)
# 	if draw:
# 		sns.lineplot(x=x, y=y, ax=ax)
# 	return x, y

# def gamma_approximation(array, min, max, ax = plt, draw = True):
# 	a, dd, p = stats.gamma.fit(array)
# 	g = spec.gamma(a)
# 	x = np.linspace(min, max, 100)
# 	y = 1 / g / p**a * (x - dd)**(a-1) * np.exp(-(x-dd)/p)
# 	if draw:
# 		sns.lineplot(x=x, y=y, ax=ax)
# 	return x, y, a, dd, p


def normal_from_library(array, min, max, ax = plt, draw = True):
	dd, p = stats.norm.fit(array)
	x = np.linspace(min, max, 100)
	y = stats.norm.pdf(x, loc = dd, scale = p)
	if draw:
		sns.lineplot(x=x, y=y, ax=ax)
	return x, y, dd, p

def gamma_from_library(array, min, max, ax = plt, draw = True):
	a, dd, p = stats.gamma.fit(array)
	x = np.linspace(min, max, 100)
	y = stats.gamma.pdf(x, a = a, loc = dd, scale = p)
	if draw:
		sns.lineplot(x=x, y=y, ax=ax)
	return x, y, a, dd, p

def rayleigh_from_library(array, min, max, ax = plt, draw = True):
	dd, p = stats.rayleigh.fit(array)
	x = np.linspace(min, max, 100)
	y = stats.rayleigh.pdf(x, dd, p)
	if draw:
		sns.lineplot(x=x, y=y, ax=ax)
	return x, y, dd, p

def calc(zno_df, subject):
	fig, (ax1, ax2) = plt.subplots(1, 2)

	N = len(zno_df)

	sns.scatterplot(x=zno_df['age'], y=zno_df[subject], ax=ax1)

	mean_arr = np.zeros(N) + zno_df[subject].mean()
	std_arr = np.zeros(N) + zno_df[subject].std()
	med_arr = np.zeros(N) + zno_df[subject].median()
	lp_arr = np.zeros(N) + zno_df[subject].quantile(.05)
	rp_arr = np.zeros(N) + zno_df[subject].quantile(.95)

	sns.lineplot(x=zno_df['age'], y=mean_arr, ax=ax1)
	sns.lineplot(x=zno_df['age'], y=med_arr, ax=ax1)

	sns.lineplot(x=zno_df['age'], y=lp_arr, ax=ax1)
	sns.lineplot(x=zno_df['age'], y=rp_arr, ax=ax1)

	sns.lineplot(x=zno_df['age'], y=mean_arr + std_arr, ax=ax1)
	sns.lineplot(x=zno_df['age'], y=mean_arr - std_arr, ax=ax1)

	k = round(N**0.5)
	math_min = zno_df[subject].min()
	math_max = zno_df[subject].max()
	Mx = zno_df[subject].mean()
	Sx = zno_df[subject].std()
	d = (math_max - math_min) / k

	histogr, b = np.histogram(zno_df[subject], k, density = True)

	sns.histplot(
		zno_df[subject],
		bins = b,
		stat = 'density',
		element = "step"
	)

	# normal_approximation(
	# 	min = math_min,
	# 	max = math_max,
	# 	Mx = Mx,
	# 	Sx = Sx,
	# 	ax = ax2
	# )
	# gamma_approximation(
	# 	array = zno_df[subject],
	# 	min = math_min,
	# 	max = math_max,
	# 	ax = ax2
	# )
	x, y, n_dd, n_p = normal_from_library(
		array = zno_df[subject],
		min = math_min,
		max = math_max,
		ax = ax2
	)
	x, y, g_a, g_dd, g_p = gamma_from_library(
		array = zno_df[subject],
		min = math_min,
		max = math_max,
		ax = ax2
	)

	x, y, r_dd, r_p = rayleigh_from_library(
		array = zno_df[subject],
		min = math_min,
		max = math_max,
		ax = ax2
	)

	exp_freqG = np.zeros(k)
	exp_freqN = np.zeros(k)
	exp_freqR = np.zeros(k)

	for i in range(k):
		exp_freqG[i] = stats.gamma.cdf(math_min +(i + 1) * d, a=g_a, loc=g_dd, scale=g_p)
		- stats.gamma.cdf(math_min + i * d, a=g_a, loc=g_dd, scale=g_p)
		exp_freqN[i] = stats.norm.cdf(math_min + (i + 1) * d, loc=n_dd, scale=n_p)
		- stats.norm.cdf(math_min + i * d, loc=n_dd, scale=n_p)
		exp_freqR[i] = stats.rayleigh.cdf(math_min + (i + 1) * d, loc=r_dd, scale=r_p)
		- stats.rayleigh.cdf(math_min + i * d, loc=r_dd, scale=r_p)

	obs_freq = histogr * d

	print(exp_freqR)

	chiG, pG = stats.chisquare(obs_freq, exp_freqG)
	print('\n\nChi squred test for Gamma distribution')
	print(chiG, pG)
	chiN, pN = stats.chisquare(obs_freq, exp_freqN)
	print('Chi squred test for Hauss distribution')
	print(chiN, pN)
	chiR, pR = stats.chisquare(obs_freq, exp_freqR)
	print('Chi squred test for Rayleigh distribution')
	print(chiR, pR, '\n-------------------\n\n')

	plt.show()

if __name__ == '__main__':
	zno_dataset = './data/ZNO_var12.csv'

	zno_df = pd.read_csv(zno_dataset, sep = ";")
	print(zno_df.head())
	print('\n\n', zno_df.describe())

	subjects = zno_df.columns
	for subject in subjects[2:]:
		calc(zno_df, subject)