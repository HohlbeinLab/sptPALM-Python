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
import numpy as np


# Function defining all the input parameters and data to be analyzed
def set_parameters_simulation():
    print('\nRun set_parameters_simulation.py')
    sim_input = {
    # Number of species and particles per species
    '#_species': 1,  # number of species
    '#_particles_per_species': [200000, 960000],  # particles per species
    
    # Cell dimensions (in µm)
    'radius_cell': 0.5,  # (µm) radius of the cap, edefault: 0.5
    'length_cell': 2.0,    # (µm) length of the cylindrical part, default: 2.0
    
    # Track lengths and diffusion constraints (also track_lengths': [1,2,3,4,5,6,7,8])
    'tracklength_locs_min': 2,  # Track lengths (2 to 8 frames) tracklength of 1 is two locs, or track_lengths': [1,2,3,4,5,6,7,8]
    'tracklength_locs_max': 8,  # Track lengths (2 to 8 frames) tracklength of 1 is two locs, or track_lengths': [1,2,3,4,5,6,7,8]
    'mean_track_length': 10,  # Mean track length for exponential distribution, default 3
    
    # Simulation parameters
    'confined_diffusion': True,  # Confine diffusion within a cell
    'loc_error': 0.035,  # (µm) Localization error (in µm), default: 0.035
    'correct_diff_calc_loc_error': False,  # Match anaDDA settings, default: False
    
    # Timing parameters
    'steptime': 0.001,  # (s) step time in seconds, default: 0.001
    'frametime': 0.01,  # (s) frame time in seconds, default: 0.02
    
    # Fitting and plotting options
    'perform_fitting': True,  # Whether to perform fitting or not
    'display_figures': True,  # Display figures
    'plot_diff_hist_min': 0.004,  # Diffusion coefficient histogram min (µm^2/s), default: 0.004
    'plot_diff_hist_max': 10.0,  # Diffusion coefficient histogram max (µm^2/s), deafult: 10.0
    'binwidth': 0.1,  # Bin width for histogram, default 0.1
    'species_to_select': 0, # For fitting, only one specis can be selected, set here which one, default:0
    
    # Error handling values
    'avoidFloat0': 1e-09,  # To avoid rates being exactly zero, default: 1e-09
   
    # Species-specific parameters
    'species': [], #defined below
   
   #Plotting stuff
   'dpi': 150, # DPI setting for plotting figures, default: 300
   }
    
    sim_input['track_lengths'] = np.arange(sim_input['tracklength_locs_min']-1,
                                            sim_input['tracklength_locs_max'])
    
    """
    sim_input.species(ii).diff_quot = [A, B, ...]; 
    Possibilities for states
    one state: sim_input.species(ii).rates = [0]
    two states: sim_input.species(ii).rates = [kAB, kBA]
    three states: sim_input.species(ii).rates = [kAB, kBA, kBC, kCB, kAC, kCA]
    four linear (!) states: sim_input.species(ii).rates = [kAB, kBA, kBC, kCB, kCD, kDC]
    """
    
    # Example species setup
    # species = {
    #     '#_states': 1,
    #     'diff_quot': [0],  # Diffusion coefficients for each state (µm^2/s)
    #     'rates': [0],     # Transition rates between states (1/s)
    # }
    # sim_input['species'].append(species)
    
    # Following part can be copied for every species to be simulated
    # sim_input['avoidFloat0']
    species= {
        '#_states': 2,
        'diff_quot': np.array([sim_input['avoidFloat0'], 2.8]),  # Diffusion coefficients for each state (µm^2/s)
        # two states: sim_input.species(ii).rates = [kAB, kBA]
        'rates': np.array([155, 137])}   # Transition rates between states (1/s)
        # For fitting purposes
    species['diff_quot_init_guess'] = species['diff_quot']   
    species['diff_quot_lb_ub'] = np.array([[0, 1.], #was np.nan
                                            [2*sim_input['avoidFloat0'], 5.]])  #was np.nan
    species['rates_init_guess'] = species['rates']  # Initial guess for rates: fitting
    species['rates_lb_ub'] = np.array([[10.0, 10.0],
                                      [200.0, 500.0]])  # Lower and upper bounds for rates
    sim_input['species'].append(species)
 

    # # Following part can be copied for every species to be simulated
    # species = {
    #     '#_states': 3,
    #     'diff_quot': np.array([0, 0, 2.2]),  # Diffusion coefficients for each state (µm^2/s)
    #     # three states: sim_input.species(ii).rates = [kAB, kBA, kBC, kCB, kAC, kCA];
    #     'rates': np.array([120, 270, 250, 143, 0, 0])}   # Transition rates between states (1/s)
    #     # For fitting purposes
    # species['diff_quot_init_guess'] = species['diff_quot'] * sim_input['multiplicator']
    # species['diff_quot_lb_ub'] =  np.array([[np.nan, 0, 2],
    #                                         [np.nan, 2, 10]]) * sim_input['multiplicator']       
    # species['rates_init_guess'] = species['rates']  # Initial guess for rates
    # species['rates_lb_ub'] =  np.array([[1, 1, 1, 1, np.nan, np.nan],
    #                                   [1000, 1000, 1000, 1000, np.nan, np.nan]])  # Lower and upper bounds for rates
    # sim_input['species'].append(species)
    
    # # Following part can be copied for every species to be simulated
    # species = {
    #     '#_states': 4,
    #     'diff_quot': np.array([0, 0, 1.2, 2]),  # Diffusion coefficients for each state (µm^2/s)
    #     # four linear states: sim_input.species(ii).rates = [kAB, kBA, kBC, kCB, kCD, kDC];
    #     'rates': np.array([100, 400, 125, 40, 10, 10])}   # Transition rates between states (1/s)
    #     # For fitting purposes
    # species['diff_quot_init_guess'] = species['diff_quot'] * sim_input['multiplicator']
    # species['diff_quot_lb_ub'] =  np.array([[np.nan, 0, 2],
    #                                        [np.nan, 2, 10]]) * sim_input['multiplicator']       
    # species['rates_init_Guess'] = species['rates']  # Initial guess for rates
    # species['rates_lb_ub'] =  np.array([[1, 1, 1, 1, 1, 1],
    #                                  [1000, 1000, 1000, 1000, 1000, 1000]])  # Lower and upper bounds for rates
    # sim_input['species'].append(species)
    

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
 
    return sim_input

