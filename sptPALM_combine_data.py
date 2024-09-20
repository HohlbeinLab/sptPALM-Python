#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


import scipy.io as sio
import numpy as np
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
import os
import pickle
from define_input_parameters import define_input_parameters

def sptPALM_combine_data(data=None):
    
    print('\nRun sptPALM_combine_data()')

    # loaded more as a dummy here: define input parameters
    input_parameter = define_input_parameters()
    
    # # 1.1 Check whether DATA was passed to the function
    # if data is None:
    #     # Use Tkinter for file dialog
    #     Tk().withdraw()  # Close root window
    #     starting_directory = os.path.join(input_parameter['data_dir'],
    #                                               input_parameter['default_output_dir'])
    #     filename = askopenfilename(initialdir = starting_directory, 
    #                                 filetypes = [("pickle file", "*.pkl")],
    #                                 title = "Select *.pkl file from sptPALM_analyse_movies.py")
    #     if filename:
    #         with open(filename, 'rb') as f:
    #             data = pickle.load(f)
    #     else:
    #         raise ValueError("No file selected!")
    # else:
    #     filename = None
    
    # For bugfixing - Replace the following line with your file path if needed
    filename = '/Users/hohlbein/Documents/WORK-DATA-local/TestData_CRISPR-Cas/output_python/sptData_movies.pkl'
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    
    temp = data[0]

    # Optional part to modify input parameters before combining data
    # Placeholder for define_input_parameters.py functionality

    # Allow savename to be changed (default: 'sptData_combined_movies.pkl')
    input_parameter['fn_combined_movies'] = askstring(f"Rename {input_parameter['fn_combined_movies']}?", 
                              f"Enter new name for saving {input_parameter['fn_combined_movies']} or press OK/Enter", 
                              initialvalue=input_parameter['fn_combined_movies'])

    breakpoint()

 #TEMPORARILY DISABLED (to avoid pausing execution of the analysis}
    # fn_output_default = input_parameter['fn_combined_data']
    # user_input = input(f"  Enter string or press enter (default is: {n_output_default}): ")
    # if not user_input:
    #      user_input = fn_output_default 
    # input_parameter['fn_combined_output'] = user_input


    
    CombinedDATA = {}
    # CombinedDATA['NumberMoviesLoaded'] = len(DATA['MOVIES'])
    # print(f"... there were in total {CombinedDATA['NumberMoviesLoaded']} movie(s) found in '{filename}'")

    # CombinedDATA['numberConditions'] = len(DATA['inputParameter']['Condition_name'])  # number of conditions
    # CombinedDATA['numberMoviesPerCondition'] = [len(cond_files) for cond_files in DATA['inputParameter']['Condition_files']]  # movies per condition
    
    # CombinedDATA['Condition_name'] = DATA['inputParameter']['Condition_name']
    # CombinedDATA['Condition_files'] = DATA['inputParameter']['Condition_files']

    # # Check whether any combining is possible
    # if CombinedDATA['numberConditions'] == 0:
    #     raise ValueError('Please set a number of combinable files in DefineInputParameters.m (Option 1)')

    # # Assign data to a combined table
    # tmp_id = 0
    # condi_table_Celldata = []
    # condi_table_Diffdata = []
    # condi_table_anaDDAtracks = []
    # condis_numberCells = []

    # for ff in range(CombinedDATA['numberConditions']):
    #     tmp_SCTA_table = []
    #     tmp_Dcoef_table = []
    #     tmp_tracks_table = []

    #     # Check whether data is loaded that doesn't exist
    #     if max(CombinedDATA['Condition_files'][ff]) > CombinedDATA['NumberMoviesLoaded']:
    #         raise ValueError('Please check (1.2): You are trying to load a non-existing movie!')

    #     # For each movie per condition
    #     for jj in range(CombinedDATA['numberMoviesPerCondition'][ff]):
    #         tmp_ParaNr = CombinedDATA['Condition_files'][ff][jj]  # current movie ID
    #         tmp_SCTA_table.extend(DATA['MOVIES'][tmp_ParaNr]['SCTA_table'])  # append cellwise data
    #         tmp_Dcoef_table.extend(DATA['MOVIES'][tmp_ParaNr]['DiffCoeffsList'])  # append diffcoefficients
            
    #         # --- append tracks of condition for anaDDA:
    #         tmp_tracks = np.array(DATA['MOVIES'][tmp_ParaNr]['tracks_filtered']) / [1000, 1000, 1, 1]  # rescale to um
    #         tmp_tracks[:, 3] += tmp_id  # update trackID for continuous assignments
    #         tmp_tracks_table.extend(tmp_tracks)  # append tracker tracks (for anaDDA)
    #         tmp_id = tmp_tracks_table[-1][3]  # tmp_id for shifting trackID

    #     # Store important variables
    #     condi_table_Celldata.append(tmp_SCTA_table)  # all cellwise data per condition
    #     condi_table_Diffdata.append(tmp_Dcoef_table)  # all diffcoefficients per condition
        
    #     # Use anaDDA format for tracks
    #     tmp_tracks_table = np.array(tmp_tracks_table)
    #     anaDDA_tracks = np.column_stack((tmp_tracks_table[:, :3], pd.factorize(tmp_tracks_table[:, 3])[0], 
    #                                      np.ones(tmp_tracks_table.shape[0]) * DATA['inputParameter']['frametime']))
        
    #     condi_table_anaDDAtracks.append([anaDDA_tracks, f"anaDDA: {CombinedDATA['Condition_name'][ff]}"])
    #     condis_numberCells.append(len(tmp_SCTA_table))  # how many valid cells per condition

    # CombinedDATA['condi_table_Celldata'] = condi_table_Celldata
    # CombinedDATA['condi_table_Diffdata'] = condi_table_Diffdata
    # CombinedDATA['condi_table_anaDDAtracks'] = condi_table_anaDDAtracks
    # CombinedDATA['condis_numberCells'] = condis_numberCells
    # CombinedDATA['inputParameter'] = DATA['inputParameter']

    # # Save combined data
    # sio.savemat(f"{DATA['inputParameter']['dataPathOutp']}/{saveFileName}", CombinedDATA, do_compression=True)

    return CombinedDATA



