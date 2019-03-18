
import rotation as rot
import orion
import tool_box as tb
import numpy as np
import matplotlib.pyplot as plt


orion_galactic_coordinates = (209.0137, -19.3816)

def LST_from_unixtimes(unixtimes):
	"""
	Returns LST from array of unixtimes
	"""
	julian_dates = tb.time["Julian"](unixtimes)
	lst = tb.time["LST"](julian_dates)
	return np.array(lst)


def hour_angle(galactic_coordinates, unixtimes):
	"""
	Calculates hour angle from unixtimes
	"""
	lst = np.degrees(LST_from_unixtimes(unixtimes))
	hour_angle = []
	for time in lst:
		rotation2, rotation1 = rot.GAL_to_EQ_rotation(), rot.EQ_to_HA_rotation(time)
		rotation_matrix = np.dot(rotation1, rotation2)
		new_coords = rot.rotate(galactic_coordinates, rotation_matrix)
		hour_angle.append(new_coords[0])
	return np.array(hour_angle)

HA_of_orion_data = hour_angle(orion_galactic_coordinates, orion.times)
plt.plot(HA_of_orion_data, orion.volts)
plt.show()