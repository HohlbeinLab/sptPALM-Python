#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

# import tkinter as tk
# import sys
from tkinter import simpledialog, filedialog
import os
import pickle

from define_input_parameters import define_input_parameters
from load_csv import load_csv
from apply_cell_segmentation import apply_cell_segmentation
from tracking_analysis import tracking_analysis
from diffusion_analysis import diffusion_analysis
from plot_hist_diffusion_track_length import plot_hist_diffusion_track_length
from single_cell_tracking_analysis import single_cell_tracking_analysis
from plot_single_cell_tracking_analysis import plot_single_cell_tracking_analysis
# from NormIncrements_Analysis import norm_increments_analysis


def sptPALM_analyse_movies():
    print('\nRun sptPALM_analyse_movies.py')
    # 1.1 Define input parameters
    input_parameter = define_input_parameters()
    
    # Allow savename to be changed (default: 'sptDataMovies.mat')
    # NOT NEEDED, REMEMBER FOR LATER
    # root = tk.Tk()
    # root.withdraw()  # Hide the root window    
    # prompt = "Enter new name for saving sptDataMovies.mat or press OK/Enter"
    # inputParameter['dataFileNameMat'] = simpledialog.askstring("Rename sptDataMovies.mat?", prompt, initialvalue='sptDataMovies.mat')
   
 #TEMPORARILY DISABLED (to avoid pausing execution of the analysis}
    # fn_output_default = input_parameter['fn_combined_data']
    # user_input = input(f"  Enter string or press enter (default is: {n_output_default}): ")
    # if not user_input:
    #      user_input = fn_output_default 
    # input_parameter['fn_combined_output'] = user_input
      
    
    # Fall-back to GUI if no list of ThunderSTORM.csv files 
    # '*_thunder_.csv' are specified in DefineInputParameters.m
    if not input_parameter['fn_locs']:
        files = filedialog.askopenfilenames(
            title="Select *.csv from ThunderSTORM or other SMLM programs",
            filetypes=[("CSV files", "*_thunder.csv")])
        input_parameter['fn_locs_csv'] = list(files)
        if files:
            # Overwrites inputParameter['data_pathname'] as defined in 'define_inpuit_parameters.py'
            input_parameter['data_pathname'] = os.path.dirname(files[0])
            os.chdir(input_parameter['data_pathname'])
            
    # Check whether an equal number of files for localisations and segmentations was selected
    # in the SPECIAL CASE that several *_thunder.csv files, but only one brightfield image
    # were selected, ask wether to continue. If yes is chosen, this brightfiield image
    # is used for all loaded *_thunder.csv files.
    if input_parameter.get('use_segmentations'):
        if len(input_parameter['fn_locs']) != len(input_parameter['fn_proc_brightfield']):
            if len(input_parameter['fn_proc_brightfield']) == 1 and len(input_parameter['fn_locs_csv']) > 1:
                print('Only one brightfield image but >1 CSV files were chosen!')
                proceed = simpledialog.askinteger("Continue?", "Enter 1 to continue or 0 to cancel:", initialvalue=1)
                if proceed == 1:
                    temp = input_parameter['fn_proc_brightfield'][0]
                    input_parameter['fn_proc_brightfield'] = [temp] * len(input_parameter['fn_locs_csv'])
                else:
                    raise Exception('User chose to cancel the process.')
            else:
                raise Exception('Select an equal number of files for localisations and segmentations!')

    # Create OUTPUT folder if it doesn't yet exist
    temp_path = os.path.join(input_parameter['data_dir'], input_parameter['default_output_dir'])
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    # Display analysis parameters
    print('  Show input_parameter')
    # Iterate through the dictionary and print each key-value pair on a new line
    for key, value in input_parameter.items():
        print(f"    .{key}: {value}")

    # 2. sptPALM data analysis (looping over each movie)
    data = {}
    for ii in range(len(input_parameter['fn_locs'])):
        input_parameter['movie_number'] = ii #start with 0 not 1

        # 2.1 Initialisation of dictionary para (local analysis over one movie)
        # Para will contain all parameters and updated references to filenames and pathnames.
        para = input_parameter.copy() #Initialise data structure
        para['fn_locs'] = input_parameter['fn_locs'][ii]
        if input_parameter['fn_proc_brightfield']:
            para['fn_proc_brightfield'] = input_parameter['fn_proc_brightfield'][ii]
        else:
            para['fn_proc_brightfield'] = None

        os.chdir(para['data_dir'])

        # 2.2 Loading and preparing localisation data
        para = load_csv(para)

        # 2.3 Apply cell segmentation
        if input_parameter['use_segmentations']:
            para = apply_cell_segmentation(para)

        # 2.4 Perform tracking
        para = tracking_analysis(para)

        # 2.5 Calculate and plot diffusion coefficients
        para = diffusion_analysis(para)
        para = plot_hist_diffusion_track_length(para)

        # 2.6 Single Cell Tracking Analysis
        if input_parameter['use_segmentations']:
            para = single_cell_tracking_analysis(para)
            para = plot_single_cell_tracking_analysis(para)

#         # 2.7 Optional Analysis of normalized increment distribution
#         if para.get('NormIncAnalysis', False):
#             para = norm_increments_analysis(para)

        # # 2.8 Save current analysis as Matlab workspace
        # saveFile = para['filename_analysis_csv'].replace('.csv', '')
        # save_path = os.path.join(temp_path, f"{saveFile}")
        # with open(save_path, 'wb') as f:
        #     pickle.dump(para, f)
        # print('Para dictionary for current movie was saved as pickle file')

        # Cell array containing all para structs
        data[ii] = para

    # 3. Save entire DATA dictionary
    with open(temp_path + para['fn_combined_data'], 'wb') as f:
        pickle.dump(data, f)
    print('Complete data (all movies) saved as pickle file')
    
    ## To open the data:
    # with open(temp_path + para['fn_combined_data'] + '.pkl', 'rb') as f:
    #     data_loaded = pickle.load(f)
        
    return data, input_parameter, para



