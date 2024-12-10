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
import numpy as np

# Function defining all the input parameters and data to be analyzed
def set_parameters_sptPALM():
    input_parameter = {
        'data_dir': '', # Directory where the data is found (selection via GUI or pre-defined, see below) 
        'default_output_dir': 'output_python/', # Initialise new directory to which analysed data is saved        
        'fn_locs': '',  # Initialise filename to the localisation data (selection via GUI or pre-defined, see below) 
        'fn_proc_brightfield': '', # Initialise filename to the brighfield data (selection via GUI or pre-defined, see below
        'fn_csv_handle': '_py_out.csv', # Will be used to name the csv file of the analysed data
        # 'fn_dict_handle': '_py_out.pkl', # Will be used to name the pickle file of the analysed data
        # 'fn_diffs_handle': '_diff_coeffs.csv', # Will be used to name the file of diffusion coefficients
        'fn_movies': 'sptData_movies.pkl', # Filename of 'movies' output
        'fn_combined_movies': 'sptData_combined_movies.pkl', # Filename of 'combined conditions' output
        
        'condition_names': [], # Initialise, further defined below
        'condition_files': [], # Initialise, further defined below
        'copynumber_intervals': [[1, 100], [101, 200], [201, 300], [301, 400]], # Initialise, further definied below        

        # Segmentation of cells allows linking localisations to individual cells
        'pixelsize': float(0.119),  # Pixelsize of the camera (this is also set in thunderstorm.ijm), default: ~0.119
        'use_segmentations': bool(True), # Account for segmentations = False, default: True
        'cellarea_pixels_min': int(50),  # Filter cells for minum area (area is given in number of pixels), default: 50
        'cellarea_pixels_max': int(500), # Filter cells for area (area is given in number of pixels), default: 500

        # Tracking and diffusion analysis
        'frametime': float(0.01), # Frametime in seconds, default: 0.01
        'loc_error': float(0.035), # Localization error (um), default: 0.03
        'track_steplength_max': float(0.8), # Tracking window (um), default: 0.8 um or 0.5 um
        'track_memory': int(0), # Tracking memory in frames, default: 1
        'diff_hist_steps_min': int(3), # Minimum number of steps for a track to be analyzed --> Actual value/number of localisations is 1 higher than this!, default: 3
        'diff_hist_steps_max': int(100), # Maximum number of steps for a track to be analyzed, default: 100
        # Track lengths and diffusion constraints (also track_lengths': [1,2,3,4,5,6,7,8])
        'tracklength_locs_min': int(2),  # 
        'tracklength_locs_max': int(8),  # 
        'tracklengths_steps':[], # further defined below
        # Cell by cell analysis
        'number_tracks_per_cell_min': int(1), # Minimum number of tracks for each cell, default: 1
        'number_tracks_per_cell_max': int(10000), # Maximum number of tracks for each cell, default: 10000

        # Histograms for diffusion analysis
        'plot_diff_hist_min': float(4E-3), # Plot and histogram from um^2/s to um^2/s, default: 4E-3
        'plot_diff_hist_max': float(10), # Plot and histogram from um^2/s to um^2/s, default: 10
        'binwidth': float(0.1), # width of bins, default: 0.1
        
        # Parameters for plotting figures etc
        'fontsize': int(10), # Default: 10
        'linewidth': int(1), # Default: 1
        'plot_norm_histograms': 'probability', # Carefull: Matlab: choose either 'count' (default) | 'probability' | 'countdensity' | 'pdf' | 'cumcount' | 'cdf'
        'plot_frame_number': bool(True), # Plot frame numbers next to the tracks in Plot_SingleCellTrackingAnalysis.m
        'dpi': int(150), # DPI setting for plotting figures, default: 300
        'cmap_applied': 'gist_ncar', ##was: 'nipy_spectral', tab20c, 
        'plot_option': 'logarithmic', # 'logarithmic', # How to plot x-axes either logarithmic or linear
        
        
        # (OPTIONAL) settings for visualisation of tracks SCTA: Single-cell tracking analysis
        'scta_vis_cells': bool(False), # Visualize individual cells True/False, default: False
        'scta_plot_cell_window': int(15), # Radius in pixels for plotting individual cells and their tracks
        'scta_vis_interactive': bool(False), # Interactively cycle through cells True/False, default: False
        'scta_vis_rangemax': float(0.3), # Color-coding in the range of [0:plot_DiffHist_max)], default: 0.4

    }
    input_parameter['tracklengths_steps'] = np.arange(input_parameter['tracklength_locs_min']-1,
                                            input_parameter['tracklength_locs_max'])
    
    # Directory containing your data
    input_parameter['data_dir'] = '/Users/hohlbein/Documents/WORK-DATA-local/TestData_CRISPR-Cas/'
    input_parameter['data_dir']  = os.path.join(input_parameter['data_dir'] , '')
    # Name(s) of "_thunder.csv" files to be analyzed, separate with "," and start new line if required
    input_parameter['fn_locs'] = [
        '9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv'
        # 'Short_9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv',
        # 'VeryShort_9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv',
    ]
    #name(s) of processed brightfield images for cell segmentation "*_procBrightfield.tif"
    #filename is also used to locate the segmented image and corresponding csv-table!)
    input_parameter['fn_proc_brightfield'] = [
        '9NTFixTL_2_1_MMStack_Pos0.ome_procBrightfield.tif'
    ]

    # Name and assign your measurement conditions/files
    #1.2 (sptPALM_CombineData) Name and assing your measurement conditions/files
    input_parameter['condition_names'] = ['Cond 1']
    input_parameter['condition_files'] = [[0]]  # refers to the order of files defined above
    
   # # DO NOT REMOVE THE FOLLOWING LINES!
   #  # Directory containing your data (make sure you end with a '/' or '\')
   #  input_parameter['data_dir'] = '/Users/hohlbein/Documents/WORK-DATA-local/Cas12a-data-JH/'
   #  input_parameter['data_dir']  = os.path.join(input_parameter['data_dir'] , '')
   #  # Name(s) of "_thunder.csv" files to be analyzed, separate with "," and start new line if required
   #  input_parameter['fn_locs'] = [
   #      '230208_Cas12aScrambled_EM620_LASER1_1_MMStack_Pos0.ome_MLE_thunder.csv',
   #      '230208_Cas12aScrambled_EM620_LASER1_2_MMStack_Pos0.ome_MLE_thunder.csv',
   #      '230131_Cas12aTargeting-0.15_EM620_LASER2_1_MMStack_Pos0.ome_MLE_thunder.csv',
   #      '230131_Cas12aTargeting-0.15_EM620_LASER2_2_MMStack_Pos0.ome_MLE_thunder.csv',
   #  ]
   #  #name(s) of processed brightfield images for cell segmentation "*_procBrightfield.tif"
   #  #filename is also used to locate the segmented image and corresponding csv-table!)
   #  input_parameter['fn_proc_brightfield'] = [
   #      '230208_Cas12aScrambled_EM620_1_1_MMStack_Pos0.ome_procBrightfield.tif',
   #      '230208_Cas12aScrambled_EM620_1_1_MMStack_Pos0.ome_procBrightfield.tif',
   #      '230131_Cas12aTargeting-0.15_EM620_2_1_MMStack_Pos0.ome_procBrightfield.tif',
   #      '230131_Cas12aTargeting-0.15_EM620_2_1_MMStack_Pos0.ome_procBrightfield.tif',
   #  ]

   #  input_parameter['condition_names'] = ['Cas12a_scrambled', 'Cas12a_targetting']
   #  input_parameter['condition_files'] = [[0,1],[2,3]]  # refers to the order of files defined above


    return input_parameter

