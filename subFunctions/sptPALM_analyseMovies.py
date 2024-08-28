#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

import tkinter as tk
from tkinter import simpledialog, filedialog
import os
import sys
from pathlib import Path

# Add the subfolder to the Python path
sys.path.append(str(Path('subFunctions')))

from sptPALM_analyseMovies import sptPALM_analyseMovies


def define_input_parameters():
    # Placeholder function for DefineInputParameters.
    # You need to implement this function based on the actual MATLAB code or requirements.
    return {
        "dataFileNameMat": "sptDataMovies.mat",
        "filename_thunderstormCSV": None,
        "dataPathName": None
    }

def sptPALM_analyseMovies():
    # 1.1 Define input parameters
    print('Run define_input_parameters()')
    inputParameter = define_input_parameters()

    # Allow savename to be changed (default: 'sptDataMovies.mat')
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    prompt = "Enter new name for saving sptDataMovies.mat or press OK/Enter"
    inputParameter['dataFileNameMat'] = simpledialog.askstring("Rename sptDataMovies.mat?", prompt, initialvalue='sptDataMovies.mat')

    # Convert to string if it's None
    if inputParameter['dataFileNameMat'] is None:
        inputParameter['dataFileNameMat'] = 'sptDataMovies.mat'

    # Fall-back to GUI if no list of ThunderSTORM CSV files is specified
    if not inputParameter['filename_thunderstormCSV']:
        files = filedialog.askopenfilenames(
            title="Select *.csv export from ThunderSTORM",
            filetypes=[("CSV files", "*_thunder.csv")]
        )
        
        inputParameter['filename_thunderstormCSV'] = list(files)
        if files:
            inputParameter['dataPathName'] = os.path.dirname(files[0])
            os.chdir(inputParameter['dataPathName'])

    return inputParameter

# Example usage
DATA, Para1 = sptPALM_analyseMovies()
