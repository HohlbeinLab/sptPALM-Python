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

# import tkinter as tk
# import sys
from tkinter import simpledialog, filedialog
from tkinter.simpledialog import askstring
import os
import pickle
import pandas as pd
import numpy as np

from set_parameters_sptPALM import set_parameters_sptPALM
from set_parameters_sptPALM_GUI import set_parameters_sptPALM_GUI
from load_localisations_from_csv import load_localisations_from_csv
from apply_cell_segmentation_sptPALM import apply_cell_segmentation_sptPALM
from tracking_sptPALM import tracking_sptPALM
from analyse_diffusion_sptPALM import analyse_diffusion_sptPALM
from plot_diffusion_tracklengths_sptPALM import plot_diffusion_tracklengths_sptPALM
from single_cell_analysis_sptPALM import single_cell_analysis_sptPALM
from plot_single_cell_analysis_sptPALM import plot_single_cell_analysis_sptPALM
from helper_functions import yes_no_input, string_input_with_default

def analyse_movies_sptPALM(input_parameter = None):
    """
    
    
    Parameters
    ----------
    input_parameter : DICT, optional
        Contains all settings on what data to load and how to process ur. The default is None.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    data : TYPE
        DESCRIPTION.
    input_parameter : TYPE
        DESCRIPTION.

    """
    
    
    print('\nRun analyse_movies_sptPALM.py')
    
    # 1.1 Define input parameters
    if not input_parameter:
        print("  Re-run set_parameters_sptPALM.py + GUI")
        input_parameter = set_parameters_sptPALM()
        input_parameter = set_parameters_sptPALM_GUI(input_parameter)
    
    # Fall-back to GUI if no list of ThunderSTORM.csv files 
    # '*_thunder_.csv' are specified in define_input_parameters.py
    if not input_parameter['fn_locs']:
        print('  Select *.csv data with GUI...')
        starting_directory = os.path.join(input_parameter['data_dir'],
                                          input_parameter['default_output_dir'])
        files = filedialog.askopenfilenames(
            initialdir = starting_directory, 
            title="Select *.csv from ThunderSTORM or other SMLM programs",
            filetypes=[("CSV files", "*_thunder.csv")])
        input_parameter['fn_locs'] = list(files)
        if files:
            # Overwrites inputParameter['data_pathname'] as defined in 'define_input_parameters.py'
            input_parameter['data_dir'] = os.path.dirname(files[0])
            os.chdir(input_parameter['data_dir'])
            
    # Check whether an equal number of files for localisations and segmentations was selected
    # in the SPECIAL CASE that several *_thunder.csv files, but only one brightfield image
    # were selected, ask whether to continue. If yes is chosen, this brightfiield image
    # is used for all loaded *_thunder.csv files.
    if input_parameter.get('use_segmentations'):
        if len(input_parameter['fn_locs']) != len(input_parameter['fn_proc_brightfield']):
            if len(input_parameter['fn_proc_brightfield']) == 1 and len(input_parameter['fn_locs']) > 1:
                print('  Only one brightfield image but >1 *.csv files were chosen!')
                if yes_no_input("  Do you want to continue? Default is yes", default="yes"):
                    temp = input_parameter['fn_proc_brightfield'][0]
                    input_parameter['fn_proc_brightfield'] = [temp] * len(input_parameter['fn_locs'])
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
    data['movies'] = {}
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
        para = load_localisations_from_csv(para)

        # 2.3 Apply cell segmentation
        if input_parameter['use_segmentations']:
            para = apply_cell_segmentation_sptPALM(para)

        # 2.4 Perform tracking
        para = tracking_sptPALM(para)

        # 2.5 Calculate and plot diffusion coefficients
        para = analyse_diffusion_sptPALM(para)
        para = plot_diffusion_tracklengths_sptPALM(para)

        # 2.6 Single Cell Tracking Analysis
        if input_parameter['use_segmentations']:
            para = single_cell_analysis_sptPALM(para)
            para = plot_single_cell_analysis_sptPALM(para)
        else:
            para['scta_table']= pd.DataFrame({
                    'cell_id', 
                    'cell_locs',
                    'cell_area',
                    '#tracks (filtered for #tracks per cell)',
                    'cum. #tracks (filtered for #tracks per cell)',
                    '#tracks (unfiltered for #tracks per cell)', 
                    'cum. #tracks (unfiltered for #tracks per cell)',
                    'keep_cells',
                    'average_diff_coeff_per_cell',
                })
        
        # 2.8 Save current analysis
        with open(temp_path + para['fn_locs'][:-4] + para['fn_dict_handle'], 'wb') as f:
            pickle.dump(para, f)
        print(f"  Parameter dictionary for current movie {ii} out of {len(input_parameter['fn_locs'])} movies(s) was saved as pickle file")
        # Cell array containing all para structs
        
        data['movies'][ii] = para
        
    # 3. Save entire DATA dictionary
    data['input_parameter'] = input_parameter
    with open(temp_path + para['fn_movies'], 'wb') as f:
        pickle.dump(data, f)
    print(f"Analysis of individual movie(s) saved as pickle file: {para['fn_movies']}")
        
    return data, input_parameter



