# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:56:54 2022

Pull Proability data and plot

- Pull the mean and std over f or a

@author: Administrator
"""


def extract_stats(rcs_a, rcs_f):
    
    """
    Function extracts the statistics of the normed data. 
        Input:
                rcs_a:  rcs data normed over angles per frequency
                rcs_f:  rcs data normed over freqs per angle
        Output:
                p_rcs: modified data structure
    """

    # Duplicate input
    p_rcs_a = rcs_a.copy()
    p_rcs_f = rcs_f.copy()
    keys = ['tt', 'pp', 'tp', 'pt']
    
    """Extract stats for angle-normed data"""
    for k in keys:
        
        p_rcs_a[k] =0