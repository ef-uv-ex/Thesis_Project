# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 16:07:14 2022

- Example spectrogram generator for a make believe signal

@author: Administrator
"""


import numpy as np
import matplotlib.pyplot as plt
import math

c = 3e8
k = 1.38e-23

fo = 2e6    # Frq in Hz
PRI = 1e-3  # PRI in s
Ts = 1e-8   # sample time
pw = 1e-6   # pulse width

Eo = 1      # Signal voltage
t_d = 0     # Time delay
l = c/fo    # Wavelength
Pt = Eo**2  # Signal Power

# PRI group total time
to_tx = np.arange(0, PRI-Ts, Ts)
# to_tx = np.tile(to_tx, [1, 4])

# Pulse Train
N_fast = int(PRI/Ts)     # how many samples are there in PRI...PRI == "fast time"
N_pulse = int(math.ceil(pw/Ts))  # How many samples are there in the pulse
pulse_tx = np.concatenate((np.ones(N_pulse), np.zeros(N_fast-N_pulse-1)), 0)

# Time domain signal
tx_out = np.multiply(to_tx, pulse_tx)
tx_out = np.tile(tx_out, [1, 4])[0, :]
to_tx = np.tile(to_tx, [1, 4])[0, :]

# take the fft
print('Solving FFT')
Y0 = np.fft.fft(tx_out)
Y = np.fft.fftshift(Y0)
Y = np.abs(Y)
frq = np.fft.fftfreq(to_tx.shape[-1])
frq = np.fft.fftshift(frq)

plt.plot(frq, Y)


# plt.specgram(Y, Fs=1/Ts, Fc=fo, cmap='inferno')
# plt.colorbar()
