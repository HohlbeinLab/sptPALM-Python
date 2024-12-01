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

import os
import pandas as pd
from tkinter import Tk, filedialog, simpledialog


import os
import pandas as pd
from tkinter import Tk, filedialog


def combine_thunderstorm_csv_files():
    # Option A: Graphical User Interface for selecting files
    root = Tk()
    root.withdraw()  # Hide the root window

    csv_filenames = filedialog.askopenfilenames(
        title="Select csv export from ThunderSTORM",
        filetypes=[("ThunderSTORM CSV files", "*.csv")]
    )
    if not csv_filenames:
        print("No files selected. Exiting.")
        return

    # Get the directory of the input files
    input_dir = os.path.dirname(csv_filenames[0])

    # Ask for output file name via command line
    output_file_name = input(
        "Enter new name for saving OutputCombined_thunder.csv (press Enter to use default: OutputCombined_thunder.csv): "
    ).strip()

    # GUI version: Prompt for output file name
    # output_file_name = simpledialog.askstring(
    #     title="Rename OutputCombined_thunder.csv?",
    #     prompt="Enter new name for saving OutputCombined_thunder.csv or press OK/Enter",
    #     initialvalue="OutputCombined_thunder.csv"
    # )

    if not output_file_name:
        output_file_name = "OutputCombined_thunder.csv"

    # Combine the directory with the file name to save in the input directory
    output_file_path = os.path.join(input_dir, output_file_name)
    print(f"Output file will be saved at: {output_file_path}")

    # Allow user to reorder files (optional)
    csv_filenames_new = check_input_order(csv_filenames)

    # Combine files
    table_temp = pd.DataFrame()

    for jj, filename in enumerate(csv_filenames_new):
        print(f"File {jj} loaded: {filename}")
        table_temp2 = pd.read_csv(filename)

        # Adjust offset for columns 'id' and 'frame'
        if jj > 0:
            offset_id = table_temp['id'].max()
            offset_frame = table_temp['frame'].max()
            table_temp2['id'] += offset_id
            table_temp2['frame'] += offset_frame

        table_temp = pd.concat([table_temp, table_temp2], ignore_index=True)

    # Fix headers (add quotes around column names)
    table_temp.columns = [f'"{col}"' for col in table_temp.columns]

    # Write to output CSV
    table_temp.to_csv(output_file_path, index=False, quoting=3)  # quoting=3 avoids quotes around strings
    print(f"Data written into {output_file_path}.")


def check_input_order(csv_filenames):
    """
    Allow the user to confirm or reorder the list of input files, using zero-based indexing.
    """
    print("Number of CSV filenames:", len(csv_filenames))
    for i, filename in enumerate(csv_filenames):  # Zero-based indexing
        print(f"{i}: {filename}")

    while True:
        prompt = input("Is the order of files correct (0: no, 1: yes): ")
        if prompt == '1':
            print("Order of files seems to be fine!")
            return list(csv_filenames)
        elif prompt == '0':
            new_order_input = input("Provide list of file numbers in correct order (e.g. 2,0,3): ")
            try:
                # Convert input to a list of indices and reorder files
                new_order = list(map(int, new_order_input.split(',')))
                csv_filenames_new = [csv_filenames[i] for i in new_order]
                for i, filename in enumerate(csv_filenames_new):  # Zero-based indexing
                    print(f"{i}: {filename}")
                return csv_filenames_new
            except (ValueError, IndexError):
                print("Invalid input! Please try again.")
        else:
            print("Invalid choice. Please enter 0 or 1.")

# if __name__ == "__main__":
#     combine_thunderstorm_csv_files()
