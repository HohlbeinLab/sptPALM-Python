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


# Function defining all the input parameters and data to be analyzed
def set_parameters_sptPALM():
    input_parameter = {
        'data_dir': '', # Directory where the data is found (selection via GUI or pre-defined, see below) 
        'default_output_dir': 'output_python/', # Initialise new directory to which analysed data is saved        
        'fn_locs': '',  # Initialise filename to the localisation data (selection via GUI or pre-defined, see below) 
        'fn_proc_brightfield': '', # Initialise filename to the brighfield data (selection via GUI or pre-defined, see below
        'fn_csv_handle': '_py_out.csv', # Will be used to name the csv file of the analysed data
        'fn_dict_handle': '_py_out.pkl', # Will be used to name the pickle file of the analysed data
        'fn_diffs_handle': '_diff_coeffs.csv', # Will be used to name the file of diffusion coefficients
        'fn_movies': 'sptData_movies.pkl', # Filename of movies output
        'fn_combined_movies': 'sptData_combined_movies.pkl', # Filename of combined conditions output
        
        'condition_names': [], # Initialise, further defined below
        'condition_files': [], # Initialise, further defined below
        # 'copynumber_intervals': [[1, 100], [101, 200], [201, 300], [301, 400]], # Initialise, further definied below

        # Segmentation of cells allows linking localisations to individual cells
        'pixelsize': 0.119,  # Pixelsize of the camera (this is also set in thunderstorm.ijm), default: ~0.119
        'use_segmentations': True, # Account for segmentations = False, default: True
        'cellarea_pixels_min': 50,  # Filter cells for minum area (area is given in number of pixels), default: 50
        'cellarea_pixels_max': 500, # Filter cells for area (area is given in number of pixels), default: 500

        # Tracking and diffusion analysis
        'frametime': 0.01, # Frametime in seconds, default: 0.01
        'loc_error': 0.035, # Localization error (um), default: 0.03
        'track_steplength_max': 0.5, # Tracking window (um), default: 0.8 um
        'track_memory': 0, # Tracking memory in frames, default: 1
        'diff_hist_steps_min': 3, # Minimum number of steps for a track to be analyzed --> Actual value/number of localisations is 1 higher than this!, default: 3
        'diff_hist_steps_max': 100, # Maximum number of steps for a track to be analyzed, default: 100
        'track_lengths': [1,2,3,4],  # Track lengths (2 to 8 frames) tracklength of 1 is two locs

        # Cell by cell analysis
        'number_tracks_per_cell_min': 1, # Minimum number of tracks for each cell, default: 1
        'number_tracks_per_cell_max': 10000, # Maximum number of tracks for each cell, default: 10000

        # Histograms for diffusion analysis
        'plot_diff_hist_min': 4E-3, # Plot and histogram from um^2/s to um^2/s, default: 4E-3
        'plot_diff_hist_max': 10, # Plot and histogram from um^2/s to um^2/s, default: 10
        'binwidth': 0.1, # width of bins, default: 0.1
        
        # Parameters for plotting figures etc
        'fontsize': 10, # Default: 10
        'linewidth': 1, # Default: 1
        'plot_norm_histograms': 'probability', # Carefull: Matlab: choose either 'count' (default) | 'probability' | 'countdensity' | 'pdf' | 'cumcount' | 'cdf'
        'plot_frame_number': True, # Plot frame numbers next to the tracks in Plot_SingleCellTrackingAnalysis.m
        'dpi': 150, # DPI setting for plotting figures, default: 300
        'cmap_applied': 'gist_ncar', ##was: 'nipy_spectral', tab20c, 
        
        # (OPTIONAL) settings for visualisation of tracks SCTA: Single-cell tracking analysis
        'scta_vis_cells': False, # Visualize individual cells True/False, default: False
        'scta_plot_cell_window': 15, # Radius in pixels for plotting individual cells and their tracks
        'scta_vis_interactive': False, # Interactively cycle through cells True/False, default: False
        'scta_vis_rangemax': 0.3, # Color-coding in the range of [0:plot_DiffHist_max)], default: 0.4

    }

    # # Directory containing your data
    # input_parameter['data_dir'] = '/Users/hohlbein/Documents/WORK-DATA-local/TestData_CRISPR-Cas/'

    # # Name(s) of "_thunder.csv" files to be analyzed, separate with "," and start new line if required
    # input_parameter['fn_locs'] = [
    #     '9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv'
    #     # 'Short_9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv',
    #     # 'VeryShort_9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv',
    # ]
    # #name(s) of processed brightfield images for cell segmentation "*_procBrightfield.tif"
    # #filename is also used to locate the segmented image and corresponding csv-table!)
    # input_parameter['fn_proc_brightfield'] = [
    #     '9NTFixTL_2_1_MMStack_Pos0.ome_procBrightfield.tif'
    # ]

    # # Name and assign your measurement conditions/files
    # #1.2 (sptPALM_CombineData) Name and assing your measurement conditions/files
    # input_parameter['condition_names'].append('Cond_1')
    # input_parameter['condition_files'].append([0])  # refers to the order of files defined above
    
    # DO NOT REMOVE THE FOLLOWING LINES!
    # Copy or uncomment the following lines if necessary
    # input_parameter['condition_names'].append('Cond_2')
    # input_parameter['condition_files'].append([0,1])  # refers to the order of files defined above

    # Directory containing your data (make sure you end with a '/' or '\')
    input_parameter['data_dir'] = '/Users/hohlbein/Documents/WORK-DATA-local/Cas12a-data-JH/'

    # Name(s) of "_thunder.csv" files to be analyzed, separate with "," and start new line if required
    input_parameter['fn_locs'] = [
        '230208_Cas12aScrambled_EM620_LASER1_1_MMStack_Pos0.ome_MLE_thunder.csv',
        '230208_Cas12aScrambled_EM620_LASER1_2_MMStack_Pos0.ome_MLE_thunder.csv',
        '230131_Cas12aTargeting-0.15_EM620_LASER2_1_MMStack_Pos0.ome_MLE_thunder.csv',
        '230131_Cas12aTargeting-0.15_EM620_LASER2_2_MMStack_Pos0.ome_MLE_thunder.csv',
    ]
    #name(s) of processed brightfield images for cell segmentation "*_procBrightfield.tif"
    #filename is also used to locate the segmented image and corresponding csv-table!)
    input_parameter['fn_proc_brightfield'] = [
        '230208_Cas12aScrambled_EM620_1_1_MMStack_Pos0.ome_procBrightfield.tif',
        '230208_Cas12aScrambled_EM620_1_1_MMStack_Pos0.ome_procBrightfield.tif',
        '230131_Cas12aTargeting-0.15_EM620_2_1_MMStack_Pos0.ome_procBrightfield.tif',
        '230131_Cas12aTargeting-0.15_EM620_2_1_MMStack_Pos0.ome_procBrightfield.tif',
    ]

    input_parameter['condition_names'] = ['Cas12a_scrambled', 'Cas12a_targetting']
    input_parameter['condition_files'] = [[0,1],[2,3]]  # refers to the order of files defined above

    # # Name and assign your measurement conditions/files
    # #1.2 (sptPALM_CombineData) Name and assing your measurement conditions/files
    # input_parameter['condition_names'].append('Cas12a_scrambled')
    # input_parameter['condition_files'].append([0,1])  # refers to the order of files defined above
    
    # # DO NOT REMOVE THE FOLLOWING LINES!
    # # Copy or uncomment the following lines if necessary
    # input_parameter['condition_names'].append('Cas12a_targetting')
    # input_parameter['condition_files'].append([2,3])  # refers to the order of files defined above



    # # Directory containing your data (make sure you end with a '/' or '\')
    # input_parameter['data_dir'] = '/Users/hohlbein/Documents/WORK-DATA-local/Cas12a-data-JH/'

    # # Name(s) of "_thunder.csv" files to be analyzed, separate with "," and start new line if required
    # input_parameter['fn_locs'] = [
    #     '230208_Cas12aScrambled_EM620_LASER1_1_MMStack_Pos0.ome_MLE_thunder.csv',
    #     '230208_Cas12aScrambled_EM620_LASER1_2_MMStack_Pos0.ome_MLE_thunder.csv',
    # ]
    # #name(s) of processed brightfield images for cell segmentation "*_procBrightfield.tif"
    # #filename is also used to locate the segmented image and corresponding csv-table!)
    # input_parameter['fn_proc_brightfield'] = [
    #     '230208_Cas12aScrambled_EM620_1_1_MMStack_Pos0.ome_procBrightfield.tif',
    #     '230208_Cas12aScrambled_EM620_1_1_MMStack_Pos0.ome_procBrightfield.tif',
    # ]

    # # Name and assign your measurement conditions/files
    # #1.2 (sptPALM_CombineData) Name and assing your measurement conditions/files
    # input_parameter['condition_names'].append('Cas12a_scrambled')
    # input_parameter['condition_files'].append([0,1])  # refers to the order of files defined above
    

    # Histogramming of diffusion coefficients per copynumber
    # INTERVAL = 100
    # for i in range(1, 6):
    #     input_parameter['copynumber_intervals'].append([(i-1)*INTERVAL+1, i*INTERVAL])

    return input_parameter


