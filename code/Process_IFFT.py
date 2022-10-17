# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 10:37:50 2022

Custom Function for resolving the IFFT of a signal given a 
set of frequencies

@author: Administrator
"""

import numpy as np
from math import ceil, log
import matplotlib.pyplot as plt

def process_ifft(_rcs, _pol):
    
    """
    Function used to produce an IFFT given complex data spanning a frequency 
    and angular measurement range. 
    
    Input:
        _rcs:  truncated AFIT RCS struct
        _pol:  which polarizations should be plotted
    Output:
    
    """
    
    NYQUIST = 2
    
    # Requested angle
    # Eventually this will be an iterable range that produces pulse vectors
    _a = 0
    
    """WIP:  using zero angle only. MMR 20220906"""
    _tt = np.transpose(np.asarray(_rcs.tt[:, _a]))
    #_pp = np.transpose(np.asarray(_rcs.pp[:, _a]))
    # F = np.asarray(rcs_data.tt)[:, np.where(rcs_data.frq == 7)[0][0]]
    F = np.asarray(_rcs.frq)
    
    """Process measurement data for frequency domain plot"""
    S = 20*np.log10(np.abs(_tt))
    
    fig_num = 'Frequency Domain Plot'
    plot_labels = [
        r'Amplitude vs Frequency for $\phi = 0$', 
        'Amplitude, [dB]', 
        'Frequency, [GHz]',
        ]
    
    plt.plot(F, S)
    plt.title("Amplitude vs Frequency in dB")
    plt.ylabel("Amplitude, [dB]")
    plt.xlabel("Frequency, [GHz]")
    # plot_data = [F, S]
    #plotter(fig_num, plot_data, plot_labels)
    
    
    """Process measurement data for Time Domain Conversion"""
    # Define fourier values need for the IFFT
    n_bandwidth = len(F)                    # Frequency count for collected BW
    bandwidth = (F[-1] - F[0])*1e9          # Collected BW
    frq_res = bandwidth/(n_bandwidth - 1)   # Frq step resolution
    unamb_T = 1/frq_res                     # Unambiguous total time
    T_res = 1/bandwidth                     # time resolution step
    n_pow = ceil(log(NYQUIST*(n_bandwidth-1), 2))
    n_rng_bins = int(2**(n_pow + 1 ))       # Number of bins for time domain
    
    # Time vector 
    T = np.linspace(-unamb_T/2, unamb_T/2, n_rng_bins) - unamb_T/n_rng_bins/2
    
    # Apply the inverse FFT
    A = np.fft.ifft(_tt, 2**n_pow)
    A = np.concatenate((np.flip(A), A))
    
    fig_num = 'Time Domain Impulse'
    plot_labels = [
        r'Impulse vs Time for $\phi = 0$', 
        'Amplitude, [V(?)]', 
        'Time, [ns]',
        ]
    plt.plot(F, S)
    plt.title(r'Impulse vs Time for $\phi = 0$')
    plt.ylabel('Amplitude, [V(?)]')
    plt.xlabel('Time, [ns]')
    #plot_data = [T*1e9, np.abs(A)]
    # plotter(fig_num, plot_data, plot_labels)