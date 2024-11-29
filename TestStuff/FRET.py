#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:01:21 2024

@author: hohlbein
"""
import numpy as np
import matplotlib.pyplot as plt

# Define the Foerster radii
Foerster_radii = [4, 6, 8]  # in nm

# Distance range from 0 to 14 nm
distance = np.linspace(0, 14, 1000)

# Function to calculate FRET efficiency
def fret_efficiency(R, R0):
    return 100 / (1 + (R / R0) ** 6)

# Set up the plot
plt.figure(figsize=(8, 5))
plt.rc('font', family='Arial', size=14)
plt.rc('axes', linewidth=2)
plt.rc('xtick.major', width=2, size=6)
plt.rc('ytick.major', width=2, size=6)

# Plot the FRET efficiencies
for R0 in Foerster_radii:
    fret = fret_efficiency(distance, R0)
    plt.plot(distance, fret, label=f'{R0} nm', linewidth=2, color='black')

# Add horizontal dashed lines
plt.axhline(10, color='red', linestyle='--', linewidth=2)
plt.axhline(90, color='red', linestyle='--', linewidth=2)
plt.axhline(50, color='green', linestyle='--', linewidth=2)

# Add labels for the lines
for R0 in Foerster_radii:
    x_label = R0 +1.1    # x-value for the label
    y_label = 50  # y-value at 50% FRET efficiency
    plt.text(x_label, y_label - 6, f'$R_0$ {R0} nm', fontsize=14, color='black', ha='center')

# Set axis limits and labels
plt.xlim(0, 14)
plt.ylim(0, 100)
plt.xlabel('Donor - Acceptor distance (nm)')
plt.ylabel('FRET efficiency (%)')

# Remove legend
plt.legend().remove()

# Show the plot
plt.tight_layout()
plt.show()
