#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 21:54:13 2024

@author: hohlbein
"""
import numpy as np


# Function defining all the input parameters and data to be analyzed
def define_parameters_simulation():
    print('\nRun define_parameters_simulation.py')
    sim_input = {
    # Number of species and particles per species
    '#_species': 1,  # number of species
    '#_particles_per_species': [50000, 10000],  # particles per species
    
    # Cell dimensions (in µm)
    'radius_cell': 0.5,  # radius of the cap
    'length_cell': 2,    # length of the cylindrical part
    
    # Track lengths and diffusion constraints
    'track_lengths': np.arange(1, 9),  # Track lengths (1 to 8 frames)
    'mean_track_length': 3,  # Mean track length for exponential distribution
    
    # Simulation parameters
    'confined_diffusion': True,  # Confine diffusion within a cell
    'loc_error': 0.035,  # Localization error (in µm)
    'correct_diff_calc_loc_error': False,  # Match anaDDA settings
    
    # Timing parameters
    'steptime': 0.001,  # Step time in seconds
    'frametime': 0.01,  # Frame time in seconds
    
    # Fitting and plotting options
    'perform_fitting': False,  # Whether to perform fitting or not
    'display_figures': True,  # Display figures
    'plot_diff_hist_min': 0.004,  # Diffusion coefficient histogram min (µm^2/s)
    'plot_diff_hist_max': 10,  # Diffusion coefficient histogram max (µm^2/s)
    'binWidth': 0.1,  # Bin width for histogram
    'multiplicator': 20,  # Multiplicator to scale diffusion coefficients
    
    # Error handling values
    'avoidFloat0': 1e-09,  # To avoid rates being exactly zero
   
    # Species-specific parameters
    'species': []
    }
 
    ii = 0  # Initialize species index
 
    # simInput.species(ii).diffQuot = [A, B, ...]; 
    # Possibilities for states
    # one state
    #   simInput.species(ii).rates = [0];
    # two states
    #   simInput.species(ii).rates = [kAB, kBA];
    # three states
    #   simInput.species(ii).rates = [kAB, kBA, kBC, kCB, kAC, kCA];
    # four linear (!) states
    #   simInput.species(ii).rates = [kAB, kBA, kBC, kCB, kCD, kDC];

    
    # # Example species setup
    # species_1 = {
    #     '#_states': 1,
    #     'diff_quot': [2],  # Diffusion coefficients for each state (µm^2/s)
    #     'rates': [0],     # Transition rates between states (1/s)
    # }
    # # Append species to the list
    # sim_input['species'].append(species_1)
    
    
    species_2 = {
        '#_states': 2,
        'diff_quot': [0, 2],  # Diffusion coefficients for each state (µm^2/s)
        'rates': [60, 40],   # Transition rates between states (1/s)
        'diff_quot_init_guess': np.array([0, 2]) * sim_input['multiplicator'],
        'diff_quot_lb_ub': np.array([[np.nan, 0], [np.nan, 10]]) * sim_input['multiplicator'],
        'rates_init_Guess': [60, 40],  # Initial guess for rates
        'rates_lb_ub': np.array([[1, 1], [200, 200]]),  # Lower and upper bounds for rates
    }
     # Append species to the list
    sim_input['species'].append(species_2)
 
    
    # # Following part can be copied for every species to be simulated
    # ii = ii+1;                                             
    # simInput.species(ii).numberStates = 3; %number of states
    # simInput.species(ii).diffQuot = [0,1,2.2]; %diffusion coefficients for each state µm^2/s
    # simInput.species(ii).rates = [100,400,125,40,0,0];        %rates with in 1/s
    # # for fitting or comparison with experimental data
    # simInput.species(ii).diffQuot_initGuess = [0,0,2]*simInput.multiplicator; %initial guesses
    # simInput.species(ii).diffQuot_lb_ub = [nan,nan,nan; nan,nan,nan]*simInput.multiplicator; %lower bound and upper bound
    # simInput.species(ii).rates_initGuess = [80,500,505,90,0,0]; %initial guesses
    # simInput.species(ii).rates_lb_ub = [1,1,1,1,nan,nan; 1000,1000,1000,1000,nan,nan]; %lower bound and upper bound
    # Append species to the list
    sim_input['species'].append(species_2)   
    
    # # following part can be copied for every species to be simulated
    # ii = ii+1;                                             
    # simInput.species(ii).numberStates = 4; %number of states
    # simInput.species(ii).diffQuot = [0, 0, 0.1, 2]; %diffusion coefficients for each state µm^2/s
    # # for fitting or comparison with experimental data
    # simInput.species(ii).diffQuot_initGuess = [0, 0, 0, 2]*simInput.multiplicator; %initial guesses
    # simInput.species(ii).diffQuot_lb_ub = [0,0,0,0; 0,2,2,10]*simInput.multiplicator; %lower bound and upper bound
    # simInput.species(ii).rates_initGuess = [100,400,125,40,10,10]; %initial guesses
    # simInput.species(ii).rates_lb_ub = [0,0,0,0,0,0; 1000,1000,1000,1000,1000,1000]; %lower bound and upper bound
     # Append species to the list
    sim_input['species'].append(species_2)
    
 
    # Error checking for consistency
    if sim_input['#_species'] > len(sim_input['species']):
        raise ValueError("Number of species is larger than parameters provided for each species!")
    
    if sim_input['steptime'] >= sim_input['frametime']:
        raise ValueError("Careful! sim_input['steptime'] >= sim_input['frametime']!")
    
    if sim_input['radius_cell'] < 0:
        raise ValueError("Careful! sim_input['radius_cell'] < 0!")
    
    if sim_input['length_cell'] < 0:
        raise ValueError("Careful! sim_input['length_cell'] < 0!")
    
    # Check whether each species has a diffusion coefficient for every state
    for ii in range(sim_input['#_species']):
        species = sim_input['species'][ii]
        if len(species['diff_quot']) < species['#_states']:
            print(f"Problem with species number {ii + 1} encountered!")
            raise ValueError(f"Not enough diffusion coefficients for species {ii + 1}!")
        
        if species['#_states'] > 4:
            raise ValueError("More than 4 states are not supported!")
    
    # End of the simulation input setup
 
    return sim_input

