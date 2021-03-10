# README : Simple Transport Model in Mesa

Created by: EPA1352 Group 07

| Name    | Student Number |
| Ferd van Bergeijk | 5198518 |
| Marvin Kleijweg | 4381955 | 
| Robin Lenskens | 4448170 |
| Rory Hooper | 5311446 |
| Sherman Lee | 4653777 | 


## Introduction

This is a 'simple' transport model simulation, as an assignment in the EPA1352 Advanced Simulation course. This program simulates the movement of homogeneous vehicles on a single road, impacted by delays caused by bridges in maintenance. There are several scenarios available for comparing the travel time of vehicles under different likelihood of bridge disruption.  

Every project should have a README file to help a first-time user understand what it is about and how they might be able to use it. This file is where you (as a group) shall provide the information needed by the TAs to evaluate and grade your work. 

If you are looking for information about the Demo model of Assignment 2, navigate to the [model/README.md](model/README.md) in the [model](model) directory. Have **fun** modeling in Python! 

## How to Use

To run the simulation model, run the script 'model/model_run_batch.py'. 

Several model parameters can be varied in 'model_run_batch.py':
- num_steps : runtime per simulation in minutes (default:  5 days)
- scenario_first : lowest scenario number to be run in the batch simulation run (default: 0)
- scenario_last : highest scenario number to be run in the batch simulation run (default: 1, max 8)
- num_iterations : number of simulation iterations per scenario. This will generate some variance in output, as different bridges will fail per iteration. (default: 1 iteration)

Scenarios can be accessed at 'data/scenario_table.csv'. Currently does not support running single scenarios.m 

When the script is executed, there will be a status printout of iterations completed. The number of iterations run is n_iters * number of scenarios. Time taken to complete is dependent on run_length and is on the order of several minutes, so be patient and enjoy a cup of tea! :)

When completed, a .csv file will be output as *****SPECIFY**** 'df_batch.csv'.

