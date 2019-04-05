import numpy as np
import plotly.plotly as py


def modulating_function(N):
	"""
	Creates x-values (ffR) and y-values of the theoretical modulating function

	Parameters:
	N (int): limits you want to sum over

	Returns:
	ffR_array (float array): 
	modulating_function_vals (float array):
	"""
	N_array = np.linspace(-N, N, 100)
	ffR_array = np.linspace(-10, 10, len(N_array)) # 2N guessed values for ffR 
	def function(ffR, N, n):
		return np.sqrt(1 - (n/N)**2) * np.cos(2 * np.pi * n * ffR / N)

	MF_values = []
	for ffR in ffR_array:
		MF_values.append(np.sum(function(ffR, N, N_array)))

	return ffR_array, np.array(MF_values)

def u(baseline, hour_angle, wavelength=0.028):
    return np.cos(hour_angle) * baseline / wavelength

