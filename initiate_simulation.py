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
    
import numpy as np
import pandas as pd

def initiate_simulation(sim_input):
    print('\nRun initiate_simulation.py')
    # Calculate some parameters from the input
    sim_input['total_number_particles'] = 0
    for ii in range(sim_input['#_species']):
        sim_input['total_number_particles'] +=  sim_input['species'][ii]['#_particles']
    
    print(f"  We simulate a total of {sim_input['total_number_particles']} particles")
    sim_input['#_species'] = len(sim_input['species'])
    
    sim_input['total_length_cell'] = float(2 * sim_input['radius_cell'] + sim_input['length_cell'])
    sim_input['total_duration_simulation'] = float(max(sim_input['tracklengths_steps']) * sim_input['frametime'] )
    sim_input['steptime'] = sim_input['frametime']/sim_input['oversampling']
    sim_input['steps_simulation'] = int(sim_input['total_duration_simulation'] / sim_input['steptime'])
    
    print(f"  We simulate a total of {int(sim_input['steps_simulation'])} steps")

    # Simulate starting positions and prepare particle_data DataFrame
    particle_data = pd.DataFrame(np.zeros((sim_input['total_number_particles'], 12)), 
                                columns=['particle', 'species', 'xPos', 'yPos', 'zPos', 'pos_reject', 'active_state',
                                         'active_diff_quot', 'next_state', 'state_time_remaining', 'track_length', 'track_length_remaining'])
    float_strings = ['xPos', 'yPos', 'zPos','active_diff_quot','state_time_remaining']
    particle_data[float_strings] = particle_data[float_strings].astype(float)

    particle_data['particle'] = np.arange(0, sim_input['total_number_particles'])
    particle_data['pos_reject'] = True  # Initially, all positions are invalid

    temp_counter = 0

    for ii in range(sim_input['#_species']):
        start_idx = temp_counter
        end_idx = temp_counter + sim_input['species'][ii]['#_particles']
        particle_data.loc[start_idx:end_idx, 'species'] = ii
        temp_counter = end_idx

        # Avoid any rates being zero to avoid issues with probabilities
        sim_input['species'][ii]['rates'] = np.maximum(sim_input['species'][ii]['rates'], sim_input['avoidFloat0'])

    sum_pos_reject = particle_data['pos_reject'].sum()

    # Assign random positions and reject those outside cell boundaries
    while sum_pos_reject > 0:
        # Random X, Y, Z positions
        particle_data.loc[particle_data['pos_reject'], 'xPos'] = sim_input['total_length_cell'] * np.random.rand(sum_pos_reject)
        particle_data.loc[particle_data['pos_reject'], 'yPos'] = 2 * sim_input['radius_cell'] * (np.random.rand(sum_pos_reject) - 0.5)
        particle_data.loc[particle_data['pos_reject'], 'zPos'] = 2 * sim_input['radius_cell'] * (np.random.rand(sum_pos_reject) - 0.5)
        
        radius_y_z_squared_temp = particle_data['yPos'] ** 2 + particle_data['zPos'] ** 2
        
        # Check boundaries
        reject_pos_left_part = (particle_data['xPos'] < sim_input['radius_cell']) & \
                            ((particle_data['xPos'] - sim_input['radius_cell']) ** 2 + radius_y_z_squared_temp > sim_input['radius_cell'] ** 2)
        reject_pos_cylinder_part = radius_y_z_squared_temp > sim_input['radius_cell'] ** 2
        reject_pos_right_part = (particle_data['xPos'] > (sim_input['length_cell'] + sim_input['radius_cell'])) & \
                             ((particle_data['xPos'] - (sim_input['length_cell'] + sim_input['radius_cell'])) ** 2 + radius_y_z_squared_temp > sim_input['radius_cell'] ** 2)
        
        particle_data['pos_reject'] = reject_pos_left_part | reject_pos_cylinder_part | reject_pos_right_part
        sum_pos_reject = particle_data['pos_reject'].sum()

    if sim_input['display_figures']:
        import matplotlib.pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(particle_data['xPos'], particle_data['yPos'], particle_data['zPos'])
        plt.show()

    # Define states for each species
    for ii in range(sim_input['#_species']):
        print(f"  Species: {ii + 1}")
        loc_species = particle_data.index[particle_data['species'] == ii].tolist()
        diff_quot = sim_input['species'][ii]['diff_quot']

        for idx, dq in enumerate(diff_quot):
            print(f"    State {idx}:")
            print(f"      stepsize per frame (µm): {round(np.sqrt(2 * dq * sim_input['frametime']),2)}")
            print(f"      stepsize per step (µm): {round(np.sqrt(2 * dq * sim_input['frametime']/sim_input['oversampling']),2)}")
        
        numberStates = sim_input['species'][ii]['#_states']
        if numberStates == 1:
            handle_one_state_init(sim_input, particle_data, loc_species)

        elif numberStates == 2:
            handle_two_states_init(ii, sim_input, particle_data, loc_species)

        # Similar approach for 3 or more states...
        elif numberStates == 3:
            handle_three_states_init(ii, sim_input, particle_data, loc_species)
 
        elif numberStates == 4:
            handle_four_states_init(ii, sim_input, particle_data, loc_species)

        # Assign active diffusion quotient for each particle
        # Convert 'active_state' to a numpy array
        active_states = particle_data.loc[loc_species, 'active_state'].astype(int).to_numpy() 
        
        # Use the active_states array to index into the diff_quot list
        particle_data.loc[loc_species, 'active_diff_quot'] = np.array(sim_input['species'][ii]['diff_quot'])[active_states]

    # Set track lengths using an exponential distribution and round
    particle_data['track_length'] = np.ceil(np.random.exponential(sim_input['mean_track_length'], sim_input['total_number_particles']))
    particle_data['track_length_remaining'] = particle_data['track_length']

    return particle_data, sim_input


