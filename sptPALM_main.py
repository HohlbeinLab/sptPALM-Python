#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

from set_parameters_sptPALM import set_parameters_sptPALM
from analyse_movies_sptPALM import analyse_movies_sptPALM
from combine_analysed_data_sptPALM import combine_analysed_data_sptPALM
from plot_combined_data_sptPALM import plot_combined_data_sptPALM
from MC_diffusion_distribution_analysis_sptPALM import MC_diffusion_distribution_analysis_sptPALM

import pdb

data = {}
para = {}
comb_data = {}

def merge_data_folders_files():
    print('-2-1-')
    # merge_data_folders_files implementation here
    return []
def combine_thunderstorm_csv_files():
    print('-2-4-')
    # Combine_ThunderSTORM_csv_files implementation here
    return []
def sptPALM_anaDDA(condition, comb_data=None):
    print('-6-')
    # Your implementation here
    return comb_data

while True:
    print('-')
    PROMPT = """Choose and press Enter
    0: Exit
    1: Edit parameters for data analysis
    2: Sub programs (ImageJ/Fiji macros, etc.)
    3: Analyse individual movies
    4: Combine individually analysed movies
    5: Plot combined data
    6: Monte-Carlo DDA
    \n"""
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
            print('Edit parameters for data analysis!')
            print('  Look for the input_parameter in the Variable Explorer and edit it.')
            print("  When done, type '!continue' into the command line.")
            input_parameter = set_parameters_sptPALM()
            # Doesn't yet enable accessing the Variable Explorer :(
            pdb.set_trace()  # This will pause execution and open the debugger
                
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
            data, input_parameter, para = analyse_movies_sptPALM()
            print("'data' now available in the workspace\n")
        
        case 4:  # sptPALM_combineData
            if data:
                comb_data = combine_analysed_data_sptPALM(data)
            else:
                print('No DATA from option 3 available')
                print('Continue with GUI to select DATA from "sptData_movies.pkl" or similar')
                comb_data = combine_analysed_data_sptPALM()
            print("Combined data 'comb_data' now available in the workspace\n")
        
        case 5:  # sptPALM_PlotCombinedData
            print('Run splot_combined_data_sptPALM(comb_data)')
            if comb_data:
                comb_data = plot_combined_data_sptPALM(comb_data)
            else:
                print("No comb_data from option 4 available")
                print('Continue with GUI to select comb_data '
                      '("sptData_combined_movies.pkl" or similar)')
                comb_data = plot_combined_data_sptPALM()
        
        # case 6:  # anaDDA
        #     print('run sptPALM_anaDDA(CombinedDATA, 1) on condition 1')
        #     if comb_data:
        #         comb_data = sptPALM_anaDDA(1, comb_data)
        #     else:
        #         print("No 'comb_data' from option 4 available")
        #         print("Continue with GUI to select 'comb_data' "
        #               '("sptDataCombinedMovies.mat" or similar)')
        #         comb_data = sptPALM_anaDDA(1)
        
        case 6:  # MCDDA
            condition_to_select = 0
            if comb_data:
                condition = 0
                comb_data = MC_diffusion_distribution_analysis_sptPALM(condition_to_select, comb_data)
            else:
                print('No comb_data from option 4 available')
                print('Continue with GUI to select comb_data '
                      '("sptData_combined_movies.pkl" or similar)')
                comb_data = MC_diffusion_distribution_analysis_sptPALM(condition_to_select)
        
        # case 8: # Run everything until anaDDA
        #     data, para = sptPALM_analyse_movies()
        #     comb_data = sptPALM_combine_data(data)
        #     comb_data = sptPALM_plot_combined_data(comb_data)
        #     comb_data = sptPALM_anaDDA(1, comb_data)
        
        case _:
            print("Invalid option, please choose a valid number.")
            continue
print("Done")