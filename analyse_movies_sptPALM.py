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
import pandas as pd

from set_parameters_sptPALM import set_parameters_sptPALM
from set_parameters_sptPALM_GUI import set_parameters_sptPALM_GUI
from load_localisations_from_csv import load_localisations_from_csv
from apply_cell_segmentation_sptPALM import apply_cell_segmentation_sptPALM
from tracking_sptPALM import tracking_sptPALM
from analyse_diffusion_sptPALM import analyse_diffusion_sptPALM
from plot_diffusion_tracklengths_sptPALM import plot_diffusion_tracklengths_sptPALM
from single_cell_analysis_sptPALM import single_cell_analysis_sptPALM
from plot_single_cell_analysis_sptPALM import plot_single_cell_analysis_sptPALM
from diff_coeffs_from_tracks_fast import diff_coeffs_from_tracks_fast
from plot_diff_histograms_tracklength_resolved import plot_diff_histograms_tracklength_resolved
from helper_functions import yes_no_input

def analyse_movies_sptPALM(input_parameter = None):
    """
    analyse_movies_sptPALM.py: main function to analyse each movie based on the settings in 'input_parameter' 
    
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
    data : dict
        Dictionary containing all processed experimental of each slected movie.
    input_parameter : dict
        Potentially updated input_parameter.

    """
       
    print('\nRun analyse_movies_sptPALM.py')
    
    print("  TEMP! SPECIFIC FILE is being loaded: input_parameter.pkl!")    
    # filename = '/Users/hohlbein/Documents/WORK-DATA-local/Data_Finland/input_parameter.pkl'
    filename = '/Users/hohlbein/Documents/WORK-DATA-local/2024-TypeIII/input_parameter_single.pkl'
    with open(filename, 'rb') as f:
        input_parameter = pickle.load(f)    
 
       
    """ 1. Define input parameters """
    if not input_parameter:
        print("  Re-run set_parameters_sptPALM.py + GUI")
        input_parameter = set_parameters_sptPALM()
        input_parameter = set_parameters_sptPALM_GUI(input_parameter)
    
    # Check whether an equal number of files for localisations and segmentations was selected
    # in the SPECIAL CASE that several *_thunder.csv files, but only one brightfield image
    # were selected, ask whether to continue. If 'yes' is chosen, this brightfiield image
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

    # Display input parameters
    print('  Show input_parameter')
    for key, value in input_parameter.items():
        print(f"    .{key}: {value}")

    """ 2. sptPALM data analysis (looping over each single movie) """
    data = {}
    data['movies'] = {}
    for ii in range(len(input_parameter['fn_locs'])):
        input_parameter['movie_number'] = ii # Python: start with 0 not 1

        """ 2.1 Initialisation of dictionary 'para' (local analysis over one movie) """
        para = input_parameter.copy() # Initialise data structure
        para['fn_locs'] = input_parameter['fn_locs'][ii]
        if input_parameter['fn_proc_brightfield']:
            para['fn_proc_brightfield'] = input_parameter['fn_proc_brightfield'][ii]
        else:
            para['fn_proc_brightfield'] = None

        os.chdir(para['data_dir'])

        """ 2.2 Loading and preparing localisation data """
        para = load_localisations_from_csv(para)

        """ 2.3 Apply cell segmentation """
        if input_parameter['use_segmentations']:
            para = apply_cell_segmentation_sptPALM(para)

        """ 2.4 Perform tracking: 
         returns para['tracks']: x[µm), y[µm]], frame, track_id, frametime """
        para = tracking_sptPALM(para)

        """ 2.5 Calculate and plot diffusion coefficients: 
         returns para['diff_coeffs_filtered_list']: 
            'diff_coeffs_filtered',
            'track_length_filtered': track_ids_length_filtered[:, 1],
            'track_id': track_ids_length_filtered[:, 0] """
        # OLD:        
        # para = analyse_diffusion_sptPALM(para)

        # tracks: x[µm), y[µm]], frame, track_id, frametime
        # D: tracks + #_loc, MSD, D_coeff
        # D_track_length_matrix: Bins, steps[2-3]
        [D, D_track_length_matrix] = diff_coeffs_from_tracks_fast(para['tracks'], input_parameter);
     
        # Plot experimental data
        plot_diff_histograms_tracklength_resolved(D_track_length_matrix, input_parameter, D)
        
        para = plot_diffusion_tracklengths_sptPALM(para)

        """ 2.6 [Optional] SCTA Single Cell Tracking Analysis """
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
        
        """ 2.7 Save current analysis of a single movie """
        # with open(temp_path + para['fn_locs'][:-4] + para['fn_dict_handle'], 'wb') as f:
        #     pickle.dump(para, f)
        # print(f"  Parameter dictionary for current movie {ii} out of {len(input_parameter['fn_locs'])} movies(s) was saved as pickle file")
        
        # Cell array containing all para structs
        data['movies'][ii] = para
        
    """ 3. Save entire DATA dictionary """
    data['input_parameter'] = input_parameter
    
    with open(temp_path + para['fn_movies'], 'wb') as f:
        pickle.dump(data, f)
    print(f"Analysis of individual movie(s) saved as pickle file: {para['fn_movies']}")
        
    return data, input_parameter



