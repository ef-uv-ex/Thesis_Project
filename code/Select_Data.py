# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:11:37 2022

Custom function used to select data for analysis.

@author: Administrator
"""

"""Select Data to import"""

# Tkinter utilites for GUI interaction
import tkinter as tk
from tkinter import filedialog as fd # Used to pull files via gui
import scipy.io as sio # To read in .mat file types
import scipy.stats as sts
import numpy as np

def select_data(_dir_DATA, name='???'):
    
    """
    Function that prompts the user to browse directories and select the 
    target RCS data file. Data files are type .mat. They are created using
    matlab code provided by the AFIT EENG 627 course. This code uses a binary 
    read-funciton written by the radar developer that is written in matlab. 
    
    Input:
        None
        
    Output:
        None
        
    """
    
    # identify data to load
    root = tk.Tk()
    root.lift()
    path = fd.askopenfilename(initialdir=_dir_DATA)
    root.destroy()

    # Pull the rsr object from matlab
    data = sio.loadmat(path, mdict=None, appendmat=True)
    keys = list(data.keys())
    data = data[keys[-1]]
    data = data[0,0]
    
    # Data to dictionary
    rcs = {}
    rcs.update({'name': name})
    rcs.update({'frq': np.asarray(data[0])[0]})
    rcs.update({'ph': np.asarray(data[1])[0]})
    rcs.update({'th': data[2]})
    # The readFEKO script multiplies raw values by sqrt(4*PI)
    rcs.update({'tt': np.asarray(data[12])/np.sqrt(4*np.pi)})
    rcs.update({'pp': np.asarray(data[13]/np.sqrt(4*np.pi))})
    rcs.update({'tp': data[14]/np.sqrt(4*np.pi)})
    rcs.update({'pt': data[15]/np.sqrt(4*np.pi)})
    rcs.update({'header': data[16]})

    return rcs
# End Data Selection

def calc_stats(rcs):
    """ Pull probability values, and store in a matrix"""
    pols = ['tt', 'pp', 'tp', 'pt']
    print("Calculating statistics over Frequency and Angle using RCS in [$m^2$]")
    print('\n')
    for p in pols:
        if np.sum(np.abs(rcs[p])) > 0:
            d = 4 * np.pi * (np.abs(rcs[p])) ** 2

            d_As = d  # /np.max(d, axis=1)[:, np.newaxis]
            d_Fs = d  # /np.max(d, axis=0)

            F, A = np.shape(d)
            A_norm = np.ndarray((4, F)) * 0
            F_norm = np.ndarray((4, A)) * 0

            # Calculate Mean
            A_norm[0, :] = np.mean(d_As, axis=1)
            F_norm[0, :] = np.mean(d_Fs, axis=0)

            # Calculate Var
            A_norm[1, :] = np.std(d_As, axis=1)
            F_norm[1, :] = np.std(d_Fs, axis=0)

            # Calulate Skewness
            A_norm[2, :] = sts.skew(d_As, axis=1)
            F_norm[2, :] = sts.skew(d_Fs, axis=0)

            # Calculate Kurtosis
            A_norm[3, :] = sts.kurtosis(d_As, axis=1)
            F_norm[3, :] = sts.kurtosis(d_Fs, axis=0)

            rcs.update({p + '_An': A_norm})
            rcs.update({p + '_Fn': F_norm})

    return rcs
# END: Calc stats

def convert_rcs(rcs):
    
    """
    Convert the input data from complex to rcs
    """

    rcs_new = rcs.copy()
    keys = ['tt', 'pp', 'tp', 'pt']
    for k in keys:
        rcs_new[k] = 4*np.pi*np.abs(rcs_new[k])**2
    # End rcs conversion
        
    return rcs_new

def simple_load(_dir_DATA):
    # identify data to load
    root = tk.Tk()
    root.lift()
    path = fd.askopenfilename(initialdir=_dir_DATA)
    root.destroy()

    # Pull the rsr object from matlab
    data = np.load(path, allow_pickle=True)

    return data
# Simple load funciton






