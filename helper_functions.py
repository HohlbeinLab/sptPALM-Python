#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

# import threading

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