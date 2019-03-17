from __future__ import print_function
import numpy as np
import ugradio


units = {"time": "($\mu$s)",
         "frequency": "(mHz)",
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


def scaled(data, volt_range):
    """
    Rescales sampler data.

    Parameters:
    data (array) : data to be rescaled
    volt_range (double) : volt range input parameter

    Returns:
    output (array) : rescaled data
    """
    scaled_output = (data * volt_range) / np.power(2, 15) / 2
    return scaled_output


def load(filename, nblocks):
    """
    Parameters:
    filename (string): address of the file being loaded
    nblocks (int): number of blocks in sample

    Returns:
    complex_array (array): complex array where each element is A + iB
    real_split (array): array of real components of the complex array
    imag_split (array): array of imaginary components of the complex array
    """
    signal = scaled(np.load(filename), 0.05)
    split = np.split(signal, 2)
    real, imaginary = split[0], split[1]
    real_split, imag_split = np.split(real, nblocks), np.split(imaginary, nblocks)
    complex_array = []
    for i in range(nblocks):
        complex_array.append(real_split[i] + 1j * imag_split[i])
    return complex_array, real_split, imag_split


def save_picture(fig, title):
    fig.savefig("Pictures\\" + title + '.png')
