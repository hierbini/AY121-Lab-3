
import rotation as rot
import orion
import tool_box as tb
import numpy as np
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
	Calculates hour angle from unixtimes
	"""
	lst = np.degrees(LST_from_unixtimes(unixtimes))
	return (lst - ra) / 15


orion_galactic_coordinates = (209.0137, -19.3816)
orion_ra, orion_dec = rot.rotate(orion_galactic_coordinates, rot.GAL_to_EQ_rotation())
orion_hour_angles = hour_angle(orion.times, orion_ra)
plt.plot(orion_hour_angles, orion.volts)
plt.show()