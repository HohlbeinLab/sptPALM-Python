#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 21:54:13 2024

@author: hohlbein
"""

def define_input_parameters():
    # Function defining all the input parameters and data to be analyzed
    
    input_parameter = {
        'dataPathName': '',
        'filename_thunderstormCSV': [],
        'filename_procBrightfield': [],
        'Condition_name': [],
        'Condition_files': [],
        'copyNumber_intervals': [],
        'pixelSize': 0.119,  #pixelsize of the camera (this is also set thunderstorm.ijm), default: ~0.117
        
        #Segmentation of cells allows linking localisations to individual cells
        'CellAreaPix_min': 50,  #filter cells for area (area is given in number of pixels), default: ~[10 300]
        'CellAreaPix_max': 600, #%filter cells for area (area is given in number of pixels), default: ~[10 300]
        'useSegmentations': True, #%still need to account for Playground.useSegmentations = false, default: true
        
        #Tracking parameters
        'trackStepLength_max': 800, #set tracking window (nm), default: 800nm
        'trackMemory': 0, #set tracking memory in frames, default: 1
        
        #%Diffusion analysis
        'frametime': 0.01, #frametime in seconds, default: 0.01
        'sigmaNoise': 0.03, # %localization error (um), default: 0.03
        'DiffHistSteps_min': 3, #minimum number of steps for a track to be analyzed --> Actual value/number of localisations is 1 higher than this!, default: 3
        'DiffHistSteps_max': 100, # %maximum number of steps for a track to be analyzed, deafult: 100
        
        #%Cell by cell analysis
        'numberTracksPerCell_min': 1, #minimum number of tracks that cell must contain, default: 1
        'numberTracksPerCell_max': 10000, # %maximum number of tracks, default 10000
        
        #(OPTIONAL) settings for visualisation of tracks SCTA: Single-cell tracking analysis
        #Old Matlab software, currently not used
        'SCTA_vis_cells': False, #%visualize individual cells true/false, default: false
        'SCTA_plotCellWindow': 15, #radius in pixels for plotting individual cells and their tracks
        'SCTA_vis_interactive': False, #%interactively cycle through cells true/false, default: false
        'SCTA_vis_rangemax': 0.4, # %color-coding in the range of [0:(vis_rangemax*inputParameter.plotDiffHist_max)], default: 0.4
        
        #histograms for diffusion analysis
        'ConversionFactor': 1E-6, #localisations are in nm. Diff coef => um^2/s, default: 1-E6
        'plotDiffHist_min': 4E-3, #plot and histogram from um^2/s to um^2/s, default: 4E-3
        'plotDiffHist_max': 10, #plot and histogram from um^2/s to um^2/s, default: 10
        
        #(OPTIONAL)settings for Normalized Increments analsis
        #JH: can;t remember what this is supoosed to to
        'NormIncAnalysis': False, #run  NormalizedIncrementsAnalysis true/false, default: false
        'NormInc_min_length': 10, #minimum length of tracks used for normalized increments analysis, deafult: 10
        'NormInc_windows': [1, 2, 10], #%time windows of normalized increments investigated, default: [1,2,10]

        
        #parameters for plotting figures
        'fontSize': 10, #%default: 10
        'lineWidth': 1, #default: 1
        'PlotNormHistograms': 'probability',#Carefull: Matlab: choose either 'count' (default) | 'probability' | 'countdensity' | 'pdf' | 'cumcount' | 'cdf'
        'ModDefineInputParameters': False, #%run DefineInputParameters.m in sptPALM_combineData.m true/false, default: false
        'plotFrameNumber': True, #%whether to plot the frame numbers next to the tracks in Plot_SingleCellTrackingAnalysis.m
        'Para1': {}  #structure that will later save all parameters and settings

    }

    # Directory containing your data
    input_parameter['dataPathName'] = '/Users/hohlbein/Documents/WORK-DATA-local/TestData_CRISPR-Cas/'

    # Name(s) of "_thunder.csv" files to be analyzed, separate with "," and start new line if required
    input_parameter['filename_thunderstormCSV'] = [
        #'9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv'
        'SHORT_9NTFixTL_LASER2_1_MMStack_Pos0.ome_thunder.csv'
    ]
    #name(s) of processed brightfield images for cell segmentation "*_procBrightfield.tif"
    #filename is also used to locate the segmented image and corresponding csv-table!)
    input_parameter['filename_procBrightfield'] = [
        '9NTFixTL_2_1_MMStack_Pos0.ome_procBrightfield.tif'
    ]

    # Name and assign your measurement conditions/files
    #1.2 (sptPALM_CombineData) Name and assing your measurement conditions/files
    input_parameter['Condition_name'].append('start')
    input_parameter['Condition_files'].append([1])  # refers to the order of files defined above

    # input_parameter['Condition_name'].append('standard')
    # input_parameter['Condition_files'].append([1,2])  # refers to the order of files defined above

    # Histogramming of diffusion coefficients per copynumber
    interval = 200
    for i in range(1, 6):
        input_parameter['copyNumber_intervals'].append([(i-1)*interval+1, i*interval])

    return input_parameter



