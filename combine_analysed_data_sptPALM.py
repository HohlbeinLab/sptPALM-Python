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

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
import os
import pickle
from set_parameters_sptPALM import set_parameters_sptPALM
from helper_functions import string_input_with_default

def combine_analysed_data_sptPALM(data=None):
    
    print('\nRun combine_analysed_data_sptPALM.py')

    # loaded more as a dummy here: define input parameters
    input_parameter = set_parameters_sptPALM()
    filename = []
    
    # # TEMPORARY For bugfixing - Replace the following line with your file path if needed
    # filename = '/Users/hohlbein/Documents/WORK-DATA-local/Cas12a-data-JH/output_python/sptData_movies.pkl'
    # with open(filename, 'rb') as f:
    #     data = pickle.load(f)
    
    # 1.1 Check whether DATA was passed to the function
    if data is None:
        # Use Tkinter for file dialog
        Tk().withdraw()  # Close root window
        starting_directory = os.path.join(input_parameter['data_dir'],
                                                  input_parameter['default_output_dir'])
        filename = askopenfilename(initialdir = starting_directory, 
                                    filetypes = [("pickle file", "*.pkl")],
                                    title = "Select *.pkl file from sptPALM_analyse_movies.py")
        if filename:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
        else:
            raise ValueError("No file selected!")
    else:
        print('  Careful, there might be no data available to proceed!')
        
 
    # Optional part to modify input parameters before combining data
    # Placeholder for define_input_parameters.py functionality

    # # GUI version: Allow savename to be changed (default: 'sptData_combined_movies.pkl')
    # input_parameter['fn_combined_movies'] = askstring(f"Rename {input_parameter['fn_combined_movies']}?", 
    #                           f"Enter new name for saving {input_parameter['fn_combined_movies']} or press OK/Enter", 
    #                           initialvalue=input_parameter['fn_combined_movies'])
    
    # CMD Version: Allow savename to be changed (default: 'sptData_combined_movies.pkl')
    fn_output_default = data['input_parameter']['fn_combined_movies']
    data['input_parameter']['fn_combined_movies'] = string_input_with_default("  Rename filename or press OK/Enter", fn_output_default)


    comb_data = {}
    comb_data['#_movies_loaded'] = len(data['movies'])

    print(f"  ... there were in total {comb_data['#_movies_loaded']} movie(s) found in '{filename}'")

    comb_data['#_conditions'] = len(data['input_parameter']['condition_names'])  # number of conditions
    comb_data['#_movies_per_condition'] = [len(movies) for movies in data['input_parameter']['condition_files']]  # movies per condition
    comb_data['condition_names'] = data['input_parameter']['condition_names']
    comb_data['condition_files'] = data['input_parameter']['condition_files']

    # Check whether any combining is possible
    if comb_data['#_conditions'] == 0:
        raise ValueError('Please set a number of combinable files in define_input_parameters.py (Option 1)')

    # # Assign data to a combined table
    tmp_max_track_id = 0
    tmp_max_frame = 0
    condi_table = {}
    condi_table['cell_data'] = {} 
    condi_table['diff_data'] = {} 
    condi_table['anaDDA_tracks'] = {} 
    # condi_table['anaDDA_condis'] = []
    condi_table['condis_#_cells'] = {}

    for ff in range(comb_data['#_conditions']):
        tmp_scta_table = data['movies'][ff]['scta_table'].iloc[0:0].copy()
        tmp_dcoef_table = data['movies'][ff]['diff_coeffs_filtered_list'].iloc[0:0].copy()
        tmp_tracks_table = data['movies'][ff]['tracks'].iloc[0:0].copy()

        # Check whether data is loaded that doesn't exist
        if max(comb_data['condition_files'][ff]) > comb_data['#_movies_loaded']:
            raise ValueError('Please check: You are trying to load a non-existing movie!')

        # For each movie per condition
        for jj in range(comb_data['#_movies_per_condition'][ff]):

            tmp_ParaNr = comb_data['condition_files'][ff][jj]  # current movie ID
            tmp_scta_table = pd.concat(
                [tmp_scta_table, data['movies'][tmp_ParaNr]['scta_table']], ignore_index=True)  # append cellwise data
            tmp_dcoef_table = pd.concat(
                [tmp_dcoef_table, data['movies'][tmp_ParaNr]['diff_coeffs_filtered_list']], ignore_index=True)  # append diffcoefficients
            
            # --- append tracks of condition for anaDDA:
            # A. Use all localisations in valid cells; not filtered for 'DiffHistSteps' and 'numberTracksPerCell'
            tmp_tracks = data['movies'][tmp_ParaNr]['tracks'].copy()
            # B. Use localisations in valid cells, filtered for 'diff_hist_steps' and '#_tracks_per_cell'    
            #tmp_tracks = data['movies'][tmp_ParaNr]['tracks_filtered'].copy()
            
            tmp_tracks.loc[:, 'track_id'] += tmp_max_track_id  # update track_id for continuous assignments
            # breakpoint()
            tmp_tracks.loc[:, 'frame'] += tmp_max_frame  # update frame_id for continuous assignments
            
            tmp_tracks_table = pd.concat([tmp_tracks_table, tmp_tracks], ignore_index=True)  # append diffcoefficients
            
            tmp_max_track_id = max(tmp_tracks_table['track_id'])  # tmp_id for shifting track_id
            tmp_max_frame = max(tmp_tracks_table['frame'])  # tmp_id for shifting frame_id
            
        # Store important variables
        condi_table['cell_data'][ff] = tmp_scta_table  # a
        condi_table['diff_data'][ff] = tmp_dcoef_table  # all diffcoefficients per condition
       
        anaDDA_tracks = tmp_tracks_table[['x [µm]', 'y [µm]', 'frame', 'track_id']] 
        anaDDA_tracks['frametime'] = data['input_parameter']['frametime']
        condi_table['anaDDA_tracks'][ff] = anaDDA_tracks

        # condi_table['anaDDA_condis'].append(f"anaDDA: {comb_data['condition_names'][ff]}")
        condi_table['condis_#_cells'][ff] = len(tmp_scta_table)  # how many valid cells per condition

    comb_data['cell_data'] = condi_table['cell_data']
    comb_data['diff_data'] = condi_table['diff_data']
    comb_data['anaDDA_tracks'] = condi_table['anaDDA_tracks']
    # comb_data['anaDDA_condis']= condi_table['anaDDA_condis']
    comb_data['condis_#_cells'] = condi_table['condis_#_cells']
    comb_data['input_parameter'] = data['input_parameter']

    # 3. Save comb_data dictionary
    temp_path = os.path.join(data['input_parameter']['data_dir'], data['input_parameter']['default_output_dir'])
    with open(temp_path + data['input_parameter']['fn_combined_movies'], 'wb') as f:
        pickle.dump(comb_data, f)
        
    print(f"  Analysis of infividual movie(s) saved as pickle file: {data['input_parameter']['fn_combined_movies']}")
 
    return comb_data



