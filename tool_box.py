from __future__ import print_function
import numpy as np
import ugradio


units = {"time": "($\mu$s)",
         "frequency": "(Hz)",
         "temperature": "(K)",
         "velocity": "($km \cdot s^{-1}$)",
         "voltage": "($\mu$V)",
         "voltage spectra": "($\mu V \cdot \mu s$)",
         "power spectra": "($\mu V^{2} \cdot \mu s^{2}$)"
        }


time = {"Local": ugradio.timing.local_time,
        "UTC": ugradio.timing.utc, # current UTC as a string
        "UTC seconds": ugradio.timing.unix_time,
        "Julian": ugradio.timing.julian_date, # current Julian day and time,
        "LST": ugradio.timing.lst # current LST at NCH
       }


fft = np.fft.fft
shift = np.fft.fftshift
freq = np.fft.fftfreq


def save_picture(fig, title):
    fig.savefig("Pictures\\" + title + '.png')
