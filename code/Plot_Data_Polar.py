# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 13:01:09 2022

@author: Administrator
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_data(m_rcs, s_rcs):
    
    """
    Function used to generate data plots for the desired rcs data
    Inputs:
        m_rcs:  measurement data rcs
        s_rcs:  simulation data rcs
    Outputs:
        plots
    """
    """
    
    Funciton returns several sets of plot data:
        Figure 1: Linear Plots of the measured and simulated data in h and v
    
    """
    
    
    """Pre-process data"""
    a = s_rcs['ph']*(np.pi/180)
    f = [9.5, 10, 10.5] # Frequencies to grab for plots
    f_keys = ['9.5 GHz', '10 GHz', '10.5 GHz']
    s_h = {}
    s_v = {}
    m_h = {}
    m_v = {}
    for i, v in enumerate(f):
        idx = (np.where(s_rcs['frq']==v)[0][0])
        
        s = np.log10(np.abs(s_rcs['pp'][idx, :]))
        s_h.update( {f_keys[i] : s} )
        
        s = np.log10(np.abs(s_rcs['tt'][idx, :]))
        s_v.update( {f_keys[i] : s} )
        
        s = np.log10(np.abs(m_rcs['pp'][idx, :]))
        m_h.update( {f_keys[i] : s} )
        
        s = np.log10(np.abs(m_rcs['tt'][idx, :]))
        m_v.update( {f_keys[i] : s} )
        
    """Create Polar plots:  """
    # Plot polar

    # Horizontal Polarization
    fig, ax = plt.subplots(2, 3, subplot_kw={'projection': 'polar'})
    fig.suptitle('Horizontally Polarized Incident Wave')
    for i, v in enumerate(f_keys): 
        ax[0, i].plot(a, s_h[v], label=v)
        ax[0, i].set_title('Normalized Simulation RCS, \n '+v)
        ax[0, i].grid(True)
        
        ax[1, i].plot(a, m_h[v], label=v)
        ax[1, i].set_title('Normalized Measurement RCS, \n '+v)
        ax[1, i].grid(True)
    plt.show()
    
    # Vertical Polarization
    fig, ax = plt.subplots(2, 3, subplot_kw={'projection': 'polar'})
    fig.suptitle('Vertically Polarized Incident Wave')
    for i, v in enumerate(f_keys): 
        ax[0, i].plot(a, s_v[v], label=v)
        ax[0, i].set_title('Normalized Simulation RCS, \n '+v) 
        ax[0, i].grid(True)
        
        ax[1, i].plot(a, m_v[v], label=v)
        ax[1, i].set_title('Normalized Measurement RCS, \n '+v)
        ax[1, i].grid(True)
    plt.show()
    
    
    