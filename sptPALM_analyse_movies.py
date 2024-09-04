#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

#import tkinter as tk
from tkinter import simpledialog, filedialog
import os
#import sys

from define_input_parameters import define_input_parameters


from convert_csv import convert_csv
from apply_cell_segmentation import apply_cell_segmentation
from tracking_analysis import tracking_analysis
# from DiffusionAnalysis import diffusion_analysis
# from Plot_Hist_DiffusionTracklength import plot_hist_diffusion_tracklength
# from SingleCellTrackingAnalysis import single_cell_tracking_analysis
# from Plot_SingleCellTrackingAnalysis import plot_single_cell_tracking_analysis
# from NormIncrements_Analysis import norm_increments_analysis


def sptPALM_analyse_movies():
    DATA = None
    # 1.1 Define input parameters
    print('Run define_input_parameters()')
    inputParameter = define_input_parameters()
    
    # Allow savename to be changed (default: 'sptDataMovies.mat')
    # NOT NEEDED, REMEMBER FOR LATER
    # root = tk.Tk()
    # root.withdraw()  # Hide the root window    
    # prompt = "Enter new name for saving sptDataMovies.mat or press OK/Enter"
    # inputParameter['dataFileNameMat'] = simpledialog.askstring("Rename sptDataMovies.mat?", prompt, initialvalue='sptDataMovies.mat')
   
 #temporarily disabled   
    inputParameter['data_filename_mat'] = 'sptDataMovies.matPy'
    # input_default = 'sptDataMovies.matPy'
    # user_input = input("  Enter string or press enter (default is: '"+input_default+"'): ")
    # if not user_input:
    #     user_input = input_default 
    # inputParameter['dataFileNameMat'] = user_input
      
    
    # Fall-back to GUI if no list of ThunderSTORM.csv files is specified
    # *_thunder_.csv files is specified in DefineInputParameters.m
    if not inputParameter['filename_thunderstorm_csv']:
        files = filedialog.askopenfilenames(
            title="Select *.csv from ThunderSTORM or other SMLM programs",
            filetypes=[("CSV files", "*_thunder.csv")]
        )
        
        inputParameter['filename_thunderstorm_csv'] = list(files)
        if files:
            inputParameter['data_pathname'] = os.path.dirname(files[0])
            os.chdir(inputParameter['data_pathname'])
            
    # Check whether an equal number of files for localisations and segmentations was selected
    # in the SPECIAL CASE that several *_thunder.csv files, but only one brightfield image
    # were selected, ask wether to continue. If yes is chosen, this brightfiield image
    # is used for all loaded *_thunder.csv files.
    if inputParameter.get('use_segmentations'):
        if len(inputParameter['filename_thunderstorm_csv']) != len(inputParameter['filename_proc_brightfield']):
            if len(inputParameter['filename_proc_brightfield']) == 1 and len(inputParameter['filename_thunderstorm_csv']) > 1:
                print('Only one brightfield image but >1 CSV files were chosen!')
                proceed = simpledialog.askinteger("Continue?", "Enter 1 to continue or 0 to cancel:", initialvalue=1)
                if proceed == 1:
                    temp = inputParameter['filename_proc_brightfield'][0]
                    inputParameter['filename_proc_brightfield'] = [temp] * len(inputParameter['filename_thunderstorm_csv'])
                else:
                    raise Exception('User chose to cancel the process.')
            else:
                raise Exception('Select an equal number of files for localisations and segmentations!')

    # Create OUTPUT folder if it doesn't exist
    inputParameter['data_path_output'] = os.path.join(inputParameter['data_pathname'], 'Output_Python/')
    if not os.path.exists(inputParameter['data_path_output']):
        os.makedirs(inputParameter['data_path_output'])

    # Display analysis parameters
    print('  Print inputParameters')
    print(inputParameter)

    # 2. sptPALM data analysis (looping over each movie)
    DATA = {'MOVIES': []}

    for ii in range(len(inputParameter['filename_thunderstorm_csv'])):
        inputParameter['movie_number'] = ii #start with 0 not 1

        # 2.1 Initialisation of structure para (local analysis over one movie)
        #The structure para will contain all parameters and updated references to filenames and pathnames.
        para = inputParameter.copy() #Initialise data structure
        para['filename_thunderstorm_csv'] = inputParameter['filename_thunderstorm_csv'][ii]
        if inputParameter['filename_proc_brightfield']:
            para['filename_proc_brightfield'] = inputParameter['filename_proc_brightfield'][ii]
        else:
            para['filename_proc_brightfield'] = None

        os.chdir(para['data_pathname'])

        # 2.2 Loading and preparing localisation data
        para = convert_csv(para)

        # 2.3 Apply cell segmentation
        if inputParameter['use_segmentations']:
            para = apply_cell_segmentation(para)

        # 2.4 Perform tracking
        para = tracking_analysis(para)

#         # 2.5 Calculate and plot diffusion coefficients
#         para = diffusion_analysis(para)
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
        DATA['MOVIES'].append((para, para['filename_thunderstorm_csv']))

    # 3. Save entire DATA structure
    save_path = os.path.join(inputParameter['data_path_output'], inputParameter['data_filename_mat'])
    with open(save_path, 'w') as f:
        f.write(str(DATA))

    return DATA, inputParameter

# # Example usage
# if __name__ == "__main__":
#     DATA, para = sptPALM_analyseMovies()
        
            
            
            
            
    return inputParameter, DATA


