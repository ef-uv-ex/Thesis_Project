# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 10:21:10 2022

Function that applies noise to the input signals over the frequency axis

@author: Administrator
"""

import numpy as np
import copy

def add_noise(rcs, SNR=10):
    
    """
    Function applies noise to the input RCS data given a specific SNR
    Input:
        rcs:  input rcs dictionary
        N:  noise power in dB
    """
    rcs_new = copy.deepcopy(rcs)
    nF, nA = np.shape(rcs_new['tt'])
    SNR = 10**(SNR/10)
    N = np.sqrt((np.max(np.abs(rcs_new['tt']/SNR)))/2)
    N_vec = N*(np.random.randn(nF, 1)+ 1j*np.random.randn(nF,1))
    for i in range(0, nA):
        N_vec = N*(np.random.randn(nF)+ 1j*np.random.randn(nF))
        rcs_new['tt'][:, i] = rcs_new['tt'][:, i] + N_vec
    
    return rcs_new
    # SNR = 10*np.log10(S/N)
