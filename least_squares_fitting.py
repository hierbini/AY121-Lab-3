import numpy as np
import linsolve 
import rotation as rot
import orion
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
	Calculates hour angle from unixtimes in degrees
	"""
	lst = np.degrees(LST_from_unixtimes(unixtimes))
	return (lst - ra)


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
	ymin = min(s_squared)
	xpos = s_squared.index(ymin)
	xmin = orion_Q_ew[xpos]
	return xmin, ymin

orion_galactic_coordinates = (209.0137, -19.3816)
orion_ra, orion_dec = rot.rotate(orion_galactic_coordinates, rot.GAL_to_EQ_rotation())
print("RA: " + str(orion_ra), "Dec: " + str(orion_dec))
orion_hour_angles = hour_angle(orion.times, orion_ra)
orion_Q_ew = np.linspace(30, 60, len(orion_hour_angles))
s_squared = [sum_of_squares(orion.volts, orion_hour_angles, Q) for Q in orion_Q_ew]
min_Q, min_s_squared = get_minimum_value_coordinates(orion_Q_ew, s_squared)
print("Qew value: " + str(min_Q), "S_squared value: " + str(min_s_squared))
plt.plot(orion_Q_ew, s_squared, color='k')
plt.axvline(min_Q, min_s_squared, color='c', linestyle = "--")
plt.show()
 


