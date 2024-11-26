#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:01:21 2024

@author: hohlbein
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
https://matplotlib.org/stable/gallery/color/named_colors.html
To make a gif: import files in Fiji -> stack -> export as animated gif
https://cloudconvert.com/about
"""

# Load the Excel data
file_path = 'DyeSpectra.xlsx'

# Assuming each spectrum is on a separate sheet
No1 = pd.read_excel(file_path, sheet_name='Cy3B_Ab').to_numpy()
No2 = pd.read_excel(file_path, sheet_name='Cy3B_Em').to_numpy()
No3 = pd.read_excel(file_path, sheet_name='ATTO647N_Ab').to_numpy()
No4 = pd.read_excel(file_path, sheet_name='ATTO647N_Em').to_numpy()

Laser_1 = 561
Laser_2 = 640

# Define wavelength range
WavelengthMin = 400
WavelengthMax = 750

# Create the figure
font_size = 16
font_name = 'Arial'
LineWidth = 2

fig1 = plt.figure(figsize=(8, 6), dpi=200)
fig1.patch.set_facecolor('w')
# fig1.suptitle('Spectra', fontsize=font_size, fontname=font_name)

# Customizing axes
ax1 = plt.gca()
ax1.tick_params(direction='out', length=3*LineWidth, width=LineWidth)

ax1.set_yticks(np.arange(0, 1.1, 0.2))
ax1.set_yticklabels(['0', '0.2', '0.4', '0.6', '0.8', '1'], fontname=font_name, fontsize=font_size)
ax1.set_xticks(np.arange(WavelengthMin, WavelengthMax + 1, 50))
ax1.tick_params(axis='x', labelsize=font_size)
ax1.tick_params(axis='y', labelsize=font_size,direction='out')

ax1.spines['top'].set_linewidth(LineWidth)
ax1.spines['right'].set_linewidth(LineWidth)
ax1.spines['left'].set_linewidth(LineWidth)
ax1.spines['bottom'].set_linewidth(LineWidth)

# Normalize and fill data, add overlay
plt.fill_between(No1[:, 0], No1[:, 1] / np.max(No1[:, 1]), color='gold', alpha=0.5, label="Cy3B (ab)")
# plt.plot(No1[:, 0], No1[:, 1] / np.max(No1[:, 1]), linewidth=LineWidth, color='gold', linestyle='-')

# plt.fill_between(No2[:, 0], No2[:, 1] / np.max(No2[:, 1]), color='darkorange', alpha=0.5, label="Cy3B (em)")
# plt.plot(No2[:, 0], No2[:, 1] / np.max(No2[:, 1]), linewidth=LineWidth, color='darkorange')

# plt.fill_between(No3[:, 0], No3[:, 1] / np.max(No3[:, 1]), color='orangered', alpha=0.5, label="ATTO647N (ab)")
# plt.plot(No3[:, 0], No3[:, 1] / np.max(No3[:, 1]), linewidth=LineWidth, color='orangered', linestyle='-')

# plt.fill_between(No4[:, 0], No4[:, 1] / np.max(No4[:, 1]), color='darkred', alpha=0.5, label="ATTO647N (em)")
# plt.plot(No4[:, 0], No4[:, 1] / np.max(No4[:, 1]), linewidth=LineWidth, color='darkred')

# Add vertical lines
# plt.axvline(x=Laser_1, color='green', linestyle='--', linewidth=LineWidth, label=f"Laser {Laser_1} nm")

# plt.axvline(x=Laser_2, color='red', linestyle='--', linewidth=LineWidth, label=f"Laser {Laser_2} nm")

# Set axis labels and limits
plt.xlabel('Wavelength (nm)', fontsize=font_size, fontname=font_name)
plt.ylabel('Absorption / Emission (a.u.)', fontsize=font_size, fontname=font_name)
plt.xlim([WavelengthMin, WavelengthMax])
plt.ylim([0, 1])

# Add box
plt.grid(False)
plt.box(True)

# Adjust layout and display
plt.legend(fontsize=font_size-2, loc='upper left')
plt.tight_layout()
plt.show()
