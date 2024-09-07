#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

#import tkinter as tk
from tkinter import simpledialog, filedialog
import os
# import sys
# import pandas as pd
from define_input_parameters import define_input_parameters


from load_csv import load_csv
from apply_cell_segmentation import apply_cell_segmentation
from tracking_analysis import tracking_analysis
# from diffusion_analysis import diffusion_analysis
# from Plot_Hist_DiffusionTracklength import plot_hist_diffusion_tracklength
# from SingleCellTrackingAnalysis import single_cell_tracking_analysis
# from Plot_SingleCellTrackingAnalysis import plot_single_cell_tracking_analysis
# from NormIncrements_Analysis import norm_increments_analysis


def sptPALM_analyse_movies():
    DATA = None
    # 1.1 Define input parameters
    print('\nrun define_input_parameters.py\n')
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
    if not input_parameter['fn_locs_csv']:
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
        if len(input_parameter['fn_locs_csv']) != len(input_parameter['fn_proc_brightfield']):
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
    temp_path = os.path.join(input_parameter['data_pathname'], input_parameter['default_output_folder'])
    print('temp_path')
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    # Display analysis parameters
    print('Print input_parameter')
    # Iterate through the dictionary and print each key-value pair on a new line
    for key, value in input_parameter.items():
        print(f" input_parameter.{key}: {value}")

    # 2. sptPALM data analysis (looping over each movie)
    DATA = {'MOVIES': []}

    for ii in range(len(input_parameter['fn_locs_csv'])):
        input_parameter['movie_number'] = ii #start with 0 not 1

        # 2.1 Initialisation of structure para (local analysis over one movie)
        #The structure para will contain all parameters and updated references to filenames and pathnames.
        para = input_parameter.copy() #Initialise data structure
        para['fn_locs_csv'] = input_parameter['fn_locs_csv'][ii]
        if input_parameter['fn_proc_brightfield']:
            para['fn_proc_brightfield'] = input_parameter['fn_proc_brightfield'][ii]
        else:
            para['fn_proc_brightfield'] = None

        os.chdir(para['data_pathname'])

        # 2.2 Loading and preparing localisation data
        print('\nRun load_csv.py\n')
        para = load_csv(para)

        # 2.3 Apply cell segmentation
        print('\nRun appllied_cell_segmentation.py\n')
        if input_parameter['use_segmentations']:
            para = apply_cell_segmentation(para)

        # 2.4 Perform tracking
        para = tracking_analysis(para)

        # 2.5 Calculate and plot diffusion coefficients
        # para = diffusion_analysis(para)
#         para = plot_hist_diffusion_tracklength(para)

#         # 2.6 Single Cell Tracking Analysis
#         if inputParameter['useSegmentations']:
#             para = single_cell_tracking_analysis(para)
#             para = plot_single_cell_tracking_analysis(para)

#         # 2.7 Optional Analysis of normalized increment distribution
#         if para.get('NormIncAnalysis', False):
#             para = norm_increments_analysis(para)

#         # 2.8 Save current analysis as Matlab workspace
#         saveFile = para['filename_analysis_csv'].replace('.csv', '')
#         save_path = os.path.join(inputParameter['dataPathOutp'], f"{saveFile}.mat")
#         shutil.copyfile(para['filename_thunderstormCSV'], save_path)

        # Cell array containing all para structs
        DATA['MOVIES'].append((para, para['fn_locs_csv']))

    # 3. Save entire DATA structure
    # save_path = os.path.join(input_parameter['data_output_folder'], input_parameter['fn_combined_data'])
    with open(temp_path + para['fn_combined_data'], 'w') as f:
        f.write(str(DATA))

    return DATA, input_parameter



