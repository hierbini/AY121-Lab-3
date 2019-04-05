import numpy as np
import linsolve 
import tool_box as tb
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ugradio.coord

def get_val(Qew, Qns, hour_angles):
	"""
	Calculates the value 2*pi*nu*tau, which shows up a lot in our equations. 

	Parameters:
	Qew (float): Single value
	Qns (float): Single value
	hour_angles (float array): hour angles calculated from local sidereal time and right ascension

	Return:
	value (float): Calculated value of 2*pi*nu*tau
	"""
	return 2 * np.pi * (Qew * np.sin(hour_angles) + Qns * np.cos(hour_angles))


def get_A_and_B(volts, hour_angles, Qew, Qns):
	"""
	Solve two systems of linear equations for constants A and B

	sum(volts * hour_angles) = A * sum(cos^2(val))       + B * sum(cos(val)sin(val))
	sum(volts * hour_angles) = A * sum(cos(val)sin(val)) + B * sum(sin^2(val))

	Parameters:
	volts (int array): volts from interferometer data
	hour_angles (float array): hour angles calculated from local sidereal time and right ascension
	Qew (float array): guessed values for Qew
	Qns (float array): guessed values for Qns

	Returns:
	A (float): constant A
	B (float): constant B
	"""
	val = get_val(Qew, Qns, hour_angles)
	cos, sin = np.cos(val), np.sin(val), 
	y = np.sum(volts * hour_angles)

	data = {'cos_squared*A + cos_sin*B': y, 'cos_sin*A + sin_squared*B': y}
	constants = {'cos_sin': np.sum(cos * sin), "cos_squared": np.sum(cos**2), "sin_squared": np.sum(sin**2)}
	ls = linsolve.LinearSolver(data, **constants).solve()
	return ls["A"], ls["B"]


def sum_of_squares(volts, hour_angles, Qew, Qns):
	"""
	Calculates the sum of squares of the residuals, where sum of squares of 
	residuals is equal to the sum over (volts - (Acos(val) + Bsin(val)))^2

	Parameters:
	volts (float array): volts from interferometer data
	hour_angles (float array): hour angles calculated from local sidereal time and right ascension
	Qew (float array): guessed values for Qew
	Qns (float array): guessed values for Qns
	
	Returns:
	sum of squares of residuals (float): a single value 
	"""
	A, B = get_A_and_B(volts, hour_angles, Qew, Qns)
	val = get_val(Qew, Qns, hour_angles)
	residuals = volts - (A*np.cos(val) + B*np.cos(val))
	return np.sum(residuals**2)


def get_minimum_value_coordinates_1D(x_array, y_array):
	ymin = min(y_array)
	xpos = y_array.index(ymin)
	xmin = x_array[xpos]
	return xmin, ymin


def get_minimum_value_coordinates_2D(x1_array, x2_array, y_array):
	ymin = np.min(y_array)
	x1_index, x2_index = np.unravel_index(y_array.argmin(), y_array.shape)
	x1min, x2min = x1_array[x1_index], x2_array[x2_index]
	return x1min, x2min, ymin


def get_Bew(Qew, declination, wavelength=0.028):
	return Qew * wavelength / np.cos(declination)


def get_Bns(Qns, declination, wavelength=0.028, terrestrial_latitude=37.873199):
	return Qns * wavelength / np.cos(declination) / np.sin(np.radians(terrestrial_latitude))


def baseline_value(Bew, Bns):
	"""
	Calculates the baseline, which is the distance between the two telescopes in our interferometer.

	Parameters:
	Bew (float): east to west baseline component
	Bns (float): north to south baseline component
	
	Returns:
	B (float): length of baseline in meters
	"""
	return np.sqrt(Bew**2 + Bns**2)

#hahahahahahhahahahahahahahahahahahhahswaghahahahahhahahagooooooooooooooooooootttttttttttteeeeeeeeeeeeeeeeeemmmmmmmmmmmmmmmmmmm#

def baseline_script_1D(hour_angles, dec, volts, times):
	Qew_values = np.linspace(500, 720, 10000)
	s_squared_of_residuals = [sum_of_squares(volts, hour_angles, Q, 0) for Q in Qew_values]
	min_Qew, min_s_squared = get_minimum_value_coordinates_1D(Qew_values, s_squared_of_residuals)

	print("Qew value: " + str(min_Qew), "S_squared value: " + str(min_s_squared))
	print("Baseline: " + str(baseline_value(Qew=min_Qew, Qns=0, declination=dec)))

	plt.plot(Qew_values, s_squared_of_residuals, color='k', linewidth=1.0)
	plt.scatter(min_Qew, min_s_squared, color='c', linewidth=5)
	plt.xlabel("$Q_{ew}$ Values")
	plt.ylabel("$S^{2}$ Values")
	plt.grid()
	plt.show()


def baseline_script_2D(hour_angles, dec, volts, times):
	Qew_values = np.linspace(660, 690, 100)
	Qns_values = np.linspace(40, 50, 100)
	s_squared_of_residuals = []
	for Qns in Qns_values:
		Qns_dimension = []
		for Qew in Qew_values:
			Qns_dimension.append(sum_of_squares(volts, hour_angles, Qew, Qns))
		s_squared_of_residuals.append(Qns_dimension)
	s_squared_of_residuals = np.array(s_squared_of_residuals)
	min_Qew, min_Qns, min_s_squared = get_minimum_value_coordinates_2D(Qew_values, Qns_values, s_squared_of_residuals)
	Bew, Bns = get_Bew(min_Qew, declination), get_Bns(min_Qns, declination)
	baseline = baseline_value(Bew, Bns)
	print("Qew value: " + str(min_Qew), "Qns value: " + str(min_Qns), "S_squared value: " + str(min_s_squared))
	print("Baseline: " + str(baseline))
	return Bew, Bns, baseline