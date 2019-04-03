import numpy as np
import matplotlib.pyplot as plt
import least_squares_fitting as lsf
import data
import astropy.coordinates
import tool_box as tb

class Sun:

	def __init__(self, filepath):
		data_from_interf = np.load("Data/" + filepath)
		self.volts, self.times = data_from_interf["volts"], data_from_interf["unixtime"]
		signal = data.Signal(self.volts, 0.20, len(self.volts))
		self.ra, self.dec = tb.RA_and_DEC_from_unixtimes(self.times, source="sun")
		self.hour_angles = tb.hour_angle(tb.LST_from_unixtimes(self.times), self.ra)


	def plot_signal(self):
		self.signal.plot_signal("Sun Data")
		plt.show()


	def plot_power(self):
		self.signal.plot_power("Sun Spectra")
		plt.show()


	def baseline(self, dimension="1D"):
		if dimension == "1D":
			lsf.baseline_script_1D(self.hour_angles, 0, self.volts, self.times)
		if dimension == "2D":
			lsf.baseline_script_2D(self.hour_angles, 0, self.volts, self.times)

one_hour_sun = Sun("one_hour_sun_data.npz")
multi_hour_sun = Sun("multi_hour_sun_data.npz")
multi_hour_sun.baseline("2D")