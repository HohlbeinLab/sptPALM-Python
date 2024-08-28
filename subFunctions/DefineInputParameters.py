#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 21:54:13 2024

@author: hohlbein
"""

import numpy as np
import os

def define_input_parameters():
    # Function defining all the input parameters and data to be analyzed
    
    # INITIALIZATION, DO NOT CHANGE!
    input_parameter = {
        'dataPathName': '',
        'filename_thunderstormCSV': [],
        'filename_procBrightfield': [],
        'Condition_name': [],
        'Condition_files': [],
        'copyNumber_intervals': [],
        'pixelSize': 0.119,
        'CellAreaPix_min': 50,
        'CellAreaPix_max': 600,
        'useSegmentations': True,
        'trackStepLength_max': 800,
        'trackMemory': 0,
        'frametime': 0.01,
        'sigmaNoise': 0.03,
        'DiffHistSteps_min': 3,
        'DiffHistSteps_max': 100,
        'numberTracksPerCell_min': 1,
        'numberTracksPerCell_max': 10000,
        'SCTA_vis_cells': False,
        'SCTA_plotCellWindow': 15,
        'SCTA_vis_interactive': False,
        'SCTA_vis_rangemax': 0.4,
        'ConversionFactor': 1E-6,
        'plotDiffHist_min': 4E-3,
        'plotDiffHist_max': 10,
        'NormIncAnalysis': False,
        'NormInc_min_length': 10,
        'NormInc_windows': [1, 2, 10],
        'fontSize': 10,
        'lineWidth': 1,
        'PlotNormHistograms': 'probability',
        'ModDefineInputParameters': False,
        'plotFrameNumber': True,
        'Para1': {}
    }

    # Directory containing your data
    input_parameter['dataPathName'] = '/Users/JH/Data/2022-07-31_LorenzoOliviData/2022-10-25/'

    # Name(s) of "_thunder.csv" files to be analyzed, separate with ";"
    input_parameter['filename_thunderstormCSV'] = [
        'EcoPAM_12aTpSC101-TL_20ngmL_LASER3_1_MMStack_Pos0.ome_first5kFrames_denoised_MLE_thunder.csv',
        'EcoPAM_12aTpSC101-TL_20ngmL_LASER3_1_MMStack_Pos0.ome_first5kFrames_MLE_thunder.csv'
    ]

    # Name(s) of processed brightfield images for cell segmentation "*_procBrightfield.tif"
    input_parameter['filename_procBrightfield'] = [
        'EcoPAM_12aTpSC101-TL_20ngmL_3_1_MMStack_Pos0.ome_procBrightfield.tif'
    ]

    # Name and assign your measurement conditions/files
    input_parameter['Condition_name'].append('denoised')
    input_parameter['Condition_files'].append([1])  # refers to the order of files defined above

    input_parameter['Condition_name'].append('standard')
    input_parameter['Condition_files'].append([2])  # refers to the order of files defined above

    # Histogramming of diffusion coefficients per copynumber
    interval = 200
    for i in range(1, 6):
        input_parameter['copyNumber_intervals'].append([(i-1)*interval+1, i*interval])

    return input_parameter

input_parameters = define_input_parameters()