def handle_one_state_init(sim_input, particle_data, loc_species):
    particle_data.loc[loc_species, 'active_state'] = 0
    particle_data.loc[loc_species, ['state_time_remaining', 'next_state']] = np.nan
    return particle_data

def handle_two_states_init(ii, sim_input, particle_data, loc_species):
    kAB, kBA = sim_input['species'][ii]['rates']
    probA = kBA / (kBA + kAB)
    probB = kAB / (kBA + kAB)
    print(f"    kAB (1/s): {round(kAB,2)}")
    print(f"    kBA (1/s): {round(kBA,2)}")
    print(f"    probA: {round(probA,2)}, probB: {round(probB,2)}")
    print(f"    probA + probB = {round(probA + probB,2)}")
    tempRand = np.random.rand(sim_input['total_number_particles'], 2)

    tempStateA = np.array(loc_species)[tempRand[loc_species, 0] <= probA]
    particle_data.loc[tempStateA, 'active_state'] = 0
    particle_data.loc[tempStateA, 'next_state'] = 1
    particle_data.loc[tempStateA, 'state_time_remaining'] = np.log(tempRand[tempStateA, 1]) / (-kAB)

    tempStateB = np.array(loc_species)[tempRand[loc_species, 0] > probA]
    particle_data.loc[tempStateB, 'active_state'] = 1
    particle_data.loc[tempStateB, 'next_state'] = 0
    particle_data.loc[tempStateB, 'state_time_remaining'] = np.log(tempRand[tempStateB, 1]) / (-kBA)
    return particle_data
           
def handle_three_states_init(ii, sim_input, particle_data, loc_species):           
    kAB, kBA, kBC, kCB, kAC, kCA = sim_input['species'][ii]['rates']
    
    # Normalization factor (calculated using symbolic tools like Mathematica)
    temp = ((kBA + kBC) * (kAC + kCA) + (kAC + kBA) * kCB + kAB * (kBC + kCA + kCB))

    probA = (kBC * kCA + kBA * (kCA + kCB)) / temp
    probB = (kAC * kCB + kAB * (kCA + kCB)) / temp
    probC = (kAB * kBC + kAC * (kBA + kBC)) / temp
    
    print(f"    kAB (1/s): {round(kAB,2)}, kAC (1/s): {round(kAC,2)}")
    print(f"    kBA (1/s): {round(kBA,2)}, kBC (1/s): {round(kBC,2)}")
    print(f"    kCA (1/s): {round(kCA,2)}, kCB (1/s): {round(kCB,2)}")
    print(f"    probA: {round(probA,2)}, probB: {round(probB,2)}, probC: {round(probC,2)}")
    print(f"    probA + probB + probC = {round(probA + probB + probC,2)}")
    
    tempRand = np.random.rand(sim_input['total_number_particles'], 3)

    # State A
    tempStateA = np.array(loc_species)[tempRand[loc_species, 0] <= probA]
    particle_data.loc[tempStateA, 'active_state'] = 0
    tempSwitchAB = tempStateA[kAB / (kAB + kAC) >= tempRand[tempStateA, 1]]
    tempSwitchAC = tempStateA[kAB / (kAB + kAC) < tempRand[tempStateA, 1]]

    particle_data.loc[tempSwitchAB, 'next_state'] = 1
    particle_data.loc[tempSwitchAB, 'state_time_remaining'] = np.log(tempRand[tempSwitchAB, 2]) / (-kAB)
    particle_data.loc[tempSwitchAC, 'next_state'] = 2
    particle_data.loc[tempSwitchAC, 'state_time_remaining'] = np.log(tempRand[tempSwitchAC, 2]) / (-kAC)

    # State B
    tempStateB = np.array(loc_species)[(probA < tempRand[loc_species, 0]) & (tempRand[loc_species, 0] <= probA + probB)]
    particle_data.loc[tempStateB, 'active_state'] = 1
    tempSwitchBA = tempStateB[kBA / (kBA + kBC) >= tempRand[tempStateB, 1]]
    tempSwitchBC = tempStateB[kBA / (kBA + kBC) < tempRand[tempStateB, 1]]

    particle_data.loc[tempSwitchBA, 'next_state'] = 0
    particle_data.loc[tempSwitchBA, 'state_time_remaining'] = np.log(tempRand[tempSwitchBA, 2]) / (-kBA)
    particle_data.loc[tempSwitchBC, 'next_state'] = 2
    particle_data.loc[tempSwitchBC, 'state_time_remaining'] = np.log(tempRand[tempSwitchBC, 2]) / (-kBC)

    # State C
    tempStateC = np.array(loc_species)[tempRand[loc_species, 0] > probA + probB]
    particle_data.loc[tempStateC, 'active_state'] = 2
    tempSwitchCA = tempStateC[kCA / (kCA + kCB) >= tempRand[tempStateC, 1]]
    tempSwitchCB = tempStateC[kCA / (kCA + kCB) < tempRand[tempStateC, 1]]

    particle_data.loc[tempSwitchCA, 'next_state'] = 0
    particle_data.loc[tempSwitchCA, 'state_time_remaining'] = np.log(tempRand[tempSwitchCA, 2]) / (-kCA)
    particle_data.loc[tempSwitchCB, 'next_state'] = 1
    particle_data.loc[tempSwitchCB, 'state_time_remaining'] = np.log(tempRand[tempSwitchCB, 2]) / (-kCB)
    return particle_data

