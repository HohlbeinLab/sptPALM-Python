#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


import os
import pickle
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from define_input_parameters import define_input_parameters
from define_parameters_simulation import define_parameters_simulation
from initiate_simulation import initiate_simulation

 # Assuming Para1 is a dictionary-like object
def sptPALM_MCDDA(condition, comb_data=None):


    print('\nRun sptPALM_MCDDA()')
    # loaded more as a dummy here: define input parameters
    # Best to use only 
    input_parameter = define_input_parameters()
    filename = []
    
    # TEMPORARY For bugfixing - Replace the following line with your file path if needed
    filename = '/Users/hohlbein/Documents/WORK-DATA-local/TestData_CRISPR-Cas/output_python/sptData_combined_movies.pkl'
    with open(filename, 'rb') as f:
        comb_data = pickle.load(f)
    
    # 1.1 Check whether DATA was passed to the function
    if comb_data is None:
        # Use Tkinter for file dialog
        Tk().withdraw()  # Close root window
        starting_directory = os.path.join(input_parameter['data_dir'],
                                                  input_parameter['default_output_dir'])
        filename = askopenfilename(initialdir = starting_directory, 
                                    filetypes = [("pickle file", "*.pkl")],
                                    title = "Select *.pkl file from sptPALM_combine_movies.py")
        if filename:
            with open(filename, 'rb') as f:
                comb_data = pickle.load(f)
        else:
            raise ValueError("No file selected!")
    else:
        print('  Careful, there might be no data available to proceed!')
           
    # Access the data fields
    condi_table_anaDDAtracks = comb_data['anaDDA_tracks']
    input_param = comb_data['input_parameter']
    
    print(f"  Running MCDDA on tracks assigned for ... {comb_data['condition_names'][condition]}\n")
    
    # Use tracks for anaDDA
    tracks = comb_data['anaDDA_tracks'][condition]
    
    # Set parameters for simulation
    sim_input = define_parameters_simulation()
    
    # Initiate the simulation
    particle_data, sim_input = initiate_simulation(sim_input)
    
    # # Generate average diffusion coefficients for each track
    # sorted_tracks = tracks[tracks[:, 3].argsort()]  # Sort rows by 4th column (MATLAB index 4 is Python index 3)
    # D, DtrackLengthMatrix = GenerateDfromtracks_Sim(sorted_tracks, sim_input, max(sim_input['trackLengths']) + 1)
    
    # # Plot final simulated data
    # plotDiffHistogram(D, sim_input)
    
    # # Fit the data
    # FitSimulatedData(D, DtrackLengthMatrix, sim_input)

    return comb_data    
    
