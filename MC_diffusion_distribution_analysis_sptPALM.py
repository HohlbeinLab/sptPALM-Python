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

import os
import pickle
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from set_parameters_sptPALM import set_parameters_sptPALM
from set_parameters_sptPALM_GUI import set_parameters_sptPALM_GUI
from set_parameters_simulation import set_parameters_simulation
from set_parameters_simulation_GUI import set_parameters_simulation_GUI
from initiate_simulation import initiate_simulation
from diff_coeffs_from_tracks_fast import diff_coeffs_from_tracks_fast
from plot_diff_histograms_tracklength_resolved import plot_diff_histograms_tracklength_resolved
from fit_data_with_MCDDA_sptPALM import fit_data_with_MCDDA_sptPALM

 # Assuming Para1 is a dictionary-like object
def MC_diffusion_distribution_analysis_sptPALM(comb_data=None, input_parameter=None, sim_input=None):
    print('\nRun MC_diffusion_distribution_analysis_sptPALM.py')

    """
    TEMPORARY: For bugfixing - Replace the following line with your file path if needed
    """
    
    print("  TEMP! SPECIFIC FILE is being loaded: input_parameter.pkl!")    
    filename = '/Users/hohlbein/Documents/WORK-DATA-local/Data_Finland/input_parameter.pkl'
    with open(filename, 'rb') as f:
        input_parameter = pickle.load(f)  
        
    print("  TEMP! SPECIFIC FILE is being loaded: sptData_combined_movies.pkl!")    
    # filename = '/Users/hohlbein/Documents/WORK-DATA-local/Cas12a-data-JH/output_python/sptData_combined_movies.pkl'
    filename = '/Users/hohlbein/Documents/WORK-DATA-local/Data_Finland/output_python/sptData_combined_movies.pkl'
    with open(filename, 'rb') as f:
        comb_data = pickle.load(f)

    # print("  TEMP! SPECIFIC FILE is being loaded: sim_input_parameter.pkl!")    
    # # filename = '/Users/hohlbein/Documents/WORK-DATA-local/Cas12a-data-JH/output_python/sptData_combined_movies.pkl'
    # filename = '/Users/hohlbein/Documents/WORK-DATA-local/Data_Finland/sim_input_parameter.pkl'
    # with open(filename, 'rb') as f:
    #     sim_input = pickle.load(f)
        
 
        
    """
    Actual start of the function
    """    
 
    # Check whether 'input_parameter' was passed to the function
    if not input_parameter:
        print("  Run set_parameters_sptPALM.py + GUI")
        input_parameter = set_parameters_sptPALM()
        input_parameter = set_parameters_sptPALM_GUI()
    
    # Check whether 'comb_data' was passed to the function
    if not comb_data:
        print("No 'comb_data' from option 3 available")
        print("Continue with GUI to select 'comb_data' such as 'sptData_combined_movies.pkl' or similar")
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
  
    # Check whether 'sim_input' was passed to the function
    if not sim_input:
        print("Run 'set_parameters_simulation.py' + GUI")
        sim_input = set_parameters_simulation()
        sim_input = set_parameters_simulation_GUI(sim_input)    
    
    print(f"  Running MCDDA on tracks assigned for condition: {comb_data['condition_names'][input_parameter['condition_to_select_MCDDA']]}\n")
    
    # Use tracks from anaDDA style of plotting tracks
    tracks = comb_data['anaDDA_tracks'][input_parameter['condition_to_select_MCDDA']]
    
    # Generate average diffusion coefficients for each track
    sorted_tracks = tracks.sort_values(by=['track_id', 'frame'])

    [D, D_track_length_matrix] = diff_coeffs_from_tracks_fast(sorted_tracks, sim_input);
    
    # Plot experimental data
    plot_diff_histograms_tracklength_resolved(D_track_length_matrix, sim_input, D)
 
    # TO DO: fact check size of track_lengths array
    # breakpoint()
    # len(sim_input['track_lengths'] == len(input_parameter['track_lengths']))
    
    # Initiate the simulation
    particle_data, sim_input = initiate_simulation(sim_input)
      
    # Fit the experimental data
    fit_data_with_MCDDA_sptPALM(D_track_length_matrix, sim_input)

    return comb_data    
    
