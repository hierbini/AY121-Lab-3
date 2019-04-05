import numpy as np
import rotation as rot
import matplotlib.pyplot as plt
import data
import baseline_fitting as bf
import tool_box as tb

class Orion:

	def __init__(self, filepath):
		data_from_interf = np.load("Data/" + filepath)
		self.volts, self.times = data_from_interf["voltage"], data_from_interf["unixtimes"]
		self.polyfit()
		self.signal = data.Signal(self.volts, 0.20, len(self.volts))
		galactic_coordinates = (209.0137, -19.3816)
		self.ra, self.dec = rot.rotate(galactic_coordinates, rot.GAL_to_EQ_rotation())
		self.hour_angles = tb.hour_angle(tb.LST_from_unixtimes(self.times), self.ra)


	def polyfit(self):
		polyfit = np.polyfit(self.times, self.volts, deg=2)
		orion_fit = np.polyval(polyfit, self.times)
		self.volts = self.volts - orion_fit


	def plot_signal(self):
		self.signal.plot_signal("Orion Data")
		plt.show()


	def plot_power(self):
		self.signal.plot_power("Orion Spectra")
		plt.show()


	def baseline(self, dimension="1D"):
		if dimension == "1D":
			bf.baseline_script_1D(self.hour_angles, self.dec, self.volts, self.times)
		if dimension == "2D":
			bf.baseline_script_2D(self.hour_angles, self.dec, self.volts, self.times)

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


orion_data = Orion("orion_data.npz")
orion_data.baseline("1D")