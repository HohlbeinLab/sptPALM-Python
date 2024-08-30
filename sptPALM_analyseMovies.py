#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

import tkinter as tk
from tkinter import simpledialog, filedialog
import os
import sys

from DefineInputParameters import define_input_parameters


from Convert_csv import convert_csv
from ApplyCellSegmentation import apply_cell_segmentation
# from TrackingAnalysis import tracking_analysis
# from DiffusionAnalysis import diffusion_analysis
# from Plot_Hist_DiffusionTracklength import plot_hist_diffusion_tracklength
# from SingleCellTrackingAnalysis import single_cell_tracking_analysis
# from Plot_SingleCellTrackingAnalysis import plot_single_cell_tracking_analysis
# from NormIncrements_Analysis import norm_increments_analysis


def sptPALM_analyse_Movies():
    DATA = None
    # 1.1 Define input parameters
    print('Run DefineInputParameters()')
    inputParameter = define_input_parameters()
    
    # Allow savename to be changed (default: 'sptDataMovies.mat')
    
    # root = tk.Tk()
    # root.withdraw()  # Hide the root window    
    # prompt = "Enter new name for saving sptDataMovies.mat or press OK/Enter"
    # inputParameter['dataFileNameMat'] = simpledialog.askstring("Rename sptDataMovies.mat?", prompt, initialvalue='sptDataMovies.mat')
    
    input_default = 'sptDataMovies.matPy'
    user_input = input("  Enter string or press enter (default is: '"+input_default+"'): ")
    if not user_input:
        user_input = input_default 
    inputParameter['dataFileNameMat'] = user_input
      
    # # Convert to string if it's None
    # if inputParameter['dataFileNameMat'] is None:
    #     inputParameter['dataFileNameMat'] = 'sptDataMovies.matPy'
    
    
    # Fall-back to GUI if no list of ThunderSTORM.csv files is specified
    # *_thunder_.csv files is specified in DefineInputParameters.m
    if not inputParameter['filename_thunderstormCSV']:
        files = filedialog.askopenfilenames(
            title="Select *.csv from ThunderSTORM",
            filetypes=[("CSV files", "*_thunder.csv")]
        )
        
        inputParameter['filename_thunderstormCSV'] = list(files)
        if files:
            inputParameter['dataPathName'] = os.path.dirname(files[0])
            os.chdir(inputParameter['dataPathName'])
            

    # Check whether an equal number of files for localisations and segmentations was selected
    # in the SPECIAL CASE that several *_thunder.csv files, but only one brightfield image
    # were selected, ask wether to continue. If yes is chosen, this brightfiield image
    # is used for all loaded *_thunder.csv files.
    if inputParameter.get('useSegmentations'):
        if len(inputParameter['filename_thunderstormCSV']) != len(inputParameter['filename_procBrightfield']):
            if len(inputParameter['filename_procBrightfield']) == 1 and len(inputParameter['filename_thunderstormCSV']) > 1:
                print('Only one brightfield image but >1 CSV files were chosen!')
                proceed = simpledialog.askinteger("Continue?", "Enter 1 to continue or 0 to cancel:", initialvalue=1)
                if proceed == 1:
                    temp = inputParameter['filename_procBrightfield'][0]
                    inputParameter['filename_procBrightfield'] = [temp] * len(inputParameter['filename_thunderstormCSV'])
                else:
                    raise Exception('User chose to cancel the process.')
            else:
                raise Exception('Select an equal number of files for localisations and segmentations!')

    # Create OUTPUT folder if it doesn't exist
    inputParameter['dataPathOutp'] = os.path.join(inputParameter['dataPathName'], 'Output_Python/')
    if not os.path.exists(inputParameter['dataPathOutp']):
        os.makedirs(inputParameter['dataPathOutp'])

    # Display analysis parameters
    print('  Print inputParameters')
    print(inputParameter)

    # 2. sptPALM data analysis (looping over each movie)
    DATA = {'MOVIES': []}

    for ii in range(len(inputParameter['filename_thunderstormCSV'])):
        inputParameter['movieNumber'] = ii + 1

        # 2.1 Initialisation of structure Para1 (local analysis over one movie)
        #The structure Para1 will contain all parameters and updated references to filenames and pathnames.
        Para1 = inputParameter.copy() #Initialise data structure
        Para1['filename_thunderstormCSV'] = inputParameter['filename_thunderstormCSV'][ii]
        if inputParameter['filename_procBrightfield']:
            Para1['filename_procBrightfield'] = inputParameter['filename_procBrightfield'][ii]
        else:
            Para1['filename_procBrightfield'] = None

        os.chdir(Para1['dataPathName'])

        # 2.2 Loading and preparing localisation data
        Para1 = convert_csv(Para1)

        # 2.3 Apply cell segmentation
        if inputParameter['useSegmentations']:
            Para1 = apply_cell_segmentation(Para1)

#         # 2.4 Perform tracking
#         Para1 = tracking_analysis(Para1)

#         # 2.5 Calculate and plot diffusion coefficients
#         Para1 = diffusion_analysis(Para1)
#         Para1 = plot_hist_diffusion_tracklength(Para1)

#         # 2.6 Single Cell Tracking Analysis
#         if inputParameter['useSegmentations']:
#             Para1 = single_cell_tracking_analysis(Para1)
#             Para1 = plot_single_cell_tracking_analysis(Para1)

#         # 2.7 Optional Analysis of normalized increment distribution
#         if Para1.get('NormIncAnalysis', False):
#             Para1 = norm_increments_analysis(Para1)

#         # 2.8 Save current analysis as Matlab workspace
#         saveFile = Para1['filename_analysis_csv'].replace('.csv', '')
#         save_path = os.path.join(inputParameter['dataPathOutp'], f"{saveFile}.mat")
#         shutil.copyfile(Para1['filename_thunderstormCSV'], save_path)

        # Cell array containing all Para1 structs
        DATA['MOVIES'].append((Para1, Para1['filename_thunderstormCSV']))

    # 3. Save entire DATA structure
    save_path = os.path.join(inputParameter['dataPathOutp'], inputParameter['dataFileNameMat'])
    with open(save_path, 'w') as f:
        f.write(str(DATA))

    return DATA, inputParameter

# # Example usage
# if __name__ == "__main__":
#     DATA, Para1 = sptPALM_analyseMovies()
        
            
            
            
            
    return inputParameter, DATA


