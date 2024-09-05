#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sept 01 20:58:09 2024

@author: hohlbein
"""


import pandas as pd
import numpy as np

# # Create a list of full names
# full_names = [('Alice', 'Smith'), 
#               ('Bob', 'Jones'),
#               ('Carl', 'Huang')]

# # Split the names into separate columns
# df = pd.DataFrame(full_names, columns=['internal', 'external'])

# # Display the DataFrame
# print(df) 

# # Loop through each row of the DataFrame
# for index, row in df.iterrows():
#     print(f"{row['internal']} {row['external']}")


    
# Create a list of column names matching our internal naming 
# to external naming such as, e.g., provided by ThunderSTORM
int_ext_headers = [['loc_id', 'id'], 
                    ['movie_id', 'EMPTY'],
                    ['frame_id', 'frame'],
                    ['cell_id', 'cell_id'], 
                    ['track_id', 'EMPTY'],
                    ['x [nm]', 'x [nm]'],
                    ['y [nm]', 'y [nm]'], 
                    ['z [nm]', 'z [nm]'],
                    ['brightness', 'intensity [photon]'], 
                    ['background', 'bkgstd [photon]'], 
                    ['i0', 'offset [photon]'],
                    ['sx', 'sigma1 [nm]'],
                    ['sy', 'sigma2 [nm]'],
                    ['cell_area_id', 'EMPTY']]

# Split the names into separate columns
df = pd.DataFrame(int_ext_headers, columns=['internal', 'external'])

# Display the DataFrame
print(df) 
  
csv_header = df['internal'].tolist()

# Initialize the output DataFrame
csv_output_file = pd.DataFrame(np.nan, index=np.arange(10), columns=csv_header)
