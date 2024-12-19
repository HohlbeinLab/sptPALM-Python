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
import sys
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from analyse_movies_sptPALM import analyse_movies_sptPALM
from combine_analysed_data_sptPALM import combine_analysed_data_sptPALM
from plot_combined_data_sptPALM import plot_combined_data_sptPALM
from MC_diffusion_distribution_analysis_sptPALM import MC_diffusion_distribution_analysis_sptPALM
from set_parameters_sptPALM import set_parameters_sptPALM
from set_parameters_sptPALM_GUI import set_parameters_sptPALM_GUI


"""
    Not yet fully functional, more something for later!
"""


# Global variables
input_parameter = {}
data = {}
comb_data = {}

# Custom class to redirect stdout and stderr
class RedirectText:
    def __init__(self, text_widget):
        self.output_text = text_widget

    def write(self, string):
        self.output_text.insert(tk.END, string)
        self.output_text.see(tk.END)  # Auto-scroll to the end

    def flush(self):
        pass  # Required for file-like objects, no-op for now

# Function to clear the figure display area
def clear_plot_area():
    for widget in plot_frame.winfo_children():
        widget.destroy()

# Function to display figures in the plot area
def show_figure(fig):
    clear_plot_area()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Functions for different actions
def update_output(text):
    output_text.insert(tk.END, text + "\n")
    output_text.see(tk.END)

def exit_app():
    update_output("Exit!")
    root.quit()

def set_parameters():
    global input_parameter
    input_parameter = set_parameters_sptPALM()
    input_parameter = set_parameters_sptPALM_GUI(input_parameter)           
    update_output('  Show input_parameter:') # Display analysis parameters
    for key, value in input_parameter.items():
        update_output(f"    .{key}: {value}")
    # return input_parameter

def analyse_movies():
    global data, input_parameter
    # if input_parameter:
    #     update_output("Using existing 'input_parameter'.")
    #     data = analyse_movies_sptPALM(input_parameter)
    # else:
    #     update_output("No 'input_parameter' available, using default.")
    #     data = analyse_movies_sptPALM()
    # update_output("'data' now available in memory")
    [data, input_parameter] = analyse_movies_sptPALM(input_parameter)
    print("'data' now available in memory\n")
    # return data, input_parameter

def combine_data():
    global comb_data, input_parameter
    # if data:
    #     comb_data = combine_analysed_data_sptPALM(data)
    # else:
    #     update_output("No 'data' from option 2 available")
    #     comb_data = combine_analysed_data_sptPALM()
    # update_output("'comb_data' now available in memory")
    comb_data, input_parameter = combine_analysed_data_sptPALM(data, input_parameter)
    print("Combined data 'comb_data' now available in memory\n")

def plot_combined_data():
    global comb_data
    # if comb_data:
    #     # Run the plotting function that generates a figure
    #     fig = plot_combined_data_sptPALM(comb_data)
    #     if fig:
    #         show_figure(fig)  # Display the figure in the GUI
    # else:
    #     update_output("No combined data available, select a file from GUI.")
    #     comb_data = plot_combined_data_sptPALM()
    comb_data = plot_combined_data_sptPALM(comb_data, input_parameter)
    
    
def monte_carlo_dda():
    global comb_data
    condition_to_select = 0
    if comb_data:
        # Generate the figure from the Monte Carlo DDA function
        fig = MC_diffusion_distribution_analysis_sptPALM(condition_to_select, comb_data)
        if fig:
            show_figure(fig)  # Display the figure in the GUI
    else:
        update_output("No combined data available, select from GUI.")
        comb_data = MC_diffusion_distribution_analysis_sptPALM(condition_to_select)

def combine_thunderstorm_csv_files():
    update_output("Combining ThunderSTORM CSV files.")
    # Combine CSV functionality goes here

def auxiliary_functions():
    # Sub-menu for auxiliary functions
    def auxiliary_menu():
        sub_window = tk.Toplevel(root)
        sub_window.title("Auxiliary Functions")

        def sub_menu_exit():
            sub_window.destroy()

        def combine_csv():
            combine_thunderstorm_csv_files()
            update_output("Combine ThunderSTORM CSV files done")

        # Add buttons
        sub_btn1 = tk.Button(sub_window, text="Combine ThunderSTORM CSV files", command=combine_csv)
        sub_btn1.pack(fill=tk.X)

        sub_btn_exit = tk.Button(sub_window, text="Go back to main menu", command=sub_menu_exit)
        sub_btn_exit.pack(fill=tk.X)

    auxiliary_menu()

# Create the main application window
root = tk.Tk()
root.title("sptPALM Data Analysis GUI")

# Create frames
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create frames for output and plot area
output_frame = tk.Frame(right_frame)
output_frame.pack(side=tk.TOP, padx=10, pady=10)

plot_frame = tk.Frame(right_frame)
plot_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create buttons for each option
btn1 = tk.Button(left_frame, text="Set Parameters (GUI)", command=set_parameters)
btn1.pack(fill=tk.X)

btn2 = tk.Button(left_frame, text="Analyse Individual Movies", command=analyse_movies)
btn2.pack(fill=tk.X)

btn3 = tk.Button(left_frame, text="Combine Analysed Movies", command=combine_data)
btn3.pack(fill=tk.X)

btn4 = tk.Button(left_frame, text="Plot Combined Data", command=plot_combined_data)
btn4.pack(fill=tk.X)

btn5 = tk.Button(left_frame, text="Monte-Carlo DDA", command=monte_carlo_dda)
btn5.pack(fill=tk.X)

btn6 = tk.Button(left_frame, text="Auxiliary Functions", command=auxiliary_functions)
btn6.pack(fill=tk.X)

btn_exit = tk.Button(left_frame, text="Exit", command=exit_app)
btn_exit.pack(fill=tk.X)

# Output area (top of right frame)
output_text = tk.Text(output_frame, height=30, width=100)
output_text.pack()

# Redirect stdout and stderr to the Text widget
sys.stdout = RedirectText(output_text)
sys.stderr = RedirectText(output_text)

# Run the application
root.mainloop()


# def plot_combined_data_sptPALM(comb_data):
#     # Create your plot here
#     fig, ax = plt.subplots()
#     ax.plot([0, 1, 2], [10, 20, 5])  # Sample plot
#     return fig  # Return the figure instead of plt.show()
