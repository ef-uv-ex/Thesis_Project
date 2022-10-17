# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 13:01:09 2022

@author: Administrator
"""
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d  # Used for 3D projections

from Augment_Data import norm_a, norm_f, stan_angle, stan_freq, augment_amp
from copy import deepcopy

# Import custom style sheet
plt.style.use('rad_style')  # Save in the 'stylelib' folder in '.matplotlib' of C: directory

def get_colors(n_colors):
    """Pulls colors from a known color map given a number of functions"""
    cmap = cm.magma
    idx = np.linspace(0, cmap.N - 56, n_colors) / cmap.N  # normalize between 0 and 1
    cmap = cmap(idx)
    colors = []
    for c in cmap:
        colors.append(matplotlib.colors.rgb2hex(c))

    return colors
# End of the color finder!


def plot_surface(_rcs, pol='tt', amp='RCS'):
    """Plot the contour results of the input RCS over angle and frequency
        Input:
            rcs:  input RCS data
            pol: polarization to plot
                'all' = plot all polarizations
                'co' = plot copolar alignments
                'cr' = plot cross polar alignments
                'pp, tt, pt, tp' = plot specific polarizations
            type:  How is the amplitude handled
                'RCS':  convert to standard RCS
                'NORM_A': norm over angle
                'NORM_F': norm over frequency
                'RCS_dB': convert to dBm
    """
    rcs = deepcopy(_rcs)
    nP = len(pol)
    nCol = nP
    nRow = nP
    nFig = np.arange(nP)

    # Set params for plot axes
    F = rcs['frq']
    A = rcs['ph']
    A, F = np.meshgrid(A, F)



    for n in range(nRow):
        # Convert to Specified Type
        rcs[pol[n]] = 4 * np.pi * (np.abs(rcs[pol[n]])) ** 2
        label = 'RCS [$m^2$]'

        if amp == 'NORM_A':
            rcs[pol[n]] = rcs[pol[n]] / np.max(rcs[pol[n]], axis=1)
            label = ''
        elif amp == 'NORM_F':
            rcs[pol[n]] = rcs[pol[n]] / np.max(rcs[pol[n]], axis=0)
            label = ''
        elif amp == 'RCS_dB':
            rcs[pol[n]] = 10 * np.log10(rcs[pol][n] / 0.001)
            label = 'RCS [$dB_m$]'

        # Specify labels and plot
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        fig.suptitle(rcs['name'] + ', Frequency vs Angle, \n' \
                     +'Polarization = ' + pol[n] + ', Type = ' + amp)
        plt.xlabel('Angle, [$^{\circ}$]')
        plt.ylabel('Frequency, [GHz]')
        surf = ax.plot_surface(A, F, rcs[pol[n]], cmap=cm.magma)
        fig.colorbar(surf)

        # Set to full screen
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        #plt.show()

    # End polarizations loop
# End Surface plotter


def plot_contour(_rcs, pol=['tt', 'pp'], amp='dBm'):
    """Plot the contour results of the input RCS over angle and frequency
        Input:
            rcs:  input RCS data
            pol: polarization to plot
                'pp, tt, pt, tp' = plot specific polarizations
            type:  How the amplitude is plotted
                'An': norm over angle
                'Fn': norm over frequency
                'dBm': convert to dBm
                'RCS':  convert to standard RCS
    """

    rcs = deepcopy(_rcs)
    nP = len(pol)
    nCol = nP
    nRow = nP
    nFig = np.arange(nP)

    # Set params for plot axes
    F = rcs['frq']
    step = 0.1
    y_ticks = np.arange(F[0], F[-1] + step, step)
    A = rcs['ph']
    step = 45
    x_ticks = np.arange(A[0], A[-1] + step, step)
    A, F = np.meshgrid(A, F)

    # Convert to Specified Type
    rcs, label, mag = augment_amp(rcs, amp, pol)

    for n in range(nCol):
        # Specify labels and plot
        plt.figure()
        plt.title(rcs['name'] + ', Frequency vs Angle, \n' \
                     +'Polarization = ' + pol[n] + ', Type = ' + amp)
        plt.xlabel('Angle, [$^{\circ}$]')
        plt.ylabel('Frequency, [GHz]')
        plt.xticks(x_ticks)
        plt.yticks(y_ticks)
        plt.use_sticky_edges = False
        plt.margins(0.07)
        plt.contourf(A, F, rcs[pol[n]], cmap=cm.magma)
        cbar = plt.colorbar()
        cbar.set_label(mag, rotation=90)

        # Set to full screen render
        # manager = plt.get_current_fig_manager()
        # manager.window.showMaximized()

        #plt.show()

    # End polarizations loop
# End contourf plotter


def plot_rect(_rcs, amp='RCS', pol=['tt', 'pp'], ang=[0, 90, 180, 270]):
    """Plot the cartesian results of the input RCS over frequency at an angle
        Input:
            rcs:  input RCS data
            pol: polarization to plot
    """

    """Pre-process data"""

    rcs = deepcopy(_rcs)
    ang_lox = []
    frq = rcs['frq']
    for a in ang:
        ang_lox.append(np.where(rcs['ph'] == a)[0][0])

    """Create Rect plots:  """
    rows = len(ang)  # Each angle gets a row
    cols = 1
    colors = get_colors(4)
    fig, ax = plt.subplots(rows, cols)

    # Convert to Specified Type
    rcs, label, mag = augment_amp(rcs, amp, pol)

    for i_a, v_a in enumerate(ang_lox):

        for ip, vp in enumerate(pol):
            F = rcs[vp][:, v_a]
            ax[i_a].plot(frq, F, label=vp, color=colors[ip])
            ax[i_a].set_title(str(v_a) + '$^{\circ}$, ' + vp)
            ax[i_a].set_ylabel(mag)
            ax[i_a].legend(loc=(1.02, 0.65))
    # End:  per-angle plotter
    fig.suptitle(rcs['name'] + ' Amplitudes over Frequency, \n'
                 + ' angles = ' + str(ang) + ', polarizations ' + str(pol) + ',\n'
                 + label
                 )

    # Cast figure as max window size
    # manager = plt.get_current_fig_manager()
    # manager.window.showMaximized()


    #plt.show()  # Causes the debugger to hang
# End rect plotter


def plot_polar(_rcs, amp='RCS', pol=['tt', 'pp'], frq=[5], sector=[45, 135, 225, 315]):
    """Plot the polar results of the input RCS over angle and frequency
        Input:
            rcs:  input RCS data
            pol: polarization to plot
    """

    rcs = deepcopy(_rcs)

    """Pre-process data"""
    a = rcs['ph'] * (np.pi / 180)
    sector = np.asarray(sector) * (np.pi / 180)
    # Pull frequency rows by index given a list
    frq_lox = []
    for f in frq:
        frq_lox.append(np.where(rcs['frq'] == f)[0][0])

    """Create Polar plots:  """
    rows = len(frq)
    cols = len(pol)
    colors = get_colors(rows * cols)
    colors = np.reshape(colors, (rows, cols))
    fig, ax = plt.subplots(rows, cols, subplot_kw={'projection': 'polar'})

    # Convert to Specified Type
    rcs, label, mag = augment_amp(rcs, amp, pol)

    for i_f, v_f in enumerate(frq_lox):
        for i_p, v_p in enumerate(pol):

            if rows == 1:
                loc = i_p
            else:
                loc = i_f, i_p

            vec = rcs[v_p][v_f, :]
            ax[loc].plot(a, vec, label=v_p, color=colors[0, loc])
            ax[loc].set_title(str(rcs['frq'][v_f]) + 'GHz, '
                              + v_p)
            for s in sector:
                ax[loc].axvline(s, linestyle=':', color='r')

            ax[loc].grid(True, linestyle=':')
            ax[loc].legend(loc=(1.02, 0.65))
    # End:  Per-frequency plotter
    fig.suptitle(rcs['name'] + ' RCS Cut, \n'
                 + str(frq) + 'GHz, polarizations ' + str(pol) + ', \n'
                 + label
                 )
    #plt.show()  # Causes debugger to hang
# End polar plotter


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
    Generates:
        Figure 1:  3D plots for Rcs vs F at 4 angles with real and image data
    """

    """Pull colors given a poly collection length -- expects 12 functions!!"""
    n_funcs = 12
    cmap = cm.magma
    idx = np.linspace(0, cmap.N, n_funcs) / cmap.N  # normalize between 0 and 1
    cmap = cmap(idx)
    colors = []
    for c in cmap:
        colors.append(matplotlib.colors.rgb2hex(c))

    """Pre-process data"""
    f = s_rcs['frq']
    a = [0, 90, 180, 270]
    keys = ['0', '90', '180', '270']
    s_h = {}
    s_v = {}
    m_h = {}
    m_v = {}
    # Pull columns with the correct angle
    for i, v in enumerate(a):
        idx = (np.where(s_rcs['ph'] == v)[0][0])

        temp = []
        # Single polarization to practice
        temp.append(list(zip(f, s_rcs['pp'][:, idx].real)))  # Pull reals
        temp.append(list(zip(f, s_rcs['pp'][:, idx].imag)))  # Pull Imag
        temp.append(list(zip(f, np.abs(s_rcs['pp'][:, idx]))))
        s_h.update({keys[i]: temp})

    """Build the figure"""
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    """Create the Poly collection 3D Plots """
    c = np.asarray([0, 3])
    z = [1, 2, 3]
    # for k in s_h.keys():
    #     poly = PolyCollection(s_h[k], facecolors=colors[c[0]:c[-1]])
    #     poly.set_alpha(0.7)
    #     ax.add_collection3d(poly, zs=z, zdir='y')
    #     c = c+4
    #     z = z+1

    poly = PolyCollection(s_h['0'])  # , facecolors=colors[c[0]:c[-1]])
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=z, zdir='y')

    """Set Collection locations, and adjust the plots"""
    ax.set_xlabel('Freqeuncy, [GHz]')
    ax.set_xlim3d(f[0], f[-1])
    ax.set_xticks(np.arange(f[0], f[-1], 0.5))
    ax.set_ylabel('Angle, [deg]')
    ax.set_ylim3d(1, 3)
    ax.set_yticks([1, 2, 3])
    ax.set_zlabel('Magnitude, [V?]')
    # ax.set_zlim3d(-0.00005, 0.00005)
    # ax.set_zticks([-1, -0.5, 0, 0.5, 1])
    ax.grid()

    plt.show()
