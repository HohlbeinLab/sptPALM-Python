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

def load_localisations_from_csv(para):
    print('\nRun load_localisations_from_csv.py')
    # Import *.csv data (for example obtained from running ThunderSTORM)
    print(f"  Pathname: {para['data_dir']}")  
    print(f"  Load_filename(s) [csv]: {para['fn_locs']}")    
    csv_input_file = pd.read_csv(para['data_dir'] + para['fn_locs'])

    # Change x,y,z from thunderSTORM from nm to um
    columns_temp = ['x [nm]', 'y [nm]', 'z [nm]']
    
    # Loop through the columns and check for existence
    for ii in range(len(columns_temp)):
        if columns_temp[ii] in csv_input_file.columns:
            print(f"  Column '{columns_temp[ii]}' exists.")
            csv_input_file[columns_temp[ii]] = csv_input_file[columns_temp[ii]]/1000  # Convert nm to µm
            print("  Conversion of localisations from nm to µm done!")
        else:
            print(f"  Column '{columns_temp[ii]}' does not exist!")  

    # Create a list of column names matching our internal naming 
    # to external naming such as, e.g., provided by ThunderSTORM
    int_ext_headers = [('loc_id', 'id'), 
                       ('movie_id', ''),
                       ('frame', 'frame'),
                       ('cell_id', ''), 
                       ('track_id', ''),
                       ('x [µm]', 'x [nm]'),
                       ('y [µm]', 'y [nm]'), 
                       ('z [µm]', 'z [nm]'),
                       ('brightness', 'intensity [photon]'), 
                       ('background', 'bkgstd [photon]'), 
                       ('i0', 'offset [photon]'),
                       ('sx', 'sigma1 [nm]'),
                       ('sy', 'sigma2 [nm]'),
                       ('cell_area', '')]
    
    # Create data frame and the names into separate columns
    df = pd.DataFrame(int_ext_headers, columns=['internal_naming', 'external_naming'])
   
    # Define the output columns
    csv_header = df['internal_naming'].tolist()
 
    # Initialize the output DataFrame
    csv_data = pd.DataFrame(np.nan, index=np.arange(len(csv_input_file)), columns=csv_header)

    # Loop through each row of the DataFrame
    print("  CSV-data columns: internal_naming <= external_naming")
    for index, row in df.iterrows():
        # Read columns
        if row['internal_naming'] == 'movie_id': # Fill 'movie_id' column (preset to 1)
            csv_data['movie_id'] = para['movie_number']
        elif row['internal_naming'] == 'cell_id': # Fill 'cells_id' column (preset to -1)
            csv_data['cell_id'] = -1
        elif row['internal_naming'] == 'track_id':  # Fill 'track_id' column (preset to -1)
            csv_data['track_id'] = -1
        elif row['internal_naming'] == 'cell_area':
            csv_data['cell_area_id'] = -1
        else: # read data from provided *.csv file after checking column exists

            if row['external_naming'] in csv_input_file.columns:
                csv_data[row['internal_naming']] = csv_input_file[row['external_naming']]
            else:
                print(f"\n ATTENTION, '{row['external_naming']}' not found in {para['fn_locs']}!")
                print(f"\n ATTENTION, '{row['external_naming']}' rows are set to -1!")
                csv_data[row['internal_naming']] = -1
                # input("Press Enter to continue...")
           
        print(f"   ...csv-data column: {row['internal_naming']} <= {row['external_naming']}")
    
    #For Python, convention is that everything should start at 0 (not 1), therefore
    csv_data['loc_id'] -= 1 if csv_data['loc_id'].min() == 1 else 0
    csv_data['frame'] -= 1 if csv_data['loc_id'].min() == 1 else 0
    
    # Export the '*_analysis.csv' file
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    csv_data.to_csv(temp_path + para['fn_locs'][:-4] + para['fn_csv_handle'], index=False, quoting=0)
    para['csv_data'] = csv_data
    print(f"  Conversion of *thunder.csv to {para['fn_locs'][:-4] + para['fn_csv_handle']} done!\n")

    return para
