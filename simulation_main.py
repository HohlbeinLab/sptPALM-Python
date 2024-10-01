#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

from set_parameters_simulation import set_parameters_simulation
from initiate_simulation import initiate_simulation
from diffusion_simulation import diffusion_simulation
from diff_coeffs_from_tracks_fast import diff_coeffs_from_tracks_fast
from plot_diff_histograms_tracklength_resolved import plot_diff_histograms_tracklength_resolved

print("\nRun simulation_main.py!")

# Function for setting all parameters
sim_input = set_parameters_simulation();
    
# Function for setting all starting positions, starting states etc
[particleData, sim_input] = initiate_simulation(sim_input);

# Function for moving particles and checking for state changes
[particleData, tracks] = diffusion_simulation(sim_input, particleData);

# Function to calculate diffusion coefficients for different track lengths
sorted_tracks = tracks.sort_values(by=['track_id', 'frame']) 

[D, D_track_length_matrix] = diff_coeffs_from_tracks_fast(sorted_tracks, sim_input, max(sim_input['track_lengths']));

# Functions for plotting the data
# D_track_length_matrix.sum().sum()
# D.drop_duplicates('track_id'), 
plot_diff_histograms_tracklength_resolved(D_track_length_matrix, sim_input)