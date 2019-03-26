import numpy as np
import linsolve 
import rotation as rot
import tool_box as tb
import matplotlib.pyplot as plt

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


def get_A_and_B(volts, hour_angles, Q_ew):
	y_i = np.sum(volts * hour_angles)
	val = 2 * np.pi * Q_ew * np.sin(hour_angles)
	cos, sin = np.sum(np.cos(val)), np.sum(np.sin(val))
	data = {'cos_2*A + cos_sin*B': y_i, 'cos_sin*A + sin_2*B': y_i}
	constants = {'cos_sin': cos * sin, "cos_2": cos**2, "sin_2": sin**2}
	ls = linsolve.LinearSolver(data, **constants).solve()
	A, B = ls["A"], ls["B"]
	return A, B


def sum_of_squares(volts, hour_angles, Q_ew):
	A, B = get_A_and_B(volts, hour_angles, Q_ew)
	val = 2 * np.pi * Q_ew * np.sin(hour_angles)
	return np.sum((volts - (A*np.cos(val) + B*np.sin(val)))**2)


def get_minimum_value_coordinates(x_array, y_array):
	ymin = min(y_array)
	xpos = y_array.index(ymin)
	xmin = x_array[xpos]
	return xmin, ymin


def baseline_value(Qew, Qns, declination, wavelength=0.025, terrestrial_latitude=37.873199):
	Bew = Qew * wavelength / np.cos(declination)
	Bns = Qns * wavelength / np.cos(declination) / np.sin(np.radians(terrestrial_latitude))
	B = np.sqrt(Bew**2 + Bns**2)
	return B


def get_baseline_script(ra, dec, volts, times):
	print("RA: " + str(ra), "DEC: " + str(dec))
	hour_angles = hour_angle(times, ra)
	Qew_values = np.linspace(620, 720, 10000)
	s_squared_of_residuals = [sum_of_squares(volts, hour_angles, Q) for Q in Qew_values]
	min_Qew, min_s_squared = get_minimum_value_coordinates(Qew_values, s_squared_of_residuals)

	print("Qew value: " + str(min_Qew), "S_squared value: " + str(min_s_squared))
	print("Baseline: " + str(baseline_value(Qew=min_Qew, Qns=0, declination=dec)))
	plt.plot(Qew_values, s_squared_of_residuals, color='k')
	plt.axvline(min_Qew, min_s_squared, color='c', linestyle = "--")
	plt.show()

 


