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
from fit_data_with_MCDDA_sptPALM import fit_data_with_MCDDA_sptPALM
import pickle

print("\nRun simulation_main.py!")

# Function for setting all parameters
sim_input = set_parameters_simulation();

# print("  TEMP! SPECIFIC FILE is being loaded: sim_input_parameter.pkl!")    
# filename = '/Users/hohlbein/Documents/WORK-DATA-local/Data_Finland/sim_input_parameter.pkl'
# with open(filename, 'rb') as f:
#     sim_input = pickle.load(f)

# # # set_parameters_simulation_GUI(sim_input)
sim_input = set_parameters_simulation_GUI(sim_input)

# Function for setting all starting positions, starting states etc
[particleData, sim_input] = initiate_simulation(sim_input);

# Function for moving particles and checking for state changes
[particleData, tracks] = diffusion_simulation(sim_input, particleData);

# Function to calculate diffusion coefficients for different track lengths
sorted_tracks = tracks.sort_values(by=['track_id', 'frame']) 
[D, D_track_length_matrix] = diff_coeffs_from_tracks_fast(sorted_tracks, sim_input);

# Function for plotting the data
plot_diff_histograms_tracklength_resolved(D_track_length_matrix, sim_input, D)

# Fit the experimental data
fit_data_with_MCDDA_sptPALM(D_track_length_matrix, sim_input)

