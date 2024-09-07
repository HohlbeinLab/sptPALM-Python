#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

# Transforming thunderSTORM.csv files to _analysis.csv files for further downstream processing
# First, load localisation data from ThunderSTORM ('*_thunder.csv') and
# convert it to '*_py_save_csv.csv' table and add para.movieNumber to the file
# Note that localisations from ThunderSTORM use unit of nanometer (not pixels)! 
# author: Johannes Hohlbein, 07.09.2024

import pandas as pd
import numpy as np
import os

def load_csv(para):
    
    # Import *.csv data (for example obtained from running ThunderSTORM)
    print(f" pathname = {para['data_pathname']}")  
    print(f" load_filename(s) [csv] = {para['fn_locs_csv']}")    
    csv_input_file = pd.read_csv(para['data_pathname'] + para['fn_locs_csv'])

    # Change x,y,z from thunderSTORM from nm to um
    try:
        csv_input_file['x [nm]'] = csv_input_file['x [nm]'] /1000
        csv_input_file['y [nm]'] = csv_input_file['y [nm]'] /1000
        csv_input_file['z [nm]'] = csv_input_file['z [nm]'] /1000
    except: 
        print("\n ATTENTION, 'Something went wrong in going from nm to um !")
        input("Press Enter to continue...\n")


    # Create a list of column names matching our internal naming 
    # to external naming such as, e.g., provided by ThunderSTORM
    int_ext_headers = [('loc_id', 'id'), 
                       ('movie_id', ''),
                       ('frame', 'frame'),
                       ('cell_id', ''), 
                       ('track_id', ''),
                       ('x [um]', 'x [nm]'),
                       ('y [um]', 'y [nm]'), 
                       ('z [nm]', 'z [nm]'),
                       ('brightness', 'intensity [photon]'), 
                       ('background', 'bkgstd [photon]'), 
                       ('i0', 'offset [photon]'),
                       ('sx', 'sigma1 [nm]'),
                       ('sy', 'sigma2 [nm]'),
                       ('cell_area_id', '')]
    
    # Create data frame and the names into separate columns
    df = pd.DataFrame(int_ext_headers, columns=['internal_naming', 'external_naming'])
   
    # Define the output columns
    csv_header = df['internal_naming'].tolist()
 
    # Initialize the output DataFrame
    csv_data = pd.DataFrame(np.nan, index=np.arange(len(csv_input_file)), columns=csv_header)

    # Loop through each row of the DataFrame
    for index, row in df.iterrows():
        # Read columns
        if row['internal_naming'] == 'movie_id': # Fill 'movie_id' column (preset to 1)
            csv_data['movie_id'] = para['movie_number']
        elif row['internal_naming'] == 'cell_id': # Fill 'cells_id' column (preset to -1)
            csv_data['cell_id'] = -1
        elif row['internal_naming'] == 'track_id':  # Fill 'track_id' column (preset to -1)
            csv_data['track_id'] = -1
        elif row['internal_naming'] == 'cell_area_id':
            csv_data['cell_area_id'] = 0
        else: # read data from provided *.csv file
            try:
                csv_data[row['internal_naming']] = csv_input_file[row['external_naming']]
            except: 
                print(f"\n ATTENTION, '{row['external_naming']}' not found in {para['fn_locs_csv']} !")
                input("Press Enter to continue...")
        print(f" Data read or defined: {row['internal_naming']} {row['external_naming']}")
        
    # Export the '*_analysis.csv' file
    temp_path = os.path.join(para['data_pathname'], para['default_output_folder'])
    csv_data.to_csv(temp_path + para['fn_locs_csv'][:-4] + para['fn_csv_handle'], index=False, quoting=0)
    para['output_table'] = csv_data
    print(f"\nConversion of *thunder.csv to {para['fn_locs_csv'][:-4] + para['fn_csv_handle']} done!")

    return para
