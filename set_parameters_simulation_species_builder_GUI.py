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
import tkinter as tk
from tkinter import messagebox
import numpy as np

class SpeciesManager:
    def __init__(self, root, sim_input):
        self.root = root
        self.root.title("Species Manager")

        # Extract any existing species data from sim_input
        self.sim_input = sim_input
        self.species_list = []

        # Define headers for the table
        headers = ["Number of states\n currently 1, 2, 3, or 4 ",
                   "diff_quot (µm^2/s)\n separate by ','",
                   "rates ((s^-1)\n 1: [0], 2: [kAB, kBA],\n 3: [kAB, kBA, kBC, kCB, kAC, kCA],"
                   "\n 4(lin): [kAB, kBA, kBC, kCB, kCD, kDC]",
                   "Fiting: diff_quot_init_guess",
                   "Fitting: rates_init_guess \n structure: see rates",
                   "Fitting: diff_quot_lb_ub \n [diff_quot_min][diff_quot_max]",
                   "Fitting: rates_lb_ub \n [rates_min][rates_max]", '+']

        # Create header labels
        for i, header in enumerate(headers):
            tk.Label(root, text=header).grid(row=0, column=i)

        # If there are existing species, prepopulate rows with their data
        for species in self.sim_input.get('species', []):
            self.add_row(species)

        # Add an empty row for adding new species
        self.add_row()

        # Save button to collect all the species and update sim_input
        self.save_button = tk.Button(root, text="Save", command=self.save_species)
        self.save_button.grid(row=len(self.species_list) + 2, column=0, columnspan=7)

    def add_row(self, species=None):
        """
        Add a row of species data. If species data is provided, prepopulate the fields.
        """
        row_entries = {}

        # Create entry fields for each species parameter
        num_states = tk.Entry(self.root)
        diff_quot = tk.Entry(self.root)
        rates = tk.Entry(self.root)
        diff_quot_init_guess = tk.Entry(self.root)
        rates_init_guess = tk.Entry(self.root)
        diff_quot_lb_ub = tk.Entry(self.root)
        rates_lb_ub = tk.Entry(self.root)

        if species:
            # Prepopulate the fields with species data
            num_states.insert(0, str(species.get('#_states', '')))
            diff_quot.insert(0, ', '.join(map(str, species.get('diff_quot', []))))
            rates.insert(0, ', '.join(map(str, species.get('rates', []))))
            diff_quot_init_guess.insert(0, ', '.join(map(str, species.get('diff_quot_init_guess', []))))
            rates_init_guess.insert(0, ', '.join(map(str, species.get('rates_init_guess', []))))
            diff_quot_lb_ub.insert(0, ', '.join(map(str, species.get('diff_quot_lb_ub', []))))
            rates_lb_ub.insert(0, ', '.join(map(str, species.get('rates_lb_ub'))))

        # Place each entry widget into the grid
        row = len(self.species_list) + 1
        num_states.grid(row=row, column=0)
        diff_quot.grid(row=row, column=1)
        rates.grid(row=row, column=2)
        diff_quot_init_guess.grid(row=row, column=3)
        rates_init_guess.grid(row=row, column=4)
        diff_quot_lb_ub.grid(row=row, column=5)
        rates_lb_ub.grid(row=row, column=6)

        # Add "+" button to add more rows
        add_button = tk.Button(self.root, text="+", command=self.add_row)
        add_button.grid(row=row, column=7)

        # Store the entry widgets in a list for retrieval later
        row_entries['#_states'] = num_states
        row_entries['diff_quot'] = diff_quot
        row_entries['rates'] = rates
        row_entries['diff_quot_init_guess'] = diff_quot_init_guess
        row_entries['rates_init_guess'] = rates_init_guess
        row_entries['diff_quot_lb_ub'] = diff_quot_lb_ub
        row_entries['rates_lb_ub'] = rates_lb_ub

        # Append to species list for later data retrieval
        self.species_list.append(row_entries)

    def save_species(self):
        """
        Save all species data into sim_input.
        """
        sim_input = {'species': []}

        for row in self.species_list:
            species = {
                '#_states': int(row['#_states'].get()),  # Get the value from Entry
                'diff_quot': np.array([float(x) for x in row['diff_quot'].get().split(',')]),  # Split and convert to float
                'rates': np.array([float(x) for x in row['rates'].get().split(',')]),  # Split and convert to float
                'diff_quot_init_guess': np.array([float(x) for x in row['diff_quot_init_guess'].get().split(',')]),
                'rates_init_guess': np.array([float(x) for x in row['rates_init_guess'].get().split(',')]),
                'diff_quot_lb_ub': np.array([list(map(float, x.split())) for x in row['diff_quot_lb_ub'].get().split(',')]),
                'rates_lb_ub': np.array([list(map(float, x.split())) for x in row['rates_lb_ub'].get().split(',')])
            }
            sim_input['species'].append(species)

        # Display a message box to confirm saving
        messagebox.showinfo("Saved", "Species data saved successfully!")
        print(sim_input)  # For debugging purposes

# Example sim_input structure
sim_input = {
    'species': [
        {
            '#_states': 2,
            'diff_quot': np.array([0.001, 2.8]),
            'rates': np.array([155, 137]),
            'diff_quot_init_guess': np.array([0.001, 2.8]),
            'diff_quot_lb_ub': np.array([[0, 1.], [0.002, 5.]]),
            'rates_init_guess': np.array([155, 137]),
            'rates_lb_ub': np.array([[10, 10], [200, 500]])
        }
    ],
    'avoidFloat0': 0.001,
    'multiplicator': 1.5
}

# Create the main window and run the app
root = tk.Tk()
app = SpeciesManager(root, sim_input)
root.mainloop()

