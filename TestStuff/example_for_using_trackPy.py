#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sept 01 20:58:09 2024

@author: hohlbein
"""

import trackpy as tp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from sdt import io, motion, config, helper

# Set random seed for reproducibility
np.random.seed(42)

# 1. Initialize Parameters
N_PARTICLES= 100 # Number of particles
FRAMES = 100  # Number of frames
BOX_SIZE = 1000  # Size of the box (100x100 pixels)

# 2. Initialize Particles with Random Distribution
initial_positions = np.random.rand(N_PARTICLES, 2) * BOX_SIZE  # Random positions in a 100x100 box

# 3. Simulate Brownian Motion for each Particle
# Generate random steps and compute cumulative sum for motion
steps = 3* np.random.randn(N_PARTICLES, FRAMES, 2)  # Random steps for Brownian motion
steps[:,:,1]=steps[:,:,1]+.5 #was used to introduce drift
positions = np.zeros((N_PARTICLES, FRAMES, 2))
positions[:, 0, :] = initial_positions  # Set initial positions

# Compute positions for all frames by adding random steps
for i in range(1, FRAMES):
    positions[:, i, :] = positions[:, i - 1, :] + steps[:, i, :]

# Convert to DataFrame
data = {
    'frame': np.repeat(np.arange(FRAMES), N_PARTICLES),
    'x': positions[:, :, 0].ravel(order='F'),  # Interleave positions correctly
    'y': positions[:, :, 1].ravel(order='F'),
    'particle': np.tile(np.arange(N_PARTICLES), FRAMES)
}
df = pd.DataFrame(data)

# 4. Link Positions to Form Trajectories
# Adjust `search_range` parameter to account for expected motion per frame
SEARCH_RANGE = 10 # Adjust based on expected displacement per frame
tp.quiet()
linked = tp.link_df(df, search_range=SEARCH_RANGE, memory=0)

# 5. Remove any remaining duplicates based on 'particle' and 'frame'
# might not be necessary
linked = linked.drop_duplicates(subset=['particle', 'frame'])

# 6. Filter out Short Trajectories
filtered = tp.filter_stubs(linked, threshold=10)

fig, ax = plt.subplots(2, 2)
ax[0, 0].set_title('Particle Trajectories')
ax[0, 0].set_ylabel('y')
ax[0, 0].set_xlabel('x')
ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal
tp.plot_traj(filtered, ax = ax[0,0])
# plt.show()

# very interesting: allows to calaculate and correct drift!!!
# Keep in mind!!!
d = tp.compute_drift(filtered)
d.plot(ax = ax[1, 0])
ax[1, 0].set_ylabel('y')
ax[1, 0].set_xlabel('x')
ax[1, 0].set_title('Drift')

filtered_drift_corrected = tp.subtract_drift(filtered.copy(), d)
tp.plot_traj(filtered_drift_corrected, ax = ax[0,1])
ax[0, 1].set_title('Particle Trajectories:drift corrected')
ax[0, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

# 7. Compute Mean Squared Displacement (MSD)
msd = tp.emsd(filtered_drift_corrected, mpp=1, fps=1)

# 8. Plot Mean Squared Displacement (MSD)
# plt.figure()
# plt.plot(msd.index, msd, 'o')
# plt.xscale('log')
# plt.yscale('log')
# plt.xlabel('Lag time')
# plt.ylabel('MSD')
# plt.title('Mean Squared Displacement')

ax[1, 1].set_title('Mean Squared Displacement: with fit')
ax[1, 1].set_ylabel(r'$\langle \Delta r^2 \rangle$ [pixel$^2$]')
plt.xlabel('lag time $t$')
fit = tp.utils.fit_powerlaw(msd, ax = ax[1,1])  # performs linear best fit in log space, plots]
print(fit)

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()



# Some additions from std tracking library. It does calculate something but doesn;t show a plot?!
# https://github.com/schuetzgroup/sdt-python-tutorials/blob/master/Diffusion%20constants.ipynb 
pixel_size = 0.16  # pixel size in μm
fps = 100  # frames per second
exposure_time = 0.004  # seconds

# Calculate ensemble MSDs and standard errors in 1000 rounds of bootstrapping

msd_result = motion.Msd(linked, fps, n_lag=10, n_boot=100, pixel_size=pixel_size)
m, e = msd_result.get_msd()

fit_result = msd_result.fit("brownian", n_lag=2, exposure_time=exposure_time)
fig, ax = plt.subplots()
fit_result.plot(ax=ax)
fit_result

