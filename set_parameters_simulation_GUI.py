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
from tkinter import filedialog
import pickle
import numpy as np
from pathlib import Path
import threading
from set_parameters_simulation import set_parameters_simulation
import ast  # Safely parse the string back to a list of lists


def set_parameters_simulation_GUI(sim_input=None):

    print(" Run 'set_parameters_simulation_combined_GUI.py'")
    if sim_input is None:
        print("  Run 'set_parameters_simulation.py'")
        sim_input = set_parameters_simulation()

    def load_params():
        filename = filedialog.askopenfilename(
                                    filetypes=[("pickle file", "*.pkl")],
                                    title="Select *.pkl file")
        if filename:
            with open(filename, 'rb') as f:
                new_sim_input = pickle.load(f)
                print("Input parameters for simulation loaded")

            # Schedule the UI update to happen in the main thread
            root.after(0, update_ui, new_sim_input)  # Use 'after' to update Tkinter UI from the main thread
        else:
            raise ValueError("No file selected!")

    def update_ui(new_sim_input):
        """Update the UI with the parameters from the loaded file."""
        radius_cell_entry.delete(0, tk.END)
        radius_cell_entry.insert(0, new_sim_input['radius_cell'])

        length_cell_entry.delete(0, tk.END)
        length_cell_entry.insert(0, new_sim_input['length_cell'])

        tracklength_locs_min_entry.delete(0, tk.END)
        tracklength_locs_min_entry.insert(0, new_sim_input['tracklength_locs_min'])

        tracklength_locs_max_entry.delete(0, tk.END)
        tracklength_locs_max_entry.insert(0, new_sim_input['tracklength_locs_max'])

        mean_track_length_entry.delete(0, tk.END)
        mean_track_length_entry.insert(0, new_sim_input['mean_track_length'])

        confined_diffusion_var.set(False) # Not strictly necessary
        confined_diffusion_var.set(new_sim_input['confined_diffusion'])

        loc_error_entry.delete(0, tk.END)
        loc_error_entry.insert(0, new_sim_input['loc_error'])

        correct_diff_calc_loc_error_var.set(False) # Not strictly necessary
        correct_diff_calc_loc_error_var.set(new_sim_input['correct_diff_calc_loc_error'])

        oversampling_entry.delete(0, tk.END)
        oversampling_entry.insert(0, new_sim_input['oversampling'])

        frametime_entry.delete(0, tk.END)
        frametime_entry.insert(0, new_sim_input['frametime'])

        perform_fitting_var.set(False) # Not strictly necessary
        perform_fitting_var.set(new_sim_input['perform_fitting'])

        display_figures_var.set(False) # Not strictly necessary
        display_figures_var.set(new_sim_input['display_figures'])

        diff_hist_min_entry.delete(0, tk.END)
        diff_hist_min_entry.insert(0, new_sim_input['plot_diff_hist_min'])

        diff_hist_max_entry.delete(0, tk.END)
        diff_hist_max_entry.insert(0, new_sim_input['plot_diff_hist_max'])

        binwidth_entry.delete(0, tk.END)
        binwidth_entry.insert(0, new_sim_input['binwidth'])
        
        plot_option_var.set(False) # Not strictly necessary
        plot_option_var.set(new_sim_input['plot_option'])

        species_to_select_entry.delete(0, tk.END)
        species_to_select_entry.insert(0, new_sim_input['species_to_select'])

        avoidFloat0_entry.delete(0, tk.END)
        avoidFloat0_entry.insert(0, new_sim_input['avoidFloat0'])

        dpi_entry.delete(0, tk.END)
        dpi_entry.insert(0, new_sim_input['dpi'])

        # Update species in the SpeciesManager
        species_manager.load_species_data(new_sim_input['species'])

    # Collect all parameters from the GUI
    def transfer_params():
        nonlocal sim_input
        sim_input = {
            # Cell dimensions (in µm)
            'radius_cell': float(radius_cell_entry.get()),  # (µm) radius of the cap, edefault: 0.5
            'length_cell': float(length_cell_entry.get()),    # (µm) length of the cylindrical part, default: 2.0
            
            # Track lengths and diffusion constraints (also track_lengths': [1,2,3,4,5,6,7,8])
            'tracklength_locs_min': int(tracklength_locs_min_entry.get()),  # Track lengths (2 to 8 frames) tracklength of 1 is two locs, or track_lengths': [1,2,3,4,5,6,7,8]
            'tracklength_locs_max': int(tracklength_locs_max_entry.get()),  # Track lengths (2 to 8 frames) tracklength of 1 is two locs, or track_lengths': [1,2,3,4,5,6,7,8]
            'mean_track_length': float(mean_track_length_entry.get()),  # Mean track length for exponential distribution, default 3
            
            # Simulation parameters
            'confined_diffusion': bool(confined_diffusion_var.get()),  # Confine diffusion within a cell
            'loc_error': float(loc_error_entry.get()),  # (µm) Localization error (in µm), default: 0.035
            'correct_diff_calc_loc_error': bool(correct_diff_calc_loc_error_var.get()),  # Match anaDDA settings, default: False
            
            # Timing parameters
            'frametime': float(frametime_entry.get()),  # (s) frame time in seconds, default: 0.02
            'oversampling': int(oversampling_entry.get()),  # (s) factor by whoch framtetime is oversampled
            
            # Fitting and plotting options
            'perform_fitting': bool(perform_fitting_var.get()),  # Whether to perform fitting or not
            'display_figures': bool(display_figures_var.get()),  # Display figures
            'plot_diff_hist_min': float(diff_hist_min_entry.get()),  # Diffusion coefficient histogram min (µm^2/s), default: 0.004
            'plot_diff_hist_max': float(diff_hist_max_entry.get()),  # Diffusion coefficient histogram max (µm^2/s), deafult: 10.0
            'binwidth': float(binwidth_entry.get()),   # Bin width for histogram, default 0.1
            'species_to_select': int(species_to_select_entry.get()), # For fitting, only one species can be selected, set here which one, default:0
            'plot_option': plot_option_var.get(),# wether to plot D_histograms logarithmic or linear
            
            # Error handling values
            'avoidFloat0': float(avoidFloat0_entry.get()),  # To avoid rates being exactly zero, default: 1e-09
           
            # Here we extract raw values from the species manager:
            'species': extract_species_data(species_manager.return_species_list()),
        
            #Plotting stuff
            'dpi': int(dpi_entry.get()), # DPI setting for plotting figures, default: 300
            
         } 
        # Make sure that the track lengths are defined    
        sim_input['track_lengths'] = np.arange(sim_input['tracklength_locs_min']-1,
                                                    sim_input['tracklength_locs_max'])
    
        sim_input['#_species'] = len(sim_input['species'])
        print("sim_input transfered")
        return sim_input
    
    def save_params():
        transfer_params()
        current_directory = Path.cwd()
        save_file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            initialdir=current_directory,
            filetypes=[("pickle files", "*.pkl")],
            initialfile="sim_input_parameter.pkl",
            title="Save sim_input_parameter as"
        )
        if save_file_path:
            with open(save_file_path, 'wb') as file:
                pickle.dump(sim_input, file)
            print(f"Input parameters for simulation saved to {save_file_path}")
        else:
            print("Save operation canceled.")

    def extract_species_data(species_list):
        """Convert species list from Tkinter widgets to Python types for serialization, only if row is complete."""
        species_data = []
        for row in species_list:
            if is_row_complete(row):  # Check if the row has all required values
                species = {
                    '#_states': int(row['#_states'].get()),
                    '#_particles': int(row['#_particles'].get()),
                    'diff_quot': np.array([safe_float(x) for x in row['diff_quot'].get().split(',')]),
                    'rates': np.array([safe_float(x) for x in row['rates'].get().split(',')]),
                    'diff_quot_init_guess': np.array([safe_float(x) for x in row['diff_quot_init_guess'].get().split(',')]),
                    'rates_init_guess': np.array([safe_float(x) for x in row['rates_init_guess'].get().split(',')]),
                    'diff_quot_lb_ub': np.array(safe_literal_eval_with_nan(row['diff_quot_lb_ub'].get())),
                    'rates_lb_ub': np.array(safe_literal_eval_with_nan(row['rates_lb_ub'].get()))
                }
                species_data.append(species)
            else:
                print("Skipping incomplete row(s)!")
        return species_data
    
    def is_row_complete(row):
        """Check if all fields in the row are filled with values."""
        try:
            # Ensure no field is empty
            return all(row[field].get().strip() for field in ['#_states', 'diff_quot', 'rates', 'diff_quot_init_guess', 'rates_init_guess', 'diff_quot_lb_ub', 'rates_lb_ub'])
        except KeyError:
            return False  # If any field is missing, treat as incomplete
    
    def safe_float(value):
        """Convert string to float, handling 'nan'."""
        try:
            return float(value)
        except ValueError:
            if value.strip().lower() == 'nan':  # Check if it's 'nan'
                return np.nan
            raise  # Re-raise if it's another error
    
    def safe_literal_eval_with_nan(data):
        """Safely evaluate the string using literal_eval and handle 'nan'."""
        try:
            # Replace 'nan' with 'None' (which is handled by literal_eval)
            data = data.replace('nan', 'None')
            result = ast.literal_eval(data)
            # Convert any None back to np.nan after evaluating
            return convert_none_to_nan(result)
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing data: {data}, Error: {e}")
            return None  # Or return a default value
    
    def convert_none_to_nan(structure):
        """Recursively convert None values back to np.nan in nested structures."""
        if isinstance(structure, list):
            return [convert_none_to_nan(item) for item in structure]
        elif structure is None:
            return np.nan
        return structure

    def exit_GUI():
        transfer_params()
        root.quit()
        root.destroy()
        return sim_input


    root = tk.Tk()
    # Disable window resizing in both horizontal and vertical directions
    root.resizable(False, False)

    root.title("sptPALM simulation GUI (defaults imported from set_parameter_simulation.py)")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    left_frame = tk.Frame(root)
    left_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

    right_frame = tk.Frame(root)
    right_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

    width_text_labels = 22
    width_text_box = 8
    row_index = 0

    """
    # Frame for simulation I
    """
    sim_frame = tk.LabelFrame(left_frame, text="Parameters for simulation", padx=0, pady=0)
    sim_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ne")

    # Radius of cell (µm)
    tk.Label(sim_frame, text="Radius of cell (µm)", width=width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    radius_cell_entry = tk.Entry(sim_frame, width=width_text_box)
    radius_cell_entry.grid(row=row_index, column=1)
    radius_cell_entry.insert(0, sim_input['radius_cell'])

    # Length of cell (µm)
    tk.Label(sim_frame, text="Length of cell (µm)", width=width_text_labels, anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    length_cell_entry = tk.Entry(sim_frame, width=width_text_box)
    length_cell_entry.grid(row=row_index, column=3)
    length_cell_entry.insert(0, sim_input['length_cell'])

    # Tracklength: min locs
    row_index += 1
    tk.Label(sim_frame, text="Tracklength: min locs", width=width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    tracklength_locs_min_entry = tk.Entry(sim_frame, width=width_text_box)
    tracklength_locs_min_entry.grid(row=row_index, column=1)
    tracklength_locs_min_entry.insert(0, sim_input['tracklength_locs_min'])

    # Tracklength: max locs
    tk.Label(sim_frame, text="Tracklength: max locs", width=width_text_labels, anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    tracklength_locs_max_entry = tk.Entry(sim_frame, width=width_text_box)
    tracklength_locs_max_entry.grid(row=row_index, column=3)
    tracklength_locs_max_entry.insert(0, sim_input['tracklength_locs_max'])

    # Mean tracklength (frames)
    row_index += 1
    tk.Label(sim_frame, text="Mean tracklength (frames)", width=width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    mean_track_length_entry = tk.Entry(sim_frame, width=width_text_box)
    mean_track_length_entry.grid(row=row_index, column=1)
    mean_track_length_entry.insert(0, sim_input['mean_track_length'])

    # confined_diffusion
    row_index += 1
    confined_diffusion_var = tk.BooleanVar(value=sim_input['confined_diffusion'])
    tk.Checkbutton(sim_frame, text="Confine diffusion", variable=confined_diffusion_var, width=width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)

    # Localisation error (µm)
    row_index += 1
    tk.Label(sim_frame, text="Localisation error (µm)", width=width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    loc_error_entry = tk.Entry(sim_frame, width=width_text_box)
    loc_error_entry.grid(row=row_index, column=1)
    loc_error_entry.insert(0, sim_input['loc_error'])

    # orrect_diff_calc_loc_error'
    correct_diff_calc_loc_error_var = tk.BooleanVar(value=sim_input['correct_diff_calc_loc_error'])
    tk.Checkbutton(sim_frame, text="Correct_diff_calc_loc_error", variable=correct_diff_calc_loc_error_var, width=width_text_labels, anchor="w").grid(row=row_index, column=2, sticky=tk.W, columnspan=3)

    row_index += 1
    # Frametime (s)
    tk.Label(sim_frame, text="Frametime (s)", width=width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    frametime_entry = tk.Entry(sim_frame, width=width_text_box)
    frametime_entry.grid(row=row_index, column=1)
    frametime_entry.insert(0, sim_input['frametime'])

    # Oversampling (x)
    tk.Label(sim_frame, text="Oversampling factor", width=width_text_labels, anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    oversampling_entry = tk.Entry(sim_frame, width=width_text_box)
    oversampling_entry.grid(row=row_index, column=3)
    oversampling_entry.insert(0, sim_input['oversampling'])

    """
    # Currently empty...
    """

    # segmentation_frame = tk.LabelFrame(left_frame, text="Simulation parameters", padx=10, pady=10)
    # segmentation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")
   
                       
    """
    # Frame for plotting
    """
    plotting_frame = tk.LabelFrame(right_frame, text="Fitting and plotting options", padx=0, pady=0)
    plotting_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")  # Right half

    # Display figures
    row_index = 0
    display_figures_var = tk.BooleanVar(value=sim_input['display_figures'])
    tk.Checkbutton(plotting_frame, text="Display figures", variable=display_figures_var,
                    width = width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)

    # Whether to perform MC-DDA fitting
    row_index +=1
    perform_fitting_var = tk.BooleanVar(value=sim_input['perform_fitting'])
    tk.Checkbutton(plotting_frame, text="Perform MC-DDA fitting", variable=perform_fitting_var,
                    width = width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)
 
    # Species to select for fitting
    tk.Label(plotting_frame, text="Species to select", width = width_text_labels,
              anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    species_to_select_entry = tk.Entry(plotting_frame, width=width_text_box)
    species_to_select_entry.grid(row=row_index, column=3)
    species_to_select_entry.insert(0, sim_input['species_to_select'])  

    # plot_diff_hist_min
    row_index +=1
    tk.Label(plotting_frame, text="D. hist. min (µm^2/s)", width = width_text_labels,
              anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    diff_hist_min_entry = tk.Entry(plotting_frame, width=width_text_box)
    diff_hist_min_entry.grid(row=row_index, column=1)
    diff_hist_min_entry.insert(0, sim_input['plot_diff_hist_min'])  

    # plot_diff_hist_max
    tk.Label(plotting_frame, text="D. hist. max (µm^2/s)", width = width_text_labels,
              anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    diff_hist_max_entry = tk.Entry(plotting_frame, width=width_text_box)
    diff_hist_max_entry.grid(row=row_index, column=3)
    diff_hist_max_entry.insert(0, sim_input['plot_diff_hist_max'])  
    
    # Binwidth
    row_index +=1
    tk.Label(plotting_frame, text="Binwith histograms", width = width_text_labels,
              anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    binwidth_entry = tk.Entry(plotting_frame, width=width_text_box)
    binwidth_entry.grid(row=row_index, column=1)
    binwidth_entry.insert(0, sim_input['binwidth'])  

    # Dropdown Menu for plotting option selection
    tk.Label(plotting_frame, text="Plot option (log or lin)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    plot_option_var = tk.StringVar()
    plot_option_var.set(sim_input['plot_option'])  # Default option
    plot_option_entry = tk.OptionMenu(plotting_frame, plot_option_var, "linear", "logarithmic")
    plot_option_entry.grid(row=row_index, column=3, sticky=tk.W)

    # dpi
    row_index+=1
    tk.Label(plotting_frame, text="Resolution figus (dpi)", width = width_text_labels,
              anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    dpi_entry = tk.Entry(plotting_frame, width=width_text_box)
    dpi_entry.grid(row=row_index, column=1)
    dpi_entry.insert(0, sim_input['dpi']) 

    # Avoid float number = 0
    tk.Label(plotting_frame, text="Avoid float 0", width = width_text_labels,
              anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    avoidFloat0_entry = tk.Entry(plotting_frame, width=width_text_box)
    avoidFloat0_entry.grid(row=row_index, column=3)
    avoidFloat0_entry.insert(0, sim_input['avoidFloat0']) 

    # Create the SpeciesManager frame and add it to the right_frame, at the bottom
    species_frame = tk.LabelFrame(root, text="Define indiviudal species for the simulation", padx=10, pady=10)
    species_frame.grid(row=2, column=0, padx=10, pady=(0,10), columnspan=2, sticky="news")
    
    species_manager = SpeciesManager(species_frame, sim_input)
    species_manager.grid(row=2, column=0, padx=0, pady=0, columnspan=2)
    
#############################
    # Load, Save, and Exit buttons
#############################

    button_frame = tk.Frame(right_frame)
    button_frame.grid(row=1, column=1, padx = 10, pady=10)

    tk.Button(button_frame, text="Load...",
              command=load_params).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Save...",
              command=save_params).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Exit",
              command=exit_GUI).grid(row=0, column=4, padx=5)

    root.mainloop()
    
    # Return collected parameters after window closes
    return sim_input

class SpeciesManager(tk.Frame):
    def __init__(self, parent, sim_input):
        super().__init__(parent)
        self.sim_input = sim_input
        self.species_list = []
        
        # Define headers for the table
        headers = ["# of states\n per species\n 1:           A \n 2:       A,B \n 3:    A,B,C \n 4: A,B,C,D",
                   "# particles\n \n \n \n ",
                    "DiffQ (µm^2/s)\n separate by ',' \n 2 \n 0.01,2.8 \n 0,0.1,2 \n 0,0.1,1.1,2",
                    "Rates (s^-1)\n separate by ',' \n 0 \n 155, 137 \n AB,BA,BC,CB,AC,CA"
                    "\n AB,BA,BC,CB,CD,DC",
                    "Fitting: \n DiffQ guess \n struct.: see DiffQ \n \n \n",
                    "Fitting: \n Rates guess \n struct.: see rates \n \n \n",
                    "Fitting: \n DiffQ_lb_ub \n [diff_q_min]...\n [diff_q_max] \n 100, 100 \n ",
                    "Fitting: \n Rates_lb_ub \n [rates_min]...\n[rates_max] \n [10, 10], [200, 500] \n ", 
                    "Add\n row\n\n\n\n", "Delete \n row \n\n\n\n"]  

        for i, header in enumerate(headers):
            tk.Label(self, text=header).grid(row=0, column=i)

        for species in self.sim_input.get('species', []):
            self.add_row(species)

        self.add_row()

    def add_row(self, species=None):

        row_entries = {}
        num_states = tk.Entry(self, width=7)
        num_particles = tk.Entry(self, width=7)
        diff_quot = tk.Entry(self, width = 10)
        rates = tk.Entry(self, width = 16)
        diff_quot_init_guess = tk.Entry(self, width = 10)
        rates_init_guess = tk.Entry(self, width = 16)
        diff_quot_lb_ub = tk.Entry(self, width = 20)
        rates_lb_ub = tk.Entry(self, width = 20)

    # Custom function to format multi-dimensional numpy arrays with commas
        def format_numpy_array(arr):
            return ', '.join(['[' + ', '.join(map(str, sub_arr)) + ']' for sub_arr in arr])

        if species:
            num_states.insert(0, str(species.get('#_states', '')))
            num_particles.insert(0, str(species.get('#_particles', '')))
            diff_quot.insert(0, ', '.join(map(str, species.get('diff_quot', []))))
            rates.insert(0, ', '.join(map(str, species.get('rates', []))))
            diff_quot_init_guess.insert(0, ', '.join(map(str, species.get('diff_quot_init_guess', []))))
            rates_init_guess.insert(0, ', '.join(map(str, species.get('rates_init_guess', []))))
            diff_quot_lb_ub.insert(0, format_numpy_array(species.get('diff_quot_lb_ub')))
            rates_lb_ub.insert(0, format_numpy_array(species.get('rates_lb_ub')))

        row = len(self.species_list) + 1
        num_states.grid(row=row, column=0)
        num_particles.grid(row=row, column=1)
        diff_quot.grid(row=row, column=2)
        rates.grid(row=row, column=3)
        diff_quot_init_guess.grid(row=row, column=4)
        rates_init_guess.grid(row=row, column=5)
        diff_quot_lb_ub.grid(row=row, column=6)
        rates_lb_ub.grid(row=row, column=7)

        add_button = tk.Button(self, text="+", command=self.add_row)
        add_button.grid(row=row, column=8)

        delete_button = tk.Button(self, text="-", command=lambda r=row: self.delete_row(r))
        delete_button.grid(row=row, column=9)

        row_entries['#_states'] = num_states
        row_entries['#_particles'] = num_particles
        row_entries['diff_quot'] = diff_quot
        row_entries['rates'] = rates
        row_entries['diff_quot_init_guess'] = diff_quot_init_guess
        row_entries['rates_init_guess'] = rates_init_guess
        row_entries['diff_quot_lb_ub'] = diff_quot_lb_ub
        row_entries['rates_lb_ub'] = rates_lb_ub

        self.species_list.append(row_entries)

    def delete_row(self, row):
        if row - 1 < len(self.species_list):
            del self.species_list[row - 1]

        for widget in self.grid_slaves(row=row):
            widget.grid_forget()

        for i in range(row, len(self.species_list) + 1):
            for widget in self.grid_slaves(row=i):
                widget.grid(row=i - 1)

    def return_species_list(self):
        return self.species_list

    def load_species_data(self, species_data):
        for row in self.species_list:
            for key in row:
                row[key].delete(0, tk.END)

        self.species_list = []
        for species in species_data:
            self.add_row(species)




