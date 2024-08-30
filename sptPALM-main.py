#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

from DefineInputParameters import define_input_parameters
from sptPALM_analyseMovies import sptPALM_analyse_Movies

DATA = None
Para1 = None
CombinedDATA = None

def MergeDataFoldersFiles():
    print('-2-1-')
    # MergeDataFoldersFiles implementation here
    return []
def combine_thunderstorm_csv_files():
    print('-2-4-')
    # Combine_ThunderSTORM_csv_files implementation here
    return []
def sptPALM_combineData(data=None):
    print('-4-')
    # Your implementation here
    return []
def sptPALM_PlotCombinedData(combined_data):
    print('-5-')
    # Your implementation here
    return combined_data
def sptPALM_anaDDA(condition, combined_data=None):
    print('-6-')
    # Your implementation here
    return combined_data
def sptPALM_MCDDA(condition, combined_data=None):
    print('-7-')
    # Your implementation here
    return combined_data

while True:
    print('-')
    prompt = """Choose and press Enter
    0: Exit
    1: Edit parameters for data analysis
    2: Sub programs (ImageJ/Fiji macros, etc.)
    3: sptPALM_analyseMovies
    4: sptPALM_combineData
    5: sptPALM_PlotCombinedData
    6: sptPALM_anaDDA
    7: sptPALM_MCDDA
    8: sptPALM_runAll (Options 3-6)\n"""
    #check prompt
    try:
        prompt_input = int(input(prompt))
    except ValueError:
        print("Invalid input, please enter a number.")
        continue   
    
    match prompt_input:
        case 0:
            print('Exit!')
            break
        case 1: #careful, this was a dirty hack in Matlab and might not work here!
            print(' Edit parameters for data analysis!')
            print(' Look for DefineInputParameters.py and edit it.')
            print(' Then save the file and continue.')
            inputParameter = define_input_parameters()
            
        case 2:# Combine_ThunderSTORM_csv_files       
            while True:
                print('--')
                sub_prompt = """    Choose and press Enter
        0: Go back to main prompt
        1: Merge data files from different sub-folders
        2: NOT WORKING YET Run ImageJ/Fiji macro 'Cell Segmentation'
        3: NOT WORKING YET Run ImageJ/Fiji macro 'ThunderStorm'
        4: Combine ThunderSTORM *.csv files\n: """
                #check prompt
                try:
                    sub_prompt_input = int(input(sub_prompt))
                except ValueError:
                    print("Invalid input, please enter a number.")
                    continue   
                
                match sub_prompt_input:
                    case int(0):
                        print('Exit sub!')
                        break    
                    case 1:
                        print('Merge data files from different sub-folders')
                        MergeDataFoldersFiles()
                    case 2:
                        print('NOT IMPLEMENTED: Running ImageJ/Fiji macro Cell Segmentation')
                        # Cellseg implementation here
                    case 3:
                        print('NOT IMPLEMENTED: Running ThunderSTORM macro')
                        # Thunderstorm implementation here
                    case 4:
                        print('Run Combine_ThunderSTORM_csv_files')
                        combine_thunderstorm_csv_files()
                    case _:
                        print("Invalid option, please choose a valid number.")
                        continue
                    
        case 3: #sptPALM_analyse_Movies
            DATA, Para1 = sptPALM_analyse_Movies()
            print('DATA now available in the workspace')
            
        case 4: #sptPALM_combineData
            print('Run sptPALM_combineData()')
            if DATA:
                CombinedDATA = sptPALM_combineData(DATA)
            else:
                print('No DATA from option 3 available')
                print('Continue with GUI to select DATA ("sptDataMovies.mat" or similar)')
                CombinedDATA = sptPALM_combineData()
            print('CombinedDATA now available in the workspace')
            
        case 5: #sptPALM_PlotCombinedData
            print('NRun sptPALM_PlotCombinedData(CombinedDATA)')
            if CombinedDATA:
                CombinedDATA = sptPALM_PlotCombinedData(CombinedDATA)
            else:
                print('No CombinedDATA from option 4 available')
                print('Continue with GUI to select CombinedDATA ("sptDataCombinedMovies.mat" or similar)')
                CombinedDATA = sptPALM_PlotCombinedData()
                
        case 6: #anaDDA
            print('run sptPALM_anaDDA(CombinedDATA, 1) on condition 1')
            if CombinedDATA:
                CombinedDATA = sptPALM_anaDDA(1, CombinedDATA)
            else:
                print('No CombinedDATA from option 4 available')
                print('Continue with GUI to select CombinedDATA ("sptDataCombinedMovies.mat" or similar)')
                CombinedDATA = sptPALM_anaDDA(1)
                
        case 7: #MCDDA
            if CombinedDATA:
                CombinedDATA = sptPALM_MCDDA(1, CombinedDATA)
            else:
                print('No CombinedDATA from option 4 available')
                print('Continue with GUI to select CombinedDATA ("sptDataCombinedMovies.mat" or similar)')
                CombinedDATA = sptPALM_MCDDA(1)
                
        case 8: # un everything until anaDDA
            DATA, Para1 = sptPALM_analyse_Movies()
            CombinedDATA = sptPALM_combineData(DATA)
            CombinedDATA = sptPALM_PlotCombinedData(CombinedDATA)
            CombinedDATA = sptPALM_anaDDA(1, CombinedDATA)
        case _:
            print("Invalid option, please choose a valid number.")
            continue