# MAYBE FOR LATER TO LOAD AND SAVE
# Prompt: https://chatgpt.com/g/g-SAbpLF1Ec-matlab-to-python/c/66f97248-8d68-8001-9b0c-04150a1b27d6
# import json

# # Define the default parameters in your function
# def default_parameters():
#     return {
#         'data_dir': '/Users/hohlbein/Documents/WORK-DATA-local/TestData_CRISPR-Cas/',
#         'default_output_dir': 'output_python/',
#         'fn_locs': [
#             'VeryShort_9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv',
#             'VeryShort_9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv'
#         ],
#         'fn_proc_brightfield': [
#             '9NTFixTL_2_1_MMStack_Pos0.ome_procBrightfield.tif'
#         ],
#         'fn_csv_handle': '_py_out.csv',
#         'fn_dict_handle': '_py_out.pkl',
#         'fn_diffs_handle': '_diff_coeffs.csv',
#         'fn_movies': 'sptData_movies.pkl',
#         'fn_combined_movies': 'sptData_combined_movies.pkl',
#         'condition_names': ['Cond_1', 'Cond_2'],
#         'condition_files': [[0, 1], [0, 1]],
#         'copynumber_intervals': [[1, 100], [101, 200], [201, 300], [301, 400], [401, 500]],
#         'pixelsize': 0.119,
#         'cellarea_pixels_min': 50,
#         'cellarea_pixels_max': 300,
#         'use_segmentations': True,
#         'track_steplength_max': 0.5,
#         'track_memory': 0,
#         'frametime': 0.01,
#         'sigma_noise': 0.03,
#         'diff_hist_steps_min': 3,
#         'diff_hist_steps_max': 100,
#         'number_tracks_per_cell_min': 2,
#         'number_tracks_per_cell_max': 10000,
#         'scta_vis_cells': False,
#         'scta_plot_cell_window': 15,
#         'scta_vis_interactive': False,
#         'scta_vis_rangemax': 0.3,
#         'plot_diff_hist_min': 4E-3,
#         'plot_diff_hist_max': 10,
#         'binwidth': 0.1,
#         'fontsize': 10,
#         'linewidth': 1,
#         'plot_norm_histograms': 'probability',
#         'plot_frame_number': True,
#         'dpi': 150,
#         'cmap_applied': 'gist_ncar',
#         'timeout': 10
#     }

