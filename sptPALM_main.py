#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This work is licensed under the CC BY 4.0 License.
You are free to share and adapt this work, even for commercial purposes,
as long as you provide appropriate credit to the original creator.

Original Creator: Johannes Hohlbein (Wageningen University & Research)
Date of Creation: September, 2024

Full license details can be found at https://creativecommons.org/licenses/by/4.0/
"""

from analyse_movies_sptPALM import analyse_movies_sptPALM
from combine_analysed_data_sptPALM import combine_analysed_data_sptPALM
from plot_combined_data_sptPALM import plot_combined_data_sptPALM
from MC_diffusion_distribution_analysis_sptPALM import MC_diffusion_distribution_analysis_sptPALM
from set_parameters_sptPALM import set_parameters_sptPALM
from set_parameters_sptPALM_GUI import set_parameters_sptPALM_GUI 

input_parameter = {}
data = {}
comb_data = {}

def combine_thunderstorm_csv_files():
    print('-2-4-')
    # Combine_ThunderSTORM_csv_files implementation here
    return []

while True:
    print('-')
    PROMPT = """Choose and press Enter
    0: Exit
    1: Set parameters GUI
    2: Analyse individual movies
    3: Combine individually analysed movies
    4: Plot combined data
    5: Monte-Carlo DDA
    6: Auxillary functions
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
        case 1:
            input_parameter = set_parameters_sptPALM()
            input_parameter = set_parameters_sptPALM_GUI(input_parameter)    
            # Display analysis parameters
            print('  Show input_parameter')
            # Iterate through the dictionary and print each key-value pair on a new line
            for key, value in input_parameter.items():
                print(f"    .{key}: {value}")
    
        case 2:  # sptPALM_analyse_Movies
            if input_parameter:
                print(" 'input_parameter' available, continue")
                data = analyse_movies_sptPALM(input_parameter)
            else:
                print(" No 'input_parameter' available, selecting defaults from set_parameters_sptPLAM.py.")
                data = analyse_movies_sptPALM()
            print("'data' now available in memory\n")
        
        case 3:  # sptPALM_combineData
            if not input_parameter:
                print(" No 'input_parameter' available")
                input_parameter = set_parameters_sptPALM()
                input_parameter = set_parameters_sptPALM_GUI(input_parameter)   
            if data:
                print(" 'data' available, continue")
                comb_data = combine_analysed_data_sptPALM(data, input_parameter)
            else:
                print("No 'data' from available")
                print("Continue with GUI to select DATA from 'sptData_movies.pkl' or similar")
                comb_data = combine_analysed_data_sptPALM(None, input_parameter)
            print("Combined data 'comb_data' now available in memory\n")
            
        case 4:  # sptPALM_PlotCombinedData
            print('Run plot_combined_data_sptPALM(comb_data)')
            if comb_data:
                comb_data = plot_combined_data_sptPALM(comb_data)
            else:
                print("No comb_data from option 2 available")
                print("Continue with GUI to select 'comb_data' "
                      "from 'sptData_combined_movies.pkl' or similar")
                comb_data = plot_combined_data_sptPALM()
          
        case 5:  # MCDDA
            condition_to_select = 0
            if comb_data:
                condition = 0
                comb_data = MC_diffusion_distribution_analysis_sptPALM(condition_to_select, comb_data)
            else:
                print('No ''comb_data'' from option 3 available')
                print("Continue with GUI to select 'comb_data' "
                      "'sptData_combined_movies.pkl' or similar")
                comb_data = MC_diffusion_distribution_analysis_sptPALM(condition_to_select)
        
        case 6:  # Combine_ThunderSTORM_csv_files
            while True:
                print('--')
                SUB_PROMPT = """    Choose and press Enter
       0: Go back to main prompt
       1: Combine ThunderSTORM *.csv files 
       2: Empty\n"""
               # Check prompt
                try:
                    sub_prompt_input = int(input(SUB_PROMPT))
                except ValueError:
                    print("Invalid input, please enter a number.")
                    continue

                match sub_prompt_input:
                    case 0:
                       print('Exit sub!')
                       break
                    case 1:
                        print('Run Combine_ThunderSTORM_csv_files')
                        combine_thunderstorm_csv_files()
                    case 2:
                        print('Do nothing....')
                    case _:
                       print("Invalid option, please choose a valid number.")
                       continue
        case _:
            print("Invalid option, please choose a valid number.")
            continue
print("Done")

# Currently taken out:
    
    # from set_parameters_sptPALM import set_parameters_sptPALM
    
     
    # def merge_data_folders_files():
    #     print('-2-1-')
    #     # merge_data_folders_files implementation here
    #     return []
    # def sptPALM_anaDDA(condition, comb_data=None):
    #     print('-6-')
    #     # Your implementation here
    #     return comb_data
      
    
    # case 1:  # Careful, this was a dirty hack in Matlab and might not work here!
    #     print('Edit parameters for data analysis!')
    #     print('  Look for the input_parameter in the Variable Explorer and edit it.')
    #     print("  When done, type '!continue' into the command line.")
    #     input_parameter = set_parameters_sptPALM()
    #     # Doesn't yet enable accessing the Variable Explorer :(
    #     pdb.set_trace()  # This will pause execution and open the debugger
            
    # case 2:  # Combine_ThunderSTORM_csv_files
    #     while True:
    #         print('--')
    #         SUB_PROMPT = """    Choose and press Enter
    # 0: Go back to main prompt
    # 1: Merge data files from different sub-folders
    # 2: NOT WORKING YET Run ImageJ/Fiji macro 'Cell Segmentation'
    # 3: NOT WORKING YET Run ImageJ/Fiji macro 'ThunderStorm'
    # 4: Combine ThunderSTORM *.csv files\n: """
    #         # Check prompt
    #         try:
    #             sub_prompt_input = int(input(SUB_PROMPT))
    #         except ValueError:
    #             print("Invalid input, please enter a number.")
    #             continue

    #         match sub_prompt_input:
    #             case int(0):
    #                 print('Exit sub!')
    #                 break
    #             case 1:
    #                 print('Merge data files from different sub-folders')
    #                 merge_data_folders_files()
    #             case 2:
    #                 print('NOT IMPLEMENTED: Running ImageJ/Fiji macro'
    #                       'Cell Segmentation')
    #                 # Running Cellseg implementation here
    #             case 3:
    #                 print('NOT IMPLEMENTED: Running ThunderSTORM macro')
    #                 # Running Thunderstorm implementation here
    #             case 4:
    #                 print('Run Combine_ThunderSTORM_csv_files')
    #                 combine_thunderstorm_csv_files()
    #             case _:
    #                 print("Invalid option, please choose a valid number.")
    #                 continue
    

        # case 5: # Run everything until anaDDA
        #     data, para = sptPALM_analyse_movies()
        #     comb_data = sptPALM_combine_data(data)
        #     comb_data = sptPALM_plot_combined_data(comb_data)
        #     comb_data = sptPALM_anaDDA(1, comb_data)
 