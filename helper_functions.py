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

# import threading

import json
import pickle
import numpy as np


def _json_default(obj):
    """Fallback encoder so numpy types (which json can't handle) round-trip as
    native Python lists/numbers."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


# Keys that are derived from other parameters and recomputed on load, so we do
# not store them (avoids saving non-portable numpy arrays and stale values).
_DERIVED_PARAM_KEYS = ('tracklengths_steps', 'movie_number')


def save_parameters(para, filepath):
    """Save an analysis parameter dictionary to a human-readable JSON file.

    Derived keys (see _DERIVED_PARAM_KEYS) are dropped; they are recomputed by
    load_parameters(). JSON was chosen over pickle so parameter files are
    readable, diffable in git, and not tied to a Python/library version.
    """
    out = {k: v for k, v in para.items() if k not in _DERIVED_PARAM_KEYS}
    with open(filepath, 'w') as f:
        json.dump(out, f, indent=2, default=_json_default)


def load_parameters(filepath):
    """Load an analysis parameter dictionary.

    Accepts JSON (new format) and, for backward compatibility, legacy pickle
    (.pkl) files. Recomputes derived keys after loading.
    """
    if filepath.lower().endswith('.pkl'):
        with open(filepath, 'rb') as f:
            para = pickle.load(f)
    else:
        with open(filepath, 'r') as f:
            para = json.load(f)

    # Recompute derived fields from their source parameters.
    if 'tracklength_locs_min' in para and 'tracklength_locs_max' in para:
        para['tracklengths_steps'] = np.arange(para['tracklength_locs_min'] - 1,
                                               para['tracklength_locs_max'])
    return para


def yes_no_input(prompt, default="yes"):
    # Define default options based on the default value
    if default == "yes":
        prompt += " [Y/n]: "
        default_choice = "yes"
    elif default == "no":
        prompt += " [y/N]: "
        default_choice = "no"
    else:
        raise ValueError("Invalid default answer: choose 'yes' or 'no'")

    # Get user input
    choice = input(prompt).strip().lower()

    # Return the default choice if no input is provided
    if choice == '':
        return default_choice == "yes"
    
    # Evaluate the input
    if choice in ['y', 'yes']:
        return True
    elif choice in ['n', 'no']:
        return False
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        return yes_no_input(prompt, default)


def string_input_with_default(prompt, default):
    # Update prompt with the default string
    prompt_with_default = f"{prompt} (default: {default}): "
    
    # Get user input and default to `default` if no input is provided
    user_input = input(prompt_with_default).strip()
    
    # If the user presses Enter without typing, use the default value
    if not user_input:
        return default
    
    return user_input

#Version if the default should already show in the commandline

# import readline  # on Unix-based systems (Linux/macOS)
# # import pyreadline3 as readline  # Uncomment this on Windows if using pyreadline3

# def string_input_with_default(prompt, default):
#     # Set up the default value for quick editing
#     readline.set_startup_hook(lambda: readline.insert_text(default))
#     try:
#         # Show prompt with the default value pre-filled
#         return input(f"{prompt}: ") or default
#     finally:
#         readline.set_startup_hook()  # Clear the hook after use

# # Example usage
# input_parameter = {'fn_movies': 'default_movie_filename.mat'}
# fn_output_default = input_parameter['fn_movies']
# input_parameter['fn_movies'] = string_input_with_default("Enter string or press enter", fn_output_default)

# print(f"Final value for 'fn_movies': {input_parameter['fn_movies']}")