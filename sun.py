import numpy as np
import matplotlib.pyplot as plt
import baseline_fitting as bf
import data
import astropy.coordinates
import tool_box as tb
import diameter


class Sun:

	def __init__(self, filepath):
		data_from_interf = np.load("Data/" + filepath)
		self.volts, self.times = data_from_interf["volts"], data_from_interf["unixtime"]
		self.signal = data.Signal(self.volts, 0.20, len(self.volts))
		self.ra, self.dec = tb.RA_and_DEC_from_unixtimes(self.times, source="sun")
		self.hour_angles = tb.hour_angle(tb.LST_from_unixtimes(self.times), self.ra)


	def plot_signal(self):
		print(self.volts, self.hour_angles)
		plt.plot(self.hour_angles, self.volts)


	def plot_power(self):
		self.signal.plot_power("Sun Spectra")
		plt.show()


	def baseline(self, dimension="1D"):
		if dimension == "1D":
			bf.baseline_script_1D(self.hour_angles, 0, self.volts, self.times)
		if dimension == "2D":
			bf.baseline_script_2D(self.hour_angles, 0, self.volts, self.times)

	def fringe_frequency(self, wavelength=0.028, terrestrial_latitude=37.873199, h_s0=0):
		"""
		Calculates the fringe frequency from the baseline.

		Parameters:
		h_s0: the hour angle at the meridian, which is equal to 0
		"""
		Bew, Bns, baseline = bf.baseline_script_2D(self.hour_angles, 0, self.volts, self.times)
		first_term = Bew / wavelength * np.cos(self.dec) * cos(h_s0)
		second_term = Bns / wavelength * np.sin(terrestrial_latitude) * np.cos(self.dec) * np.sin(h_s0)
		return first_term - second_term


#one_hour_sun = Sun("one_hour_sun_data.npz")
multi_hour_sun = Sun("multi_hour_sun_data.npz")
#ffR_array, MF_values = diameter.modulating_function(100)
#plt.plot(ffR_array, MF_values)
multi_hour_sun.plot_signal()
plt.show()