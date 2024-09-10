#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

from define_input_parameters import define_input_parameters
from sptPALM_analyse_movies import sptPALM_analyse_movies

data = {}
para = {}
combined_data = {}

def merge_data_folders_files():
    print('-2-1-')
    # merge_data_folders_files implementation here
    return []
def combine_thunderstorm_csv_files():
    print('-2-4-')
    # Combine_ThunderSTORM_csv_files implementation here
    return []
def sptPALM_combine_data(combined_data=None):
    print('-4-')
    # Your implementation here
    return []
def sptPALM_plot_combined_data(combined_data=None):
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
    PROMPT = """Choose and press Enter
    0: Exit
    1: Edit parameters for data analysis
    2: Sub programs (ImageJ/Fiji macros, etc.)
    3: sptPALM_analyse_movies
    4: sptPALM_combine_data
    5: sptPALM_plot_combined_data
    6: sptPALM_anaDDA
    7: sptPALM_MCDDA
    8: sptPALM_runAll (Options 3-6)\n"""
    # Check prompt
    try:
        prompt_input = int(input(PROMPT))
    except ValueError:
        print("Invalid input, please enter a number.")
        continue

    match prompt_input:
        case 0:
            print('Exit!')
            break
        case 1:  # Careful, this was a dirty hack in Matlab and might not work here!
            print(' Edit parameters for data analysis!')
            print(' Look for DefineInputParameters.py and edit it.')
            print(' Then save the file and continue.')
            input_parameter = define_input_parameters()
        case 2:  # Combine_ThunderSTORM_csv_files
            while True:
                print('--')
                SUB_PROMPT = """    Choose and press Enter
        0: Go back to main prompt
        1: Merge data files from different sub-folders
        2: NOT WORKING YET Run ImageJ/Fiji macro 'Cell Segmentation'
        3: NOT WORKING YET Run ImageJ/Fiji macro 'ThunderStorm'
        4: Combine ThunderSTORM *.csv files\n: """
                # Check prompt
                try:
                    sub_prompt_input = int(input(SUB_PROMPT))
                except ValueError:
                    print("Invalid input, please enter a number.")
                    continue

                match sub_prompt_input:
                    case int(0):
                        print('Exit sub!')
                        break
                    case 1:
                        print('Merge data files from different sub-folders')
                        merge_data_folders_files()
                    case 2:
                        print('NOT IMPLEMENTED: Running ImageJ/Fiji macro'
                              'Cell Segmentation')
                        # Running Cellseg implementation here
                    case 3:
                        print('NOT IMPLEMENTED: Running ThunderSTORM macro')
                        # Running Thunderstorm implementation here
                    case 4:
                        print('Run Combine_ThunderSTORM_csv_files')
                        combine_thunderstorm_csv_files()
                    case _:
                        print("Invalid option, please choose a valid number.")
                        continue
        case 3:  # sptPALM_analyse_Movies
            data, input_parameter, para = sptPALM_analyse_movies()
            print('DATA now available in the workspace')
        case 4:  # sptPALM_combineData
            print('Run sptPALM_combineData()')
            if data:
                combined_data = sptPALM_combine_data(data)
            else:
                print('No DATA from option 3 available')
                print('Continue with GUI to select DATA ("sptDataMovies.mat" '
                      'or similar)')
                CombinedDATA = sptPALM_combine_data()
            print('CombinedDATA now available in the workspace')
        case 5:  # sptPALM_PlotCombinedData
            print('NRun sptPALM_PlotCombinedData(CombinedDATA)')
            if combined_data:
                combined_data = sptPALM_plot_combined_data(combined_data)
            else:
                print('No combined_data from option 4 available')
                print('Continue with GUI to select combined_data '
                      '("sptDataCombinedMovies.mat" or similar)')
                combined_data = sptPALM_plot_combined_data()
        case 6:  # anaDDA
            print('run sptPALM_anaDDA(CombinedDATA, 1) on condition 1')
            if combined_data:
                combined_data = sptPALM_anaDDA(1, combined_data)
            else:
                print('No combined_data from option 4 available')
                print('Continue with GUI to select combined_data '
                      '("sptDataCombinedMovies.mat" or similar)')
                combined_data = sptPALM_anaDDA(1)
        case 7:  # MCDDA
            if combined_data:
                combined_data = sptPALM_MCDDA(1, combined_data)
            else:
                print('No combined_data from option 4 available')
                print('Continue with GUI to select combined_data '
                      '("sptDataCombinedMovies.mat" or similar)')
                combined_data = sptPALM_MCDDA(1)
        case 8: # Run everything until anaDDA
            data, para = sptPALM_analyse_movies()
            combined_data = sptPALM_combine_data(data)
            combined_data = sptPALM_plot_combined_data(combined_data)
            combined_data = sptPALM_anaDDA(1, combined_data)
        case _:
            print("Invalid option, please choose a valid number.")
            continue
print("Done")