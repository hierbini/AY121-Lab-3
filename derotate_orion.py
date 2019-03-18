
import rotation
import orion
import tool_box as tb

def hour_angle(unixtimes):
	"""
	Calculates hour angle from unixtimes
	"""
	lst = LST_from_unixtimes(unixtimes)
	ra = RA_from_unixtimes(unixtimes)
	print(lst, ra)
	return lst - ra


def LST_from_unixtimes(unixtimes):
	"""
	Returns LST from array of unixtimes
	"""
	julian_dates = tb.time["Julian"](unixtimes)
	lst = tb.time["LST"](julian_dates)
	return lst


orion_galactic_coordinates = (209.0137, -19.3816)
rotation_matrix = rotation.GAL_to_EQ_rotation()
right_ascension, declination = rotation.rotate(orion_galactic_coordinates, rotation_matrix)
print("Right Ascension: " + str(right_ascension))
print("Declination: " + str(declination))

seconds_per_day = 86164.091 # number of seconds in a solar day
degree_per_second = 360 / seconds_per_day # rate at which RA of star changes


def RA_from_unixtimes(unixtimes):
	"""
	Calculates Right Ascension from array of unixtimes
	"""
	current_time = tb.time["UTC seconds"]() # current unixtime in seconds
	time_difference = current_time - unixtimes # different in unixtime
	print(current_time)
	print(unixtimes)
	change_in_right_ascension = degree_per_second * time_difference # get change in degrees
	print(change_in_right_ascension)
	return right_ascension - change_in_right_ascension # derotate RA 

HA_of_orion_data = hour_angle(orion.times)
print(HA_of_orion_data)
