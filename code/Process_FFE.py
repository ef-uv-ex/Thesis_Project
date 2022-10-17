# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:55:30 2022

Prep FFE data to be used alongside measurement data

Typically just a call to duplicate the simpler FFE data

@author: Administrator
"""

from numpy import arange, flip, append

def process_ffe(rcs):
    
    """
    Function that duplicates and flips the data from a 180 degree solution
    for a symetrical FFE
    
    Inputs:
        rcs:  the rcs dictionary that will be re-arranged
    """
    
    # Check degree increments
    a = rcs['ph']
    da = a[1]-a[0]
    a_new = arange(0, 360, da)
    rcs['ph'] = a_new
    
    # Pull the measurement data via keys
    key_list = ['tt', 'pp', 'pt', 'tp']
    for i in key_list:
        data = flip(rcs[i][:, 1:-1], 1) # Grab all cols but first and last
        rcs[i] = append(rcs[i], data, 1)
        
    return rcs
        
    
