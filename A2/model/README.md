# README : Simple Transport Model in Mesa

Created by: EPA1352 Group 07

| Name    | Student Number |
| Ferd van Bergeijk | 5198518 |
| Marvin Kleijweg | 4381955 | 
| Robin Lenskens | 4448170 |
| Rory Hooper | 5311446 |
| Sherman Lee | 4653777 | 


## Introduction

This is a 'simple' transport model simulation, as an assignment in the EPA1352 Advanced Simulation course. This program simulates 
the movement of homogeneous vehicles on a single road, impacted by delays caused by bridges in maintenance. 
There are several scenarios available for comparing the travel time of vehicles under different likelihood of bridge disruption.  

## How to Use

To run the simulation model, run the script 'model/model_run_batch.py'. 

Several model parameters can be varied in 'model_run_batch.py':
- num_steps : runtime per simulation in minutes (default:  5 days)
- scenario_first : lowest scenario number to be run in the batch simulation run (default: 0)
- scenario_last : highest scenario number to be run in the batch simulation run (default: 1, max 8)
- num_iterations : number of simulation iterations per scenario. This will generate some variance in output, as different bridges will fail per iteration. (default: 1 iteration)

Scenarios can be accessed at 'data/scenario_table.csv'. 

When the script is executed, there will be a status printout of iterations completed. The number of iterations run is n_iters * number of scenarios. Time taken to complete is dependent on run_length and is on the order of several minutes, so be patient and enjoy a cup of tea! :)

## Output

When completed, .csv files will be output as 'scenario<N>.csv' in the 'model' file, where <N> refers to the number of scenarios run.

Each row in the output .csv represents one truck that has reached the Sink node of a road during the simulation. Trucks that are still 'on the road' at the end of a simulation, are thus not recorded.

The format of the output .csv files is shown below. The last 3 columns are derived from the `array_of_removal` list in Markdown.

|**column name**| **variable meaning**                            |
|--------------|-----------------------------------------------------|
| scenario_num | Number of scenario (0 to 8)                         |
| Run          | iteration                                           |
| truck_id     | Unique ID of Vehicle agent that was removed at Sink |
| start_time   | Tick (minute) at which Vehicle agent was created    |
| end_time     | Tick (minute) at which Vehicle agent was deleted    |