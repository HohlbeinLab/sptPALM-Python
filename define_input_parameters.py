#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 21:54:13 2024

@author: hohlbein
"""

# Function defining all the input parameters and data to be analyzed
def define_input_parameters():
    print('\nRun define_input_parameters.py')
    input_parameter = {
        'data_dir': '', # Directory where the data is found (selection via GUI or pre-defined, see below) 
        'default_output_dir': 'output_python/', # Initialise new directory to which analysed data is saved        
        'fn_locs': '',  # Initialise filename to the localisation data (selection via GUI or pre-defined, see below) 
        'fn_proc_brightfield': '', # Initialise filename to the brighfield data (selection via GUI or pre-defined, see below
        'fn_csv_handle': '_py_save_csv.csv', # Will be used to name the csv file of the analysed data
        'fn_dict_handle': '_py_save_dict.json', # Will be used to name the jason file of the analysed data
        'fn_diffs_handle': '_diff_coeffs.csv', # Will be used to name the file of diffusion coefficients
        'fn_combined_data': 'sptDataMovies.json', # Filename of combined output

        
        'condition_names': [], # Initialise, further defined below
        'condition_files': [], # Initialise, further defined below
        'copynumber_intervals': [], # Initialise, further definied below

        'pixel_size': 0.119,  # Pixelsize of the camera (this is also set in thunderstorm.ijm), default: ~0.119

        # Segmentation of cells allows linking localisations to individual cells
        'cellarea_pixels_min': 50,  # Filter cells for minum area (area is given in number of pixels), default: 50
        'cellarea_pixels_max': 300, # Filter cells for area (area is given in number of pixels), default: 500
        'use_segmentations': True, # Account for segmentations = False, default: True

        # Tracking parameters
        'track_steplength_max': 0.5, # Tracking window (um), default: 0.8 um
        'track_memory': 0, # Tracking memory in frames, default: 1

        # Diffusion analysis
        'frametime': 0.01, # Frametime in seconds, default: 0.01
        'sigma_noise': 0.03, # Localization error (um), default: 0.03
        'diff_hist_steps_min': 3, # Minimum number of steps for a track to be analyzed --> Actual value/number of localisations is 1 higher than this!, default: 3
        'diff_hist_steps_max': 100, # Maximum number of steps for a track to be analyzed, default: 100

        # Cell by cell analysis
        'number_tracks_per_cell_min': 1, # Minimum number of tracks for each cell, default: 1
        'number_tracks_per_cell_max': 10000, # Maximum number of tracks for each cell, default: 10000

        # (OPTIONAL) settings for visualisation of tracks SCTA: Single-cell tracking analysis
        'scta_vis_cells': False, # Visualize individual cells True/False, default: False
        'scta_plot_cell_window': 15, # Radius in pixels for plotting individual cells and their tracks
        'scta_vis_interactive': False, # Interactively cycle through cells True/False, default: False
        'scta_vis_rangemax': 0.4, # Color-coding in the range of [0:(vis_rangemax*inputParameter.plotDiffHist_max)], default: 0.4

        # Histograms for diffusion analysis
        'plot_diff_hist_min': 4E-3, # Plot and histogram from um^2/s to um^2/s, default: 4E-3
        'plot_diff_hist_max': 10, # Plot and histogram from um^2/s to um^2/s, default: 10
        
        # Parameters for plotting figures
        'fontsize': 10, # Default: 10
        'linewidth': 1, # Default: 1
        'plot_norm_histograms': 'probability', # Carefull: Matlab: choose either 'count' (default) | 'probability' | 'countdensity' | 'pdf' | 'cumcount' | 'cdf'
        'mod_define_input_parameters': False, #  Run DefineInputParameters.m in sptPALM_combineData.m True/False, default: False
        'plot_frame_number': True, # Plot frame numbers next to the tracks in Plot_SingleCellTrackingAnalysis.m
        'dpi': 150, # DPI setting for plotting figures, default: 300
        'cmap_applied': 'gist_ncar', ##was: 'nipy_spectral', tab20c, 
        # 'para': {}  # Structure that will later save all parameters and settings
    }

    # Directory containing your data
    input_parameter['data_dir'] = '/Users/hohlbein/Documents/WORK-DATA-local/TestData_CRISPR-Cas/'

    # Name(s) of "_thunder.csv" files to be analyzed, separate with "," and start new line if required
    input_parameter['fn_locs'] = [
        # '9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv'
        'veryShort_9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv'
    ]
    #name(s) of processed brightfield images for cell segmentation "*_procBrightfield.tif"
    #filename is also used to locate the segmented image and corresponding csv-table!)
    input_parameter['fn_proc_brightfield'] = [
        '9NTFixTL_2_1_MMStack_Pos0.ome_procBrightfield.tif'
    ]

    # Name and assign your measurement conditions/files
    #1.2 (sptPALM_CombineData) Name and assing your measurement conditions/files
    input_parameter['condition_names'].append('start')
    input_parameter['condition_files'].append([1])  # refers to the order of files defined above
    
    # DO NOT REMOVE THE FOLLOWING LINES!
    # Copy or uncomment the following lines if necessary
    # input_parameter['condition_names'].append('standard')
    # input_parameter['condition_files'].append([1,2])  # refers to the order of files defined above

    # Histogramming of diffusion coefficients per copynumber
    INTERVAL = 200
    for i in range(1, 6):
        input_parameter['copynumber_intervals'].append([(i-1)*INTERVAL+1, i*INTERVAL])

    return input_parameter

