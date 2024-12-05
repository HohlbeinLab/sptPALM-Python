#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:01:21 2024

@author: hohlbein
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Example MSD data (replace with your actual data)
tau = np.array([0.1, 0.2, 0.3, 0.4, 0.5])  # lag times
msd = np.array([0.15, 0.28, 0.42, 0.56, 0.70])  # MSD values

# Define the MSD equation
def msd_function(tau, D, sigma_sq):
    return 4 * D * tau + 4*sigma_sq**2

# Fit the MSD data to the equation
popt, pcov = curve_fit(msd_function, tau, msd)

# Extract the diffusion coefficient and localization variance
D_fit, sigma_sq_fit = popt

print(f"Fitted diffusion coefficient (D): {D_fit:.3f}")
print(f"Fitted localization variance (σ^2): {sigma_sq_fit:.3f}")

# Plot the data and the fit
plt.figure()
plt.scatter(tau, msd, label="Data", color="blue")
plt.plot(tau, msd_function(tau, *popt), label="Fit", color="red")
plt.xlabel("Lag time (τ)")
plt.ylabel("MSD (τ)")
plt.legend()
plt.title("MSD Fit")
plt.show()
