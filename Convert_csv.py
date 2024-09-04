#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

# Transforming thunderSTORM.csv files to _analysis.csv files for further downstream processing
# First, load localisation data from ThunderSTORM ('*_thunder.csv') and
# convert it to '*_thunder-analysis.csv' table and add para.movieNumber to the file
# Note that localisations from ThunderSTORM use unit of nanometer (not pixels)! 
# author: Johannes Hohlbein, 14.08.2022


import pandas as pd
import numpy as np

def convert_csv(para):
    # Import *.csv data (for example obtained from running ThunderSTORM)
    load_file = para['data_pathname'] + para['filename_thunderstorm_csv']
    print(f' loadFile [csv] = {load_file}')
    
    csv_input_file = pd.read_csv(load_file)

    # Prepare output file
    para['filename_analysis_csv'] = para['filename_thunderstorm_csv'][:-4] + '_analysis.csv'
    save_file = para['data_pathname'] + para['filename_analysis_csv']
    print(f' save_file [csv] = {save_file}')

    # Define the output columns
    csv_header = ['loc_id', 'movie_id', 'frame_id', 'cell_id', 'track_id', 
                  'x [nm]', 'y [nm]', 'z [nm]', 'brightness', 'background', 
                  'i0', 'sx', 'sy', 'cell_area_id']
    
    # Initialize the output DataFrame
    csv_output_file = pd.DataFrame(np.nan, index=np.arange(len(csv_input_file)), columns=csv_header)

    # Find all column numbers with some header strings from the initial *.csv table
    # (defined by settings in ThunderSTORM!)
    columns_map = {
        'id_column': csv_input_file.columns.get_loc('id') if 'id' in csv_input_file.columns else None,
        'frame_column': csv_input_file.columns.get_loc('frame') if 'frame' in csv_input_file.columns else None,
        'x_column': csv_input_file.columns.get_loc('x [nm]') if 'x [nm]' in csv_input_file.columns else None,
        'y_column': csv_input_file.columns.get_loc('y [nm]') if 'y [nm]' in csv_input_file.columns else None,
        'z_column': csv_input_file.columns.get_loc('z [nm]') if 'z [nm]' in csv_input_file.columns else None,
        'intensity_column': csv_input_file.columns.get_loc('intensity [photon]') if 'intensity [photon]' in csv_input_file.columns else None,
        'offset_column': csv_input_file.columns.get_loc('offset [photon]') if 'offset [photon]' in csv_input_file.columns else None,
        'bkgstd_column': csv_input_file.columns.get_loc('bkgstd [photon]') if 'bkgstd [photon]' in csv_input_file.columns else None,
        'sx_column': csv_input_file.columns.get_loc('sigma1 [nm]') if 'sigma1 [nm]' in csv_input_file.columns else None,
        'sy_column': csv_input_file.columns.get_loc('sigma2 [nm]') if 'sigma2 [nm]' in csv_input_file.columns else None
    }

    # Fill in the output DataFrame based on the mappings
    
    # Fill 'loc_id' column
    if columns_map['id_column'] is not None:
        csv_output_file['loc_id'] = csv_input_file.iloc[:, columns_map['id_column']]
        
    # Fill 'movie_id' column (preset to 1)
    csv_output_file['movie_id'] = para['movie_number']
    
    # Fill 'frames_id' column
    if columns_map['frame_column'] is not None:
        csv_output_file['frame_id'] = csv_input_file.iloc[:, columns_map['frame_column']]
    
    # Fill 'cells_id' column (preset to -1)
    csv_output_file['cell_id'] = -1
    
    # Fill 'track_id' column (preset to -1)
    csv_output_file['track_id'] = -1

    # Fill x positions
    if columns_map['x_column'] is not None:
        csv_output_file['x [nm]'] = csv_input_file.iloc[:, columns_map['x_column']]
  
    # Fill y positions
    if columns_map['y_column'] is not None:
        csv_output_file['y [nm]'] = csv_input_file.iloc[:, columns_map['y_column']]
    
    # Fill z positions
    if columns_map['z_column'] is not None:
        csv_output_file['z [nm]'] = csv_input_file.iloc[:, columns_map['z_column']]
    
    # Fill intensities
    if columns_map['intensity_column'] is not None:
        csv_output_file['brightness'] = csv_input_file.iloc[:, columns_map['intensity_column']]
    
    # Fill background intensities (?)
    if columns_map['offset_column'] is not None:
        csv_output_file['background'] = csv_input_file.iloc[:, columns_map['offset_column']]

    # Fill background intensities (?)    
    if columns_map['bkgstd_column'] is not None:
        csv_output_file['i0'] = csv_input_file.iloc[:, columns_map['bkgstd_column']]
    
    # Fill localisation error sigma x
    if columns_map['sx_column'] is not None:
        csv_output_file['sx'] = csv_input_file.iloc[:, columns_map['sx_column']]
  
    # Fill localisation error sigma y
    if columns_map['sy_column'] is not None:
        csv_output_file['sy'] = csv_input_file.iloc[:, columns_map['sy_column']]
    
    csv_output_file['cell_area_id'] = 0

    # Export the '*_analysis.csv' file
    csv_output_file.to_csv(save_file, index=False, quoting=0)
    para['output_table'] = csv_output_file
    print('\nConversion of *thunder.csv to *_analysis.csv done!\n')

    return para
