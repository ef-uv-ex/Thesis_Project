# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 14:52:21 2022

Function used to normalize the data in the rcs dictionaries

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt

def norm_data(rcs, a_flag=False, f_flag=False):
    
    """
    Function used to normalize RCS data along either the frequency or angle. 
    
    INput: 
        rcs:  rcs data object
        a_flag:  angle flag, Norms along the angle
        f_flag:  frequency flag, Norms along the freqs
        
    Output:
        rcs_new:  normalized RCS
    """

    # Check for flag input
    flags = [a_flag, f_flag]
    if (a_flag==False and f_flag==False) or (a_flag==True and f_flag==True):
        new_flag = ''
        while new_flag != ('a' or 'f'):
            new_flag = input("Please select which domain to normalize over: ['a' or 'f']: \n")
            if new_flag != ('a' or 'f'):
                print("Please type either 'a' or 'f' without the quotes, you dummy.")
        if new_flag == 'a': ax = 1
        elif new_flag == 'f': ax = 0
    elif flags == [True, False]: ax = 1
    elif flags == [False, True]: ax = 0
    # End flag check
    
    # Create the new dict
    rcs_new = rcs.copy()
    keys = ['tt', 'pp', 'tp', 'pt']
    
    frq = rcs['frq']
    a = rcs['ph']
    for k in keys:
        rcs_new[k] = 4*np.pi*np.abs(rcs_new[k])**2
        shape = np.shape(rcs_new[k])
        
        if np.shape(rcs_new[k])[0] > 0:
            m = rcs_new[k].max(axis=ax)
            if ax == 1:                
                for c in range(shape[1]): # Opeate over the angles
                    rcs_new[k][:, c] = rcs_new[k][:, c]/m
            elif ax == 0:                
                for r in range(shape[0]): # Opeate over the freq
                    rcs_new[k][r, :] = rcs_new[k][r, :]/m
    # End normaliation ops
    rcs_new['name'] = rcs_new['name']+' Norm'
    return rcs_new  
        
    
        