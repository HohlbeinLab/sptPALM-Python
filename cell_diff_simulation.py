#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

from define_parameters_simulation import define_parameters_simulation
from initiate_simulation import initiate_simulation
from particle_diffusion import particle_diffusion
from generate_D_from_tracks_sim import generate_D_from_tracks_sim

print("\nRun single cell simulation!")
# Function for setting all parameters
sim_input = define_parameters_simulation();
    
# Function for setting all starting positions, starting states etc
[particleData, sim_input] = initiate_simulation(sim_input);

#function for moving particles and checking for state changes
[particleData, tracks] = particle_diffusion(sim_input, particleData);



sorted_tracks = tracks.sort_values(by=['track_id', 'frame']) 


[D, DtrackLengthMatrix] = generate_D_from_tracks_sim(sorted_tracks, sim_input, max(sim_input['track_lengths']));

