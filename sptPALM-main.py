#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

import os
import sys
from pathlib import Path

# Add the subfolder to the Python path
sys.path.append(str(Path('subFunctions')))

from sptPALM_analyseMovies import sptPALM_analyseMovies


DATA = None
Para1 = None
CombinedDATA = None

def open_define_input_parameters():
    print('Look for DefineInputParameters.py and edit it.')
    print('Then save the file and continue.')

def merge_data_folders_files():
    print('Running ImageJ/Fiji macro Cell Segmentation')
    # MergeDataFoldersFiles implementation here

def combine_thunderstorm_csv_files():
    print('Run Combine_ThunderSTORM_csv_files')
    # Combine_ThunderSTORM_csv_files implementation here

# def sptPALM_analyseMovies():
#     print('Run sptPALM_analyseMovies()')
#     # Your implementation here
#     return [], {}

def sptPALM_combineData(data=None):
    print('Run sptPALM_combineData()')
    # Your implementation here
    return []

def sptPALM_PlotCombinedData(combined_data):
    print('Run sptPALM_PlotCombinedData(CombinedDATA)')
    # Your implementation here
    return combined_data

def sptPALM_anaDDA(condition, combined_data=None):
    print(f'Run sptPALM_anaDDA(CombinedDATA, {condition})')
    # Your implementation here
    return combined_data

def sptPALM_MCDDA(condition, combined_data=None):
    print(f'Run sptPALM_MCDDA(CombinedDATA, {condition})')
    # Your implementation here
    return combined_data

while True:
    prompt = """Choose and press Enter
    0: Exit
    1: Edit parameters for data analysis
    2: Sub programs (ImageJ/Fiji macros, etc.)
    3: sptPALM_analyseMovies
    4: sptPALM_combineData
    5: sptPALM_PlotCombinedData
    6: sptPALM_anaDDA
    7: sptPALM_MCDDA
    8: sptPALM_runAll (Options 3-6)"""
    
    try:
        prompt_input = int(input(prompt))
    except ValueError:
        print("Invalid input, please enter a number.")
        continue

    if prompt_input == 0:
        print('Exit!')
        break
    
    elif prompt_input == 1:
        print('Edit parameters for data analysis!')
        open_define_input_parameters()
        
    elif prompt_input == 2:
        while True:
            sub_prompt = """Choose and press Enter
        0: Exit
        1: Merge data files from different sub-folders
        2: NOT WORKING YET Run ImageJ/Fiji macro 'Cell Segmentation'
        3: NOT WORKING YET Run ImageJ/Fiji macro 'ThunderStorm'
        4: Combine ThunderSTORM *.csv files\n: """
            
            try:
                prompt_input_options = int(input(sub_prompt))
            except ValueError:
                print("Invalid input, please enter a number.")
                continue

            if prompt_input_options == 0:
                print('Exit sub!')
                break
            
            elif prompt_input_options == 1:
                merge_data_folders_files()
                
            elif prompt_input_options == 2:
                print('Running ImageJ/Fiji macro Cell Segmentation')
                # Cellseg implementation here
                
            elif prompt_input_options == 3:
                print('Running ThunderSTORM macro')
                # Thunderstorm implementation here
                
            elif prompt_input_options == 4:
                combine_thunderstorm_csv_files()
    elif prompt_input == 3:
        DATA, Para1 = sptPALM_analyseMovies()
        print('DATA now available in the workspace')
        
    elif prompt_input == 4:
        if DATA:
            CombinedDATA = sptPALM_combineData(DATA)
        else:
            print('No DATA from option 3 available')
            print('Continue with GUI to select DATA ("sptDataMovies.mat" or similar)')
            CombinedDATA = sptPALM_combineData()
        print('CombinedDATA now available in the workspace')
        
    elif prompt_input == 5:
        if CombinedDATA:
            CombinedDATA = sptPALM_PlotCombinedData(CombinedDATA)
        else:
            print('No CombinedDATA from option 4 available')
            print('Continue with GUI to select CombinedDATA ("sptDataCombinedMovies.mat" or similar)')
            CombinedDATA = sptPALM_PlotCombinedData()
            
    elif prompt_input == 6:
        if CombinedDATA:
            CombinedDATA = sptPALM_anaDDA(1, CombinedDATA)
        else:
            print('No CombinedDATA from option 4 available')
            print('Continue with GUI to select CombinedDATA ("sptDataCombinedMovies.mat" or similar)')
            CombinedDATA = sptPALM_anaDDA(1)
            
    elif prompt_input == 7:
        if CombinedDATA:
            CombinedDATA = sptPALM_MCDDA(1, CombinedDATA)
        else:
            print('No CombinedDATA from option 4 available')
            print('Continue with GUI to select CombinedDATA ("sptDataCombinedMovies.mat" or similar)')
            CombinedDATA = sptPALM_MCDDA(1)
            
    elif prompt_input == 8:
        print('Run everything!')
        DATA, Para1 = sptPALM_analyseMovies()
        CombinedDATA = sptPALM_combineData(DATA)
        CombinedDATA = sptPALM_PlotCombinedData(CombinedDATA)
        CombinedDATA = sptPALM_anaDDA(1, CombinedDATA)
    else:
        print("Invalid option, please choose a valid number.")