def handle_four_states_init(ii, sim_input, particle_data, loc_species): 
    kAB, kBA, kBC, kCB, kCD, kDC = sim_input['species'][ii]['rates']

    # Normalization factor
    temp = (kAB * kBC * kCD) + kBA * kCB * kDC + kAB * (kBC + kCB) * kDC

    probA = (kBA * kCB * kDC) / temp
    probB = (kAB * kCB * kDC) / temp
    probC = (kAB * kBC * kDC) / temp
    probD = (kAB * kBC * kCD) / temp
    
    print(f"    kAB (1/s): {round(kAB,2)}")
    print(f"    kBA (1/s): {round(kBA,2)}, kBC (1/s): {round(kBC,2)}")
    print(f"    kCB (1/s): {round(kCB,2)}, kCD (1/s): {round(kCD,2)}")
    print(f"    kDC (1/s): {round(kDC,2)}")
    print(f"    probA: {round(probA,2)}, probB: {round(probB,2)}, probC: {round(probC,2)}, probD: {round(probD,2)}")
    print(f"    probA + probB + probC + probD = {round(probA + probB + probC + probD,2)}")

    tempRand = np.random.rand(sim_input['totalNumberParticles'], 3)

    # State A
    tempStateA = np.array(loc_species)[tempRand[loc_species, 0] <= probA]
    particle_data.loc[tempStateA, 'active_state'] = 0
    particle_data.loc[tempStateA, 'next_state'] = 1
    particle_data.loc[tempStateA, 'state_time_remaining'] = np.log(tempRand[tempStateA, 2]) / (-kAB)

    # State B
    tempStateB = np.array(loc_species)[(probA < tempRand[loc_species, 0]) & (tempRand[loc_species, 0] <= probA + probB)]
    particle_data.loc[tempStateB, 'active_state'] = 1
    tempSwitchBA = tempStateB[kBA / (kBA + kBC) >= tempRand[tempStateB, 1]]
    tempSwitchBC = tempStateB[kBA / (kBA + kBC) < tempRand[tempStateB, 1]]

    particle_data.loc[tempSwitchBA, 'next_state'] = 0
    particle_data.loc[tempSwitchBA, 'state_time_remaining'] = np.log(tempRand[tempSwitchBA, 2]) / (-kBA)
    particle_data.loc[tempSwitchBC, 'next_state'] = 2
    particle_data.loc[tempSwitchBC, 'state_time_remaining'] = np.log(tempRand[tempSwitchBC, 2]) / (-kBC)

    # State C
    tempStateC = np.array(loc_species)[(probA + probB < tempRand[loc_species, 0]) & (tempRand[loc_species, 0] <= probA + probB + probC)]
    particle_data.loc[tempStateC, 'active_state'] = 2
    tempSwitchCB = tempStateC[kCB / (kCB + kCD) >= tempRand[tempStateC, 1]]
    tempSwitchCD = tempStateC[kCB / (kCB + kCD) < tempRand[tempStateC, 1]]

    particle_data.loc[tempSwitchCB, 'next_state'] = 1
    particle_data.loc[tempSwitchCB, 'state_time_remaining'] = np.log(tempRand[tempSwitchCB, 2]) / (-kCB)
    particle_data.loc[tempSwitchCD, 'next_state'] = 3
    particle_data.loc[tempSwitchCD, 'state_time_remaining'] = np.log(tempRand[tempSwitchCD, 2]) / (-kCD)

    # State D
    tempStateD = np.array(loc_species)[tempRand[loc_species, 0] > probA + probB + probC]
    particle_data.loc[tempStateD, 'active_state'] = 3
    particle_data.loc[tempStateD, 'next_state'] = 2
    particle_data.loc[tempStateD, 'state_time_remaining'] = np.log(tempRand[tempStateD, 2]) / (-kDC)
    return particle_data