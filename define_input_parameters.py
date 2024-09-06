#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 21:54:13 2024

@author: hohlbein
"""

# Function defining all the input parameters and data to be analyzed
def define_input_parameters():

    input_parameter = {
        'data_pathname': '',
        'filename_thunderstorm_csv': [],
        'filename_proc_brightfield': [],
        'condition_names': [],
        'condition_files': [],
        'copynumber_intervals': [],
        'pixel_size': 0.119,  # Pixelsize of the camera (this is also set in thunderstorm.ijm), default: ~0.119

        # Segmentation of cells allows linking localisations to individual cells
        'cellarea_pixels_min': 50,  # Filter cells for minum area (area is given in number of pixels), default: 50
        'cellarea_pixels_max': 500, # Filter cells for area (area is given in number of pixels), default: 500
        'use_segmentations': True, # Account for segmentations = False, default: True

        # Tracking parameters
        'track_steplength_max': 0.8, # Tracking window (um), default: 0.8um
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
        'conversion_factor': 1E-6, # Localisations are in nm. Diff coef => um^2/s, default: 1-E6
        'plot_diff_hist_min': 4E-3, # Plot and histogram from um^2/s to um^2/s, default: 4E-3
        'plot_diff_hist_max': 10, # Plot and histogram from um^2/s to um^2/s, default: 10
        
        # Parameters for plotting figures
        'fontsize': 10, # Default: 10
        'linewidth': 1, # Default: 1
        'plot_norm_histograms': 'probability', # Carefull: Matlab: choose either 'count' (default) | 'probability' | 'countdensity' | 'pdf' | 'cumcount' | 'cdf'
        'mod_define_input_parameters': False, #  Run DefineInputParameters.m in sptPALM_combineData.m True/False, default: False
        'plot_frame_number': True, # Plot frame numbers next to the tracks in Plot_SingleCellTrackingAnalysis.m
        'dpi': 300, # DPI setting for plotting figures, default: 300
        
        'para': {}  # Structure that will later save all parameters and settings
    }

    # Directory containing your data
    input_parameter['data_pathname'] = '/Users/hohlbein/Documents/WORK-DATA-local/TestData_CRISPR-Cas/'

    # Name(s) of "_thunder.csv" files to be analyzed, separate with "," and start new line if required
    input_parameter['filename_thunderstorm_csv'] = [
        #'9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv'
        'Short_9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv'
    ]
    #name(s) of processed brightfield images for cell segmentation "*_procBrightfield.tif"
    #filename is also used to locate the segmented image and corresponding csv-table!)
    input_parameter['filename_proc_brightfield'] = [
        '9NTFixTL_2_1_MMStack_Pos0.ome_procBrightfield.tif'
    ]

    # Name and assign your measurement conditions/files
    #1.2 (sptPALM_CombineData) Name and assing your measurement conditions/files
    input_parameter['condition_names'].append('start')
    input_parameter['condition_files'].append([1])  # refers to the order of files defined above
    
    # DO NOT REMOVE THE FOLLOWING LINES!
    # Copy or uncomment the following lines if necessary
    # input_parameter['Condition_name'].append('standard')
    # input_parameter['Condition_files'].append([1,2])  # refers to the order of files defined above

    # Histogramming of diffusion coefficients per copynumber
    INTERVAL = 200
    for i in range(1, 6):
        input_parameter['copynumber_intervals'].append([(i-1)*INTERVAL+1, i*INTERVAL])

    return input_parameter

