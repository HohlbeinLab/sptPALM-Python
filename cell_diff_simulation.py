#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

from define_parameters_simulation import define_parameters_simulation
from initiate_simulation import initiate_simulation
from particle_diffusion import particle_diffusion

print("\nRun single cell simulation!")
# Function for setting all parameters
sim_input = define_parameters_simulation();
    
# Function for setting all starting positions, starting states etc
[particleData, simInput] = initiate_simulation(sim_input);

#function for moving particles and checking for state changes
[particleData, tracks] = particle_diffusion(simInput, particleData);
