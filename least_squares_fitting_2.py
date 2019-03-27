import numpy as np
import linsolve 
import tool_box as tb
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import least_squares_fitting as lsf

def LST_from_unixtimes(unixtimes):
    """
    Returns LST from array of unixtimes
    """
    julian_dates = tb.time["Julian"](unixtimes)
    lst = tb.time["LST"](julian_dates)
    return lst


def hour_angle(unixtimes, ra):
    """
    Calculates hour angle from unixtimes in radians
    """
    lst = LST_from_unixtimes(unixtimes)
    return (lst - np.radians(ra))


def get_A_and_B(volts, hour_angles, Qew, Qns):
	y_i = np.sum(volts * hour_angles)
	val = 2 * np.pi * (Qew * np.sin(hour_angles) + Qns * np.sin(hour_angles))
	cos, sin = np.cos(val), np.sin(val), 
	cos_sin = cos*sin
	data = {'cos_2*A + cos_sin*B': y_i, 'cos_sin*A + sin_2*B': y_i}
	constants = {'cos_sin': np.sum(cos_sin), "cos_2": np.sum(cos**2), "sin_2": np.sum(sin**2)}
	ls = linsolve.LinearSolver(data, **constants).solve()
	A, B = ls["A"], ls["B"]
	return A, B


def sum_of_squares(volts, hour_angles, Qew, Qns):
	A, B = get_A_and_B(volts, hour_angles, Qew, Qns)
	val = 2 * np.pi * (Qew * np.sin(hour_angles) + Qns * np.sin(hour_angles))
	return np.sum((volts - (A*np.cos(val) + B*np.sin(val)))**2)


def get_minimum_value_coordinates(x1_array, x2_array, y_array):
	ymin = np.min(y_array)
	x1_index, x2_index = np.unravel_index(y_array.argmin(), y_array.shape)
	x1min, x2min = x1_array[x1_index], x2_array[x2_index]
	return x1min, x2min, ymin


def baseline_value(Qew, Qns, declination, wavelength=0.025, terrestrial_latitude=37.873199):
	Bew = Qew * wavelength / np.cos(declination)
	Bns = Qns * wavelength / np.cos(declination) / np.sin(np.radians(terrestrial_latitude))
	print("Bew value: " + str(Bew), "Bns value: " + str(Bns))
	B = np.sqrt(Bew**2 + Bns**2)
	return B


def baseline_script_1D(ra, dec, volts, times):
	print("RA: " + str(ra), "DEC: " + str(dec))
	hour_angles = hour_angle(times, ra)
	Qew_values = np.linspace(620, 720, 10000)
	s_squared_of_residuals = [sum_of_squares(volts, hour_angles, Q) for Q in Qew_values]
	min_Qew, min_s_squared = get_minimum_value_coordinates(Qew_values, s_squared_of_residuals)

	print("Qew value: " + str(min_Qew), "S_squared value: " + str(min_s_squared))
	print("Baseline: " + str(baseline_value(Qew=min_Qew, Qns=0, declination=dec)))
	plt.plot(Qew_values, s_squared_of_residuals, color='k', linewidth=1.0)
	plt.scatter(min_Qew, min_s_squared, color='c', linewidth=5)
	plt.xlabel("$Q_{ew}$ Values")
	plt.ylabel("$S^{2}$ Values")
	plt.grid()
	plt.show()


def baseline_script_2D(ra, dec, volts, times):
	print("RA: " + str(ra), "DEC: " + str(dec))
	hour_angles = hour_angle(times, ra)
	Qew_values = np.linspace(660, 690, 100)
	Qns_values = np.linspace(40, 50, 100)
	s_squared_of_residuals = []
	for Qns in Qns_values:
		print("beep")
		Qns_dimension = []
		for Qew in Qew_values:
			Qns_dimension.append(sum_of_squares(volts, hour_angles, Qew, Qns))
		s_squared_of_residuals.append(Qns_dimension)
	s_squared_of_residuals = np.array(s_squared_of_residuals)
	min_Qew, min_Qns, min_s_squared = get_minimum_value_coordinates(Qew_values, Qns_values, s_squared_of_residuals)

	print("Qew value: " + str(min_Qew), "Qns value: " + str(min_Qns), "S_squared value: " + str(min_s_squared))
	print("Baseline: " + str(baseline_value(Qew=min_Qew, Qns=min_Qns, declination=dec)))