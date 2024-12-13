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
    print("\n Run 'set_parameters_simulation.py'")
    sim_input = {
    # Number of species and particles per species
    '#_species': [],  # number of species
    
    # Cell dimensions (in µm)
    'radius_cell': float(0.5),  # (µm) radius of the cap, edefault: 0.5
    'length_cell': float(2.0),    # (µm) length of the cylindrical part, default: 2.0
    
    # Track lengths and diffusion constraints (also track_lengths': [1,2,3,4,5,6,7,8])
    'tracklength_locs_min': int(2),  # Track lengths (2 to 8 frames) tracklength of 1 is two locs, or track_lengths': [1,2,3,4,5,6,7,8]
    'tracklength_locs_max': int(7),  # Track lengths (2 to 8 frames) tracklength of 1 is two locs, or track_lengths': [1,2,3,4,5,6,7,8]
    'tracklengths_steps':[], # further defined below
    'mean_track_length': float(4),  # Mean track length for exponential distribution, default 3
    
    # Simulation parameters
    'confined_diffusion': True,  # Confine diffusion within a cell
    'loc_error': float(0.035),  # (µm) Localization error (in µm), default: 0.035
    'correct_diff_calc_loc_error': True,  # Match anaDDA settings, default: False
    
    # Timing parameters
    'frametime': float(0.01),  # (s) frame time in seconds, default: 0.01
    'oversampling': int(10),  # oversampling factor for the frametime
    
    # Fitting and plotting options
    'perform_fitting': True,  # Whether to perform fitting or not
    'display_figures': False,  # Display figures/video
    'plot_diff_hist_min': float(0.004),  # Diffusion coefficient histogram min (µm^2/s), default: 0.004
    'plot_diff_hist_max': float(10.0),  # Diffusion coefficient histogram max (µm^2/s), deafult: 10.0
    'binwidth': float(0.1),  # Bin width for histogram, default 0.1
    'species_to_select': int(0), # For fitting, only one specis can be selected, set here which one, default:0
    'plot_option_axes': 'logarithmic', # 'logarithmic', # How to plot x-axes either logarithmic or linear
    'plot_option_save': 'png', # 'logarithmic', # How to plot x-axes either logarithmic or linear
    
    # Error handling values
    'avoidFloat0': float(1e-09),  # To avoid rates being exactly zero, default: 1e-09
   
    # Species-specific parameters
    'species': [], #defined below
   
   #Plotting stuff
   'dpi': int(150), # DPI setting for plotting figures, default: 300
   }
    
    sim_input['tracklengths_steps'] = np.arange(sim_input['tracklength_locs_min']-1,
                                            sim_input['tracklength_locs_max'])
    
    """
    sim_input.species(ii).diff_quot = [A, B, ...]; 
    Possibilities for states
    one state: sim_input.species(ii).rates = [0]
    two states: sim_input.species(ii).rates = [kAB, kBA]
    three states: sim_input.species(ii).rates = [kAB, kBA, kBC, kCB, kAC, kCA]
    four linear (!) states: sim_input.species(ii).rates = [kAB, kBA, kBC, kCB, kCD, kDC]
    """
  
    """
        # For fitting purposes
        species['diff_quot_init_guess'] = np.array([sim_input['avoidFloat0'], 1]) 
        species['diff_quot_lb_ub'] = np.array([[0, 1.], #was np.nan
                                                [2*sim_input['avoidFloat0'], 5.]])  #was np.nan
        species['rates_init_guess'] = species['rates']  # Initial guess for rates: fitting
        species['rates_lb_ub'] = np.array([species['rates']-1,
                                          species['rates']+1])  # Lower and upper bounds for rates
    """
  
    
    # Example species setup
    # species = {
    #     '#_states': 1,
    #     '#_particles': 500000,
    #     'diff_quot': np.array([2]),  # Diffusion coefficients for each state (µm^2/s)
    #     'rates': np.array([0]),     # Transition rates between states (1/s)
    # }
    # species['diff_quot_init_guess'] = species['diff_quot']   
    # species['diff_quot_lb_ub'] = np.array([[0], #was np.nan
    #                                         [2]])  #was np.nan
    # species['rates_init_guess'] = species['rates']  # Initial guess for rates: fitting
    # species['rates_lb_ub'] = np.array([[np.nan],
    #                                   [np.nan]])  # Lower and upper bounds for rates
    # sim_input['species'].append(species)
    
    # # Following part can be copied for every species to be simulated
    # species= {
    #     '#_states': 2,
    #     '#_particles': 50000,
    #     'diff_quot': np.array([sim_input['avoidFloat0'], 2]),  # Diffusion coefficients for each state (µm^2/s)
    #     # two states: sim_input.species(ii).rates = [kAB, kBA]
    #     'rates': np.array([40.0, 60.0])}   # Transition rates between states (1/s)
    #     # For fitting purposes
    # species['diff_quot_init_guess'] = np.array([sim_input['avoidFloat0'], 1]) 
    # species['diff_quot_lb_ub'] = np.array([[0, 1.], #was np.nan
    #                                         [2*sim_input['avoidFloat0'], 5.]])  #was np.nan
    # species['rates_init_guess'] = np.array([30.0, 80.0])  # Initial guess for rates: fitting
    # species['rates_lb_ub'] = np.array([[10.0, 10.0],
    #                                   [200.0, 500.0]])  # Lower and upper bounds for rates
    # sim_input['species'].append(species)
 

    # Following part can be copied for every species to be simulated
    species= {
        '#_states': 2,
        '#_particles': 100000,
        'diff_quot': np.array([sim_input['avoidFloat0'], 2]),  # Diffusion coefficients for each state (µm^2/s)
        # two states: sim_input.species(ii).rates = [kAB, kBA]
        'rates': np.array([40.0, 60.0])}   # Transition rates between states (1/s)
        # For fitting purposes
    species['diff_quot_init_guess'] = np.array([0, 2.2]) 
    species['diff_quot_lb_ub'] = np.array([[0, 1.], #was np.nan
                                            [2*sim_input['avoidFloat0'], 5.]])  #was np.nan
    species['rates_init_guess'] = np.array([20.0, 100.0])  # Initial guess for rates: fitting
    species['rates_lb_ub'] = np.array([[10.0, 10.0],
                                      [200.0, 500.0]])  # Lower and upper bounds for rates
    sim_input['species'].append(species)







    # # Following part can be copied for every species to be simulated
    # species = {
    #     '#_states': 3,
    #     '#_particles': 200000,
    #     'diff_quot': np.array([0, 0, 2.2]),  # Diffusion coefficients for each state (µm^2/s)
    #     # three states: sim_input.species(ii).rates = [kAB, kBA, kBC, kCB, kAC, kCA];
    #     # 'rates': np.array([143, 253, 272, 120, 0, 0])}   # Cas12a non-target Transition rates between states (1/s)
    #     # 'rates': np.array([160,192,100,70, 0, 0])}   # Cas9 non-target Transition rates between states (1/s)
    #      'rates': np.array([120,397,260,95, 0.0, 0.0])}   # impCas12a non-target Transition rates between states (1/s)
    # # For fitting purposes
    # species['diff_quot_init_guess'] = species['diff_quot']
    # species['diff_quot_lb_ub'] =  np.array([[0, 0, 1],
    #                                         [sim_input['avoidFloat0'], sim_input['avoidFloat0'], 5]])
    # # species['rates_init_guess'] = species['rates']  # Initial guess for rates
    # species['rates_init_guess'] = np.array([100,  200,  150 , 50 , 0.0, 0.0]) #species['rates']  # Initial guess for rates
    # species['rates_lb_ub'] =  np.array([[10, 10, 10, 10, 0 , 0],
    #                                   [500, 500, 500, 500, sim_input['avoidFloat0'], sim_input['avoidFloat0']]])  # Lower and upper bounds for rates
    # sim_input['species'].append(species)
    
    
    
    
    
    
    # # Following part can be copied for every species to be simulated
    # species = {
    #     '#_states': 4,
    #     '#_particles': 100000,
    #     'diff_quot': np.array([0, 0, 1.2, 2]),  # Diffusion coefficients for each state (µm^2/s)
    #     # four linear states: sim_input.species(ii).rates = [kAB, kBA, kBC, kCB, kCD, kDC];
    #     'rates': np.array([100, 400, 125, 40, 10, 10])}   # Transition rates between states (1/s)
    #     # For fitting purposes
    # species['diff_quot_init_guess'] = species['diff_quot'] 
    # species['diff_quot_lb_ub'] =  np.array([[np.nan, 0, 2],
    #                                         [np.nan, 2, 10]])  
    # species['rates_init_guess'] = species['rates']  # Initial guess for rates
    # species['rates_lb_ub'] =  np.array([[1, 1, 1, 1, 1, 1],
    #                                   [1000, 1000, 1000, 1000, 1000, 1000]])  # Lower and upper bounds for rates
    # sim_input['species'].append(species)
   

    sim_input['#_species'] = len(sim_input['species'])
    
    if sim_input['oversampling'] < 1:
        raise ValueError("Careful! sim_input['oversampling'] should be larger than 1")
    
    if sim_input['radius_cell'] < 0:
        raise ValueError("Careful! sim_input['radius_cell'] < 0!")
    
    if sim_input['length_cell'] < 0:
        raise ValueError("Careful! sim_input['length_cell'] < 0!")

    if sim_input['tracklength_locs_min'] < 2:
        raise ValueError("Careful! sim_input['tracklength_locs_min'] has to be 2 or highter !")
    
    # Check whether each species has a diffusion coefficient for every state
    for ii in range(sim_input['#_species']):
        species = sim_input['species'][ii]
        if len(species['diff_quot']) < species['#_states']:
            print(f"Problem with species number {ii + 1} encountered!")
            raise ValueError(f"Not enough diffusion coefficients for species {ii + 1}!")
        
        if species['#_states'] > 4:
            raise ValueError("More than 4 states are not supported!")
 
    return sim_input

