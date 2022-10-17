# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 12:48:03 2022

@author: Administrator
"""

"""
=============================================
Generate polygons to fill under 3D line graph
=============================================

Demonstrate how to create polygons which fill the space under a line
graph. In this example polygons are semi-transparent, creating a sort
of 'jagged stained glass' effect.
"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl

def pull_colors(_a, _cmap):
    cmap = _cmap
    idx = np.linspace(0, cmap.N, len(_a))/cmap.N # normalize between 0 and 1
    cmap = cmap(idx)
    colors = []
    for c in cmap:
        colors.append(matplotlib.colors.rgb2hex(c))
    
    return colors
# End color selection

plt.close('all')
plt.rcParams.update({'font.size': 22})

target_file = 'G:\Rofrano_Thesis\Project\data\m_prolate_norm_f.obj'
file = open(target_file,'rb')
s_prolate_norm_f = pkl.load(file)
file.close()

"""Build the figure"""
# fig = plt.figure()
# ax = plt.axes(projection='3d')

pol = 'tt'

"""Pull in the norm-over-f data"""
f_norm = s_prolate_norm_f.copy()
f_norm_m = np.mean(f_norm[pol], axis=0)
f_norm_s = np.var(f_norm[pol], axis=0)
f_norm_A = np.max(f_norm[pol], axis=0)
N = len(f_norm_A)

"""Plot the Frequency Normed Amplitudes over a surface"""
fig = plt.figure("Amplitude Surface")
ax = plt.subplot(111, projection='3d')
a = f_norm['ph']
f = f_norm['frq']
A, F = np.meshgrid(a, f)
surf = ax.plot_surface(F, A, np.asarray(f_norm['tt']), cmap='magma')
ax.set_xlabel('Frequency, [GHz]')
ax.set_ylabel('Angle, [$^{\circ}$]')
ax.set_zlabel('Amplitude')
ax.set_title('Amplitude over Angle for Frequency-Normalized Data, \
             \n Pol='+pol)
ax.xaxis.labelpad = 20
ax.yaxis.labelpad = 20
ax.zaxis.labelpad = 20
ax.view_init(elev=35., azim=-155)
fig.set_tight_layout('tight')
fig.colorbar(surf, shrink=0.5, aspect=5)



x = np.linspace(9.5, 10.5, N)
p = lambda x, A, m, s: A*np.exp(-(x-m)**2/(2*s**2))
s_fac = 1
pdfs = []
for n in range(N):
    pdfs.append(p( x, f_norm_A[n], f_norm_m[n], f_norm_s[n]*s_fac))


fig = plt.figure("PDF Surface")
ax = plt.subplot(111, projection='3d')
y = np.arange(0, 360, 1)
X, Y = np.meshgrid(x, y)
surf = ax.plot_surface(X, Y, np.asarray(pdfs), cmap='magma')
ax.set_xlabel('Pdf Bin')
ax.set_ylabel('Angle, [$^{\circ}$]')
ax.set_zlabel('Amplitude')
ax.set_title('PDF over Angle for Frequency-Normalized Data,\
             \n $\sigma*$'+str(s_fac)+', Pol='+pol)
ax.xaxis.labelpad = 20
ax.yaxis.labelpad = 20
ax.zaxis.labelpad = 20
ax.view_init(elev=35., azim=-155)
fig.set_tight_layout('tight')
fig.colorbar(surf, shrink=0.5, aspect=5)




# f_frq = f_norm['frq']
# f_norm = f_norm['tt']

# a = 10

# f_norm = [f_norm[:, a], f_norm[:, 180]]#f_norm[:, 80], f_norm[:, 180], f_norm[:, 260]]
# f_norm_m = []
# f_norm_s = []
# # Zip creates an array of tuple pairs (t[i], f[i]) needed for the collection
# f_array = []
# for f in f_norm:
#     f_array.append(list(zip(f_frq, f)))
#     f_norm_m.append(list(zip(f_frq, np.mean(f)*np.ones(len(f)))))
#     f_norm_s.append(list(zip(f_frq, np.std(f)*np.ones(len(f)))))

# """Plot the amplitude and stats per angle"""
# fig, ax = plt.subplots(1, 2)

# fig.suptitle('Angle-Normalized Amplitude vs Frequency, \n $\phi = $'+str(a)+' [$^{\circ}$]')
# ax[0].plot(*zip(*f_array[0]), label='Amplitude')
# ax[0].plot(*zip(*f_norm_m[0]), label='$\mu = $'+str(np.round_(f_norm_m[0][0][1], decimals=2)))
# ax[0].plot(*zip(*f_norm_s[0]), label='$\sigma = $'+str(np.round_(f_norm_s[0][0][1], decimals=2)))
# ax[0].grid(True)

# A = np.max(list(zip(*f_array[0]))[1])
# mean = np.max(list(zip(*f_norm_m[0]))[1])
# dev = np.max(list(zip(*f_norm_s[0]))[1])
# x = np.linspace(-1, 1, 1000)
# p = A*np.exp(-(x-mean)**2/(2*dev**2))
# ax[1].plot(x, p)
# plt.legend()
# plt.show()


# """Construct the PolyCollection Object"""
# colors = pull_colors(f_array, cm.magma) # Grab colors from known colormap
# poly1 = PolyCollection(f_array, facecolors=colors)
# # poly2 = PolyCollection(f_norm_m, facecolors=colors)
# # poly3 = PolyCollection(f_norm_s, facecolors=colors)
# poly1.set_alpha(0.5)


# """Set Collection locations, and adjust the plots"""
# zs = [0, 0.25]#list(np.arange(1, len(f_array)+1, 1))
# ax.add_collection3d(poly1, zs=zs, zdir='y')
# # ax.add_collection3d(poly2, zs=zs, zdir='y')
# # ax.add_collection3d(poly3, zs=zs, zdir='y')
# ax.set_xlabel('Frequency, [GHz]')
# ax.set_xlim3d(f_frq[0], f_frq[-1])
# ax.set_xticks(np.arange(f_frq[0], f_frq[-1], 0.25))
# ax.set_ylabel('Angle Slice')
# ax.set_ylim3d(zs[0], zs[-1])
# ax.set_yticks(zs)
# ax.set_zlabel('Amplitude, [norm]')
# # ax.set_zlim3d(0, 1)
# # ax.set_zticks([0, 0.5, 1])
# ax.grid()

plt.show()


