#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

# Transforming thunderSTORM.csv files to _analysis.csv files for further downstream processing
# First, load localisation data from ThunderSTORM ('*_thunder.csv') and
# convert it to '*_thunder_analysis.csv' table and add para.movieNumber to the file
# Note that localisations from ThunderSTORM use unit of nanometer (not pixels)! 
# author: Johannes Hohlbein, 14.08.2022

import pandas as pd
import numpy as np

def load_csv(para):
    
    # Import *.csv data (for example obtained from running ThunderSTORM)
    load_file = para['data_pathname'] + para['filename_thunderstorm_csv']
    print(f' loadFile [csv] = {load_file}')    
    csv_input_file = pd.read_csv(load_file)

    # Prepare output file
    para['filename_analysis_csv'] = para['filename_thunderstorm_csv'][:-4] + '_analysis.csv'
    save_file = para['data_pathname'] + para['filename_analysis_csv']
    print(f' save_file [csv] = {save_file}')

    # Create a list of column names matching our internal naming 
    # to external naming such as, e.g., provided by ThunderSTORM
    int_ext_headers = [('loc_id', 'id'), 
                       ('movie_id', ''),
                       ('frame', 'frame'),
                       ('cell_id', ''), 
                       ('track_id', ''),
                       ('x [nm]', 'x [nm]'),
                       ('y [nm]', 'y [nm]'), 
                       ('z [nm]', 'z [nm]'),
                       ('brightness', 'intensity [photon]'), 
                       ('background', 'bkgstd [photon]'), 
                       ('i0', 'offset [photon]'),
                       ('sx', 'sigma1 [nm]'),
                       ('sy', 'sigma2 [nm]'),
                       ('cell_area_id', '')]
    
    # Create data frame and the names into separate columns
    df = pd.DataFrame(int_ext_headers, columns=['internal', 'external'])
   
    # Define the output columns
    csv_header = df['internal'].tolist()
 
    # Initialize the output DataFrame
    csv_output_file = pd.DataFrame(np.nan, index=np.arange(len(csv_input_file)), columns=csv_header)

    # Loop through each row of the DataFrame
    for index, row in df.iterrows():
        # Read columns
        if row['internal'] == 'movie_id': # Fill 'movie_id' column (preset to 1)
            csv_output_file['movie_id'] = para['movie_number']
        elif row['internal'] == 'cell_id': # Fill 'cells_id' column (preset to -1)
            csv_output_file['cell_id'] = -1
        elif row['internal'] == 'track_id':  # Fill 'track_id' column (preset to -1)
            csv_output_file['track_id'] = -1
        elif row['internal'] == 'cell_area_id':
            csv_output_file['cell_area_id'] = 0
        else: # read data from provided *.csv file
            try:
                csv_output_file[row['internal']] = csv_input_file[row['external']]
            except: 
                print(f"\n ATTENTION, '{row['external']}' not found in {load_file} !")
                input("Press Enter to continue...")
        print(f" Data read or defined: {row['internal']} {row['external']}")
        
    # Export the '*_analysis.csv' file
    csv_output_file.to_csv(save_file, index=False, quoting=0)
    para['output_table'] = csv_output_file
    print('\nConversion of *thunder.csv to *_analysis.csv done!\n')

    return para
