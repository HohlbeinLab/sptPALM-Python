#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This work is licensed under the CC BY 4.0 License.
You are free to share and adapt this work, even for commercial purposes,
as long as you provide appropriate credit to the original creator.

Original Creator: Johannes Hohlbein (Wageningen University & Research)
Date of Creation: September, 2024

Full license details can be found at https://creativecommons.org/licenses/by/4.0/
"""

from set_parameters_simulation import set_parameters_simulation
from set_parameters_simulation_GUI import set_parameters_simulation_GUI
from initiate_simulation import initiate_simulation
from diffusion_simulation import diffusion_simulation
from diff_coeffs_from_tracks_fast import diff_coeffs_from_tracks_fast
from plot_diff_histograms_tracklength_resolved import plot_diff_histograms_tracklength_resolved

print("\nRun simulation_main.py!")

# Function for setting all parameters
sim_input = set_parameters_simulation();

# set_parameters_simulation_GUI(sim_input)
sim_input = set_parameters_simulation_GUI(sim_input)

# Function for setting all starting positions, starting states etc
[particleData, sim_input] = initiate_simulation(sim_input);

# Function for moving particles and checking for state changes
[particleData, tracks] = diffusion_simulation(sim_input, particleData);

# Function to calculate diffusion coefficients for different track lengths
sorted_tracks = tracks.sort_values(by=['track_id', 'frame']) 
[D, D_track_length_matrix] = diff_coeffs_from_tracks_fast(sorted_tracks, sim_input, max(sim_input['track_lengths']));

# Function for plotting the data
# D_track_length_matrix.sum().sum()
# D.drop_duplicates('track_id'), 
plot_diff_histograms_tracklength_resolved(D_track_length_matrix, sim_input)



import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})



breakpoint()
# Create the data
rs = np.random.RandomState(1979)
x = rs.randn(500)
g = np.tile(list("ABCDEFGHIJ"), 50)
df = pd.DataFrame(dict(x=x, g=g))
m = df.g.map(ord)
df["x"] += m

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
g = sns.FacetGrid(df, row="g", hue="g", aspect=15, height=.5, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, "x",
      bw_adjust=.5, clip_on=False,
      fill=True, alpha=1, linewidth=1.5)
g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw_adjust=.5)

# passing color=None to refline() uses the hue mapping
g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)


# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)


g.map(label, "x")

# Set the subplots to overlap
g.figure.subplots_adjust(hspace=-.25)

# Remove axes details that don't play well with overlap
g.set_titles("")
g.set(yticks=[], ylabel="")
g.despine(bottom=True, left=True)