import numpy as np
import rotation as rot
import matplotlib.pyplot as plt
import data
import least_squares_fitting as lsf

class Orion:

	def __init__(self, filepath):
		data_from_interf = np.load("Data/" + filepath)
		self.volts, self.times = data_from_interf["voltage"], data_from_interf["unixtimes"]
		self.polyfit()
		signal = data.Signal(self.volts, 0.20, len(self.volts))
		galactic_coordinates = (209.0137, -19.3816)
		self.ra, self.dec = rot.rotate(galactic_coordinates, rot.GAL_to_EQ_rotation())
		self.hour_angles = lsf.hour_angle(lsf.LST_from_unixtimes(self.times), self.ra)

	def polyfit(self):
		polyfit = np.polyfit(self.times, self.volts, deg=2)
		orion_fit = np.polyval(polyfit, self.times)
		self.volts = self.volts - orion_fit

	def plot_signal(self):
		self.signal.plot_signal("Sun Data")
		plt.show()


	def plot_power(self):
		self.signal.plot_power("Sun Spectra")
		plt.show()


	def baseline(self, dimension="1D"):
		if dimension == "1D":
			lsf.baseline_script_1D(self.hour_angles, self.dec, self.volts, self.times)
		if dimension == "2D":
			lsf.baseline_script_2D(self.hour_angles, self.dec, self.volts, self.times)

orion_data = Orion("orion_data.npz")
orion_data.baseline("2D")