# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 13:55:18 2022

Function module used to extract data from the selected RCS dictionary

@author: Administrator
"""

from RCS_Class import rcs_keys
from numpy import where, abs, sum
from copy import deepcopy

def extract_data(rcs, _f=None, _a=None, _pol=None):
    
    """Extract the data from an AFIT RCS struct over a certain band of 
    frequencies, azimuthal angles, or polarizations
    
    Inputs:
            _rcs_data:  input rcs data struct
            _f: requested frequeny, or frequency range. Expects np array
            _a:  requested angles
            _pol:  requested polarizations
    """
    # Create empty dict with correct keys pre-loaded
    # ['frq', 'ph', 'th', 'tt', 'pp', 'tp', 'pt', 'header']
    new_rcs = deepcopy(rcs)
    data_keys = ['tt', 'pp', 'tp', 'pt']
    
    # Parse input angles
    if _a:
        nA = len(_a)
        if nA > 2:
            print("Extracting angles at {0}".format(str(_a)))
            a_idx = []
            for a in _a: 
                idx = where(rcs['ph'] == a)[0][0]
                a_idx.append(idx)
                
            new_rcs.update( {'ph':rcs['ph'][a_idx]} )
            
            for i in data_keys:
                new_rcs.update( { i:rcs[i][:, a_idx] } )
        
        elif nA == 1:
            print("Extracting angles at {0}".format(str(_a)))
            a_idx = where(rcs['ph'] == _a[0])[0][0]
            new_rcs.update( {'ph':rcs['ph'][a_idx]} ) 
            
            for i in data_keys:
                if len(rcs[i]) < a_idx: new_rcs.update( {i : rcs[i]} )
                else: new_rcs.update( { i:rcs[i][:, a_idx] } )
                
        elif nA == 2:
            print("Extracting angles at {0} and {1}".format(str(_a[0]), str(_a[1])))
            a_idx = [ where(rcs['ph'] == _a[0])[0][0],
                     where(rcs['ph'] == _a[1])[0][0] ]
            new_rcs.update( {'ph':rcs['ph'][a_idx[0]:a_idx[1]]} ) 
            
            for i in data_keys:
                if len(rcs[i]) < a_idx: new_rcs.update( {i : rcs[i]} )
                else: new_rcs.update( { i:rcs[i][:, a_idx[0]:a_idx[1]]} )
    else:
        print("No angles entered.")
        #new_rcs = rcs

    # Parse input frequencies
    if _f:
            
        nF = len(_f) 
        if nF > 2:
            print("Frequencies range too large. Pick a min and max only.")
            return
        
        elif nF == 1:
            print("Extracting frequency at {0}.".format(str(_f)))
            f_idx = where(rcs['frq'] == _f[0])[0][0]
            new_rcs.update( {'frq':rcs['frq'][f_idx]} ) 
            
            for i in data_keys:
                if len(rcs[i]) < f_idx: new_rcs.update({i:rcs[i]})
                else: new_rcs.update( { i:rcs[i][f_idx, :] } )
                
        elif nF == 2:
            print("Extracting frequencies at {0}, and {1}.".format(str(_f[0]), str(_f[1])))

            if (_f[0] == rcs['frq'][0]) and (_f[1] == rcs['frq'][-1]):
                new_rcs.update({'frq': rcs['frq']})
            else:
                f_idx = [where(rcs['frq'] == _f[0])[0][0],
                         where(rcs['frq'] == _f[1])[0][0]+1]
                f = rcs['frq'][f_idx[0]:f_idx[1]]
                new_rcs.update({'frq': f})
            
            for p in data_keys:
                # Pol has no content
                if sum(abs(rcs[p])) <= 0:
                    new_rcs.update({p: rcs[p]})

                # Pol has content
                else:
                    # Frequencies are in the correct range
                    if (_f[0] == rcs['frq'][0]) and (_f[1] == rcs['frq'][-1]):
                        new_rcs.update({p: rcs[p]})
                    # Frequencies must be sliced
                    else:
                        new_rcs.update({p: rcs[p][f_idx[0]:f_idx[1], :]})
            # End:  Per polarization frequency slicing

    else:
        print("No frequencies entered.")
        #new_rcs.update({'frq': rcs['frq']})
        
    return new_rcs


















