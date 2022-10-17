from copy import deepcopy
import numpy as np


def norm_a(rcs, a=None, p=None):
    """
    Norm the RCS data using Z-score statistical normalization over the angle data.
    This will apply Z-score normalization over frequency slices.
        Input:
            RCS:  input RCS structure
        Output:
            RCS_An:  RCS data Z-score normalized over angle
    """

    pol = ['tt', 'pp', 'tp', 'pt']
    rcs_stat = deepcopy(rcs)

    if type(rcs) == dict:
        for p in pol:
            if np.sum(np.abs(rcs[p])) > 0:  # Ensure there is useful data in the polarization array
                rcs[p] = 4 * np.pi * (np.abs(rcs[p])) ** 2
                m = rcs[p + '_An'][0, :]
                v = rcs[p + '_An'][1, :]

                rcs_stat[p] = (rcs[p] - m[:, np.newaxis]) / v[:, np.newaxis]
    # End:  Z-score per polarization

    # input is a vector, and operation should be applied locally
    else:
        while a is None:  # Ensure a suitable angle is input
            a = int(input("Enter the angle value this vector was pulled from: \n"))
            if a not in range(0, 361):  # Ensure angle is in range of options
                a = None
                print("Entered angle not valid. Try again dummy. ")
        # END: Angle check
        while p is None:  # Ensure a suitable polarization is input
            p = int(input("Enter polarization: [tt, pp, tp, pt] \n"))
            if p not in ['tt', 'pp', 'tp', 'pt']:  # Ensure angle is in range of options
                p = None
                print("Entered polarization not valid. Try again dummy. ")
        # END: Pol check

        # Pull stats values
        m = rcs[p + '_An'][0, a]
        v = rcs[p + '_An'][1, a]

        rcs_stat = (rcs - m) / v
    # END:  vector norm

    return rcs_stat
# End:  norm over angle


def norm_f(rcs, a=None, p=None):
    """
    Norm the RCS data using Z-score statistical normalization over the frequency data.
    This will apply Z-score normalization over angle slices.
        Input:
            RCS:  input RCS structure
            a:  angle input (Only required for vector inputs)
            p:  polarization data (ONly required for vector inputs)
        Output:
            RCS_An:  RCS data Z-score normalized over frequency
    """

    pol = ['tt', 'pp', 'tp', 'pt']
    rcs_stat = rcs  # The passes RCS is a deepcopy already; deepcopy(rcs)

    # Input is a dictionary and operation should be applied over all polarizations
    if type(rcs) == dict:
        for p in pol:
            if np.sum(np.abs(rcs[p])) > 0:  # Ensure there is useful data in the polarization array
                rcs[p] = 4 * np.pi * (np.abs(rcs[p])) ** 2
                m = rcs[p + '_Fn'][0, :]
                v = rcs[p + '_Fn'][1, :]

                rcs_stat[p] = (rcs[p] - m) / v
    # End:  Dictionary norm

    # input is a vector, and operation should be applied locally
    else:
        while a is None:  # Ensure a suitable angle is input
            a = int(input("Enter the angle value this vector was pulled from: \n"))
            if a not in range(0, 361):  # Ensure angle is in range of options
                a = None
                print("Entered angle not valid. Try again dummy. ")
        # END: Angle check
        while p is None:  # Ensure a suitable polarization is input
            p = int(input("Enter polarization: [tt, pp, tp, pt] \n"))
            if p not in ['tt', 'pp', 'tp', 'pt']:  # Ensure angle is in range of options
                p = None
                print("Entered polarization not valid. Try again dummy. ")
        # END: Pol check

        # Pull stats values
        m = rcs[p + '_Fn'][0, a]
        v = rcs[p + '_Fn'][1, a]

        rcs_stat = (rcs - m)/v
    # END:  vector norm

    return rcs_stat
# End:  norm over angle


def stan_angle(rcs):
    """
    Standardize amplitudes between 0 and 1 per frequency slice
        Input:
            rcs:  input RCS structure
        Output:
            rcs:  standardized amplitudes over frequency slice
    """

    pol = ['tt', 'pp', 'tp', 'pt']

    if type(rcs) == dict:
        for p in pol:
            if np.sum(np.abs(rcs[p])) > 0:  # Ensure there is useful data in the polarization array
                rcs[p] = 4 * np.pi * (np.abs(rcs[p])) ** 2
                rcs[p] = rcs[p] / np.max(rcs[p], axis=1)[:, np.newaxis]
    # End:  Z-score per polarization

    # input is a vector, and operation should be applied locally
    else:
        # rcs = 4 * np.pi * np.abs(rcs) ** 2
        rcs = rcs / np.max(rcs)
    # END:  vector norm

    return rcs
# End:  standardized magnitude over angle


def stan_freq(rcs):  # Can take dict or vector inputs
    """
    Standardize amplitudes between 0 and 1 per angle slice.
        Input:
            rcs:  input RCS structure
        Output:
            rcs:  standardized amplitudes over angle slice
    """

    pol = ['tt', 'pp', 'tp', 'pt']

    if type(rcs) == dict:
        for p in pol:
            if np.sum(np.abs(rcs[p])) > 0:  # Ensure there is useful data in the polarization array
                rcs[p] = 4 * np.pi * (np.abs(rcs[p])) ** 2
                rcs[p] = rcs[p] / np.max(rcs[p], axis=0)
    # End:  standardization per polarization

    # input is a vector from the data generator
    else:
        # rcs = 4*np.pi*np.abs(rcs)**2
        rcs = rcs/np.max(rcs)
    # END:  vector norm

    return rcs
# End:  standardized magnitude over angle


def augment_amp(rcs, amp, a=None, pol=None):
    """
    Augment the amplitude of the given RCS based on the type desired
        Input:
            rcs:  input RCS structure
            amp:  augmentation type
        Output:
            rcs:  augmented RCS
            label:  string describing the augmentation employed
    """

    if amp == 'Na':
        rcs = norm_a(rcs, a, pol)
        label = 'Z-Score Norm, Angle'
        mag = '# $\sigma$'
    elif amp == 'Nf':
        rcs = norm_f(rcs, a, pol)
        label = 'Z-Score Norm, Freq.'
        mag = '# $\sigma$'
    elif amp == 'dBm':
        for p in pol:
            rcs[p] = 4 * np.pi * np.abs(rcs[p]) ** 2
            rcs[p] = 10 * np.log10(rcs[p] / 0.001)
        label = 'RCS [$dB_m$]'
        mag = 'RCS [$dB_m$]'
    elif amp == 'RCS':
        for p in pol:
            rcs[p] = 4 * np.pi * np.abs(rcs[p]) ** 2
        label = 'RCS [$m^2$]'
        mag = 'RCS [$m^2$]'
    elif amp == 'Sa':
        rcs = stan_angle(rcs)
        label = 'Standardized amplitude over angle'
        mag = 'Standardized Amplitude'
    elif amp == 'Sf':
        rcs = stan_freq(rcs)
        label = 'Standardized amplitude over freq.'
        mag = 'Standardized Amplitude'
    elif amp == 'Nas':
        rcs = norm_a(rcs, a, pol)
        rcs = stan_angle(rcs)
        label = "Normalized over angle, with standardized amplitude"
        mag = 'Standardized Norm'
    elif amp == 'Nfs':
        rcs = norm_f(rcs, a, pol)
        rcs = stan_freq(rcs)
        label = "Normalized over freq., with standardized amplitude"
        mag = 'Standardized Norm'

    return rcs, label, mag
# End:  standardized magnitude over angle