# # Function to load parameters from a JSON file
# def load_parameters_from_json(file_path):
#     """Load parameters from a JSON file, with error handling."""
#     try:
#         with open(file_path, 'r') as f:
#             loaded_params = json.load(f)
#         print(f"Parameters loaded from {file_path}")
#         return loaded_params
#     except FileNotFoundError:
#         print(f"File {file_path} not found. Using default parameters.")
#         return None

# # Function to check if all required parameters are present
# def check_and_fill_parameters(loaded_params, default_params):
#     """Check if the loaded parameters are complete, fill missing ones with defaults."""
#     if loaded_params is None:
#         # If no parameters are loaded (e.g., file not found), return defaults
#         return default_params
    
#     # Check for missing keys
#     for key, default_value in default_params.items():
#         if key not in loaded_params:
#             print(f"Warning: Missing parameter '{key}'. Using default value.")
#             loaded_params[key] = default_value
    
#     # Check for extra keys
#     extra_keys = set(loaded_params.keys()) - set(default_params.keys())
#     if extra_keys:
#         print(f"Warning: Found unexpected parameters: {extra_keys}. They will be ignored.")
    
#     return loaded_params

# # Function to load and check parameters
# def set_parameters_sptPALM_json(param_file='params.json'):
#     """Main function to load and validate parameters."""
#     default_params = default_parameters()
    
#     # Load parameters from JSON
#     loaded_params = load_parameters_from_json(param_file)
    
#     # Check and complete the parameters
#     final_params = check_and_fill_parameters(loaded_params, default_params)
    
#     return final_params

# # Example of how this function can be used
# if __name__ == "__main__":
#     parameters = set_parameters_sptPALM('params.json')
#     print("Final parameters:", parameters)