# End Data plotter


def plot_fnorms(s_rcs, m_rcs):
    # Plot the normed freq response at 1 angle
    plt.figure('Normed RCS over Frequency at ph = 90')
    f = s_rcs['frq']
    s1 = s_rcs['tt'][:, 0]
    s2 = m_rcs['tt'][:, 0]
    plt.title('Normed RCS vs Frequency, \n $\phi=90^{\circ}$')
    plt.xlabel('Frequency, [GHz]')
    plt.ylabel('Normalized RCS')
    plt.plot(f, s1, label='Sim')
    plt.plot(f, s2, label='Meas')
    plt.grid(which='both', axis='both')
# End Plot Fnorms


def plot_anorms(s_rcs, m_rcs):
    a = s_rcs['ph'] * np.pi / 180
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    fig.suptitle('Normalized RCS Bugsplat at f=10 GHz')
    ax.plot(a, s_rcs['tt'][50, :], label='Sim')
    ax.plot(a, m_rcs['tt'][50, :], label='Meas')
    ax.grid(True)
    plt.show()
# End plot anorms


def plot_calVerify(s_rcs, m_rcs, a=0, f=10, pol='tt'):
    plt.close('all')
    _s_rcs = s_rcs.copy()
    _m_rcs = m_rcs.copy()
    key = ['tt', 'pp', 'tp', 'pt']

    # Plot the frequency data as a reference

    """Plot the Error over Frequency"""
    calVerify = {}
    calVerify.update({'frq': _s_rcs['frq']})
    temp = np.abs(_m_rcs[pol][:, a]) / np.abs(_s_rcs[pol][:, a])
    calVerify.update({pol: 20 * np.log(temp)})

    stats = [np.mean(calVerify[pol]),
             np.std(calVerify[pol])
             ]
    stats = np.round_(stats, decimals=2)
    plt.figure(0)
    plt.title('Normalized RCS vs Frequency, \n Polarization=' + str(pol) + ', $\phi=$' + str(a))
    plt.plot(_s_rcs['frq'], _s_rcs[pol][:, a], label="Sim")
    plt.plot(_m_rcs['frq'], _m_rcs[pol][:, a], label="Meas")
    plt.grid(True)
    plt.xlabel('Frequency, [GHz]')
    plt.ylabel('Amplitude')

    # Plot frequency range at angle a
    plt.figure(1)
    plt.title('Normalized Calibration Error vs Frequency, \n Polarization=' + str(pol) + ', $\phi=$' + str(a))
    plt.plot(calVerify['frq'], calVerify[pol], label=r'$\mu=$' + str(stats[0]) + '\n $\sigma=$' + str(stats[1]))
    plt.grid(True)
    plt.xlabel('Frequency, [GHz]')
    plt.ylabel('Amplitude, [dB]')
    plt.legend()

    """Plot the Error over Angle"""
    calVerify = {}
    calVerify.update({'ph': _s_rcs['ph']})
    temp = np.abs(_m_rcs[pol][f, :]) / np.abs(_s_rcs[pol][f, :])
    calVerify.update({pol: 20 * np.log(temp)})

    stats = [np.mean(calVerify[pol]),
             np.std(calVerify[pol])
             ]
    stats = np.round_(stats, decimals=2)
    plt.figure(2)
    plt.title('Normalized RCS vs Angle, \n Polarization=' + str(pol) + ', $f=$' + str(f) + ' [GHz]')
    plt.plot(_s_rcs['ph'], _s_rcs[pol][f, :], label="Sim")
    plt.plot(_m_rcs['ph'], _m_rcs[pol][f, :], label="Meas")
    plt.grid(True)
    plt.xlabel(r'Angle, [$^{\circ}$]')
    plt.ylabel('Amplitude')

    # Plot frequency range at angle a
    plt.figure(3)
    plt.title('Normalized Calibration Error vs Angle, \n Polarization=' + str(pol) + ', f=' + str(f) + ' [GHz]')
    plt.plot(calVerify['ph'], calVerify[pol], label=r'$\mu=$' + str(stats[0]) + '\n $\sigma=$' + str(stats[1]))
    plt.grid(True)
    plt.xlabel(r'Angle, [$^{\circ}$]')
    plt.ylabel('Amplitude, [dB]')
    plt.legend()
