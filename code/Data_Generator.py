# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 12:40:25 2022

- Data Processing functions


@author: Administrator
"""

import numpy as np

from Augment_Data import augment_amp
def pull_sector(ia, sl):
    if ia in range(0, 46) or ia in range(316, 360):
        return sl[0]
    elif ia in range(46, 136):
        return sl[1]
    elif ia in range(136, 226):
        return sl[2]
    elif ia in range(226, 316):
        return sl[3]


def data_generator(rcs_dict, pol, T=60, F=1, nS=50, aug='Na'):

    """
    Data generation functions. Produces a numpy data array that can be fed to a convolutional NN

    Inputs:
        RCS_Dict: dictionary of RCS objects. Each entry is keyed to an AFIT RCS struct
        T:  Rx temperature in Fahrenheit
        F:  Noise figure
        pol:  polarizations to include as channel data
        aug:  data augmentation method
            Na:  norm over angle
            Nf:  norm over frequency
            Sa:  standardize over angle
            Sf:  standardize over freq
            Nas:  standardize the norm over angle
            Nfs:  standardize the norm over freq
    """

    # Count the number of RCS objects
    nRCS = len(rcs_dict)

    # Start shaping the data output given the inputs
    nW, nA = np.shape(rcs_dict[list(rcs_dict.keys())[0]][pol[0]])

    # Count the channels
    nC = len(pol)

    # Tally required data rows, and instantiate the array
    nN = nS * nA * nRCS
    data = np.ndarray((nN, nW+1, nC))  # +1 for the label entry that will be included later

    # Build noise power from a thermal model
    # The data from the sim will be in volts. The corresponding noise will be as well
    T = (T - 32)*(5/9)  # Convert from deg F
    T = 273 + T  # Temperature in [K]
    frq = rcs_dict[list(rcs_dict.keys())[0]]['frq']
    B = (frq[-1] - frq[0]) * 1e9  # Bandwidth in [Hz]
    kb = 1.38e-23  # Boltzmann's Constant in [W/K]
    N = np.sqrt(kb * T * B * F)

    sector_labels = [0., 1., 2., 3.]
    idx = 0  # Index location in the main data array

    for key in rcs_dict:  # Loop over RCS objects

        for ia in range(nA):  # Loop over each angle
            sector = pull_sector(ia, sector_labels)

            for s in range(nS):  # Loop over each sample per angle

                for ip, vp in enumerate(pol):  # Loop over each polarization
                    # Build an apply random noise function
                    n = N * (np.random.randn(nW) + 1j * np.random.randn(nW))
                    n += rcs_dict[key][vp][:, ia]

                    """At this point, the function is hard coded to operate over angle slices
                        - Norming over frequency would not work here, since I am pulling ang slices
                        - I would need to rewrite this loop to pull rows instead of columns
                        - For now, I will only pass a function to augment over freq
                        - A vector Z-score will need angle data
                    """
                    if aug == 'Nfs':
                        m = rcs_dict[key][vp + '_Fn'][0, ia]
                        v = rcs_dict[key][vp + '_Fn'][1, ia]

                        n = 4*np.pi*np.abs(n)**2
                        n = (n - m) / v
                        n = n/np.max(n)

                    # Assign sector label
                    n = np.append(n, sector)

                    # Assign to the data tensor
                    data[idx, :, ip] = n

                # Increment position in main data array
                idx += 1
            # End per-sample loop


        # End the per-angle loop
        print("Sector labels for "+rcs_dict[key]['name']+" are "+str(sector_labels)+"\n")
        for i in range(0, len(sector_labels)):
            sector_labels[i] += 4.
    # End RCS loop

    return data
