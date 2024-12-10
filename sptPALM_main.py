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
from combine_thunderstorm_csv_files import combine_thunderstorm_csv_files

def sptPALM_main():
    """
    Main function to analyse single-particle-tracking Photo-Activated-Laser-Microscopy.
    Run function sptPALM_main.py from within Spyder or any other Python framework.
    
    CC BY 4.0 License.
    Original Creator: Johannes Hohlbein (Wageningen University & Research)
    Date of Creation: September, 2024
    
    Parameters
    ----------
        None.

    Raises
    ------
    Exception
        None.

    Returns
    -------
    input_parameter : DICT
        DESCRIPTION.
    data : DICT
            DESCRIPTION.
    comb_data : DICT
                DESCRIPTION.
    sim_input : DICT
                DESCRIPTION.
    """
  
    input_parameter = {}
    data = {}
    comb_data = {}
    sim_input = {}  
 
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

        try: # Check prompt
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
                print('  Show input_parameter:') # Display analysis parameters
                for key, value in input_parameter.items():
                    print(f"    .{key}: {value}")
            case 2:  # analyse_movies_sptPALM,py
                [data, input_parameter] = analyse_movies_sptPALM(input_parameter)
                print("'data' now available in memory\n")
            case 3:  # combine_analysed_data_sptPALM.py
                comb_data, input_parameter = combine_analysed_data_sptPALM(data, input_parameter)
                print("Combined data 'comb_data' now available in memory\n")
            case 4:  # plot_combined_data_sptPALM.py
                comb_data = plot_combined_data_sptPALM(comb_data, input_parameter)
            case 5:  # MCDDA
                comb_data = MC_diffusion_distribution_analysis_sptPALM(comb_data, input_parameter, sim_input)
            case 6:  # Combine_ThunderSTORM_csv_files
                while True:
                    print('--')
                    SUB_PROMPT = """    Choose and press Enter
           0: Go back to main prompt
           1: Combine ThunderSTORM *.csv files 
           2: Empty\n"""
                    try: # Check prompt
                        sub_prompt_input = int(input(SUB_PROMPT))
                    except ValueError:
                        print("Invalid input, please enter a number.")
                        continue
    
                    match sub_prompt_input:
                        case 0:
                           print('Exit sub!')
                           break
                        case 1: # combine_thunderstorm_csv_files
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

    return input_parameter, data, comb_data, sim_input


if __name__ == "__main__":
    sptPALM_main()


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
 