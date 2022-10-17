# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 16:07:14 2022

- Example spectrogram generator for a make believe signal

@author: Administrator
"""


import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.io as sio
import os, time

# Tkinter utilites for GUI interaction
import tkinter as tk
from tkinter import filedialog as fd # Used to pull files via gui

c = 3e8
k = 1.38e-23

# %% Funcitons

"""Create directories"""
def build_directories():
    
    """
    Builds directories variabels that are used to find data
    
    Input:
        Empty
    Output:
        ROOT = root directory for the program
        dir_DATA = data directory
        dir_FIG = figures directory
        dir_MWIR = mwir data directory
        dir_LWIR = lwir data directory
    """
    
    PATH = os.path.dirname(__file__)
    os.chdir(PATH)
    os.chdir('..')
    _ROOT = os.getcwd()
    _dir_DATA = os.path.join(_ROOT, 'data')
    _dir_FIG = os.path.join(_ROOT, 'figures')
    
    return(_ROOT, _dir_DATA, _dir_FIG)
# End directory builder

ROOT, DATA, FIG = build_directories()

root = tk.Tk()
root.withdraw()
target_file = fd.askopenfilename(initialdir=DATA)
root.destroy()

data = sio.loadmat(target_file, mdict=None, appendmat=True)
keys = list(data.keys())
data = data[keys[3]]



# print('Solving FFT')
# Y0 = np.fft.fft(tx_out)
# Y = np.fft.fftshift(Y0)
# Y = np.abs(Y)
# frq = np.fft.fftfreq(to_tx.shape[-1])
# frq = np.fft.fftshift(frq)

# plt.plot(frq, Y)


# plt.specgram(Y, Fs=1/Ts, Fc=fo, cmap='inferno')
# plt.colorbar()
