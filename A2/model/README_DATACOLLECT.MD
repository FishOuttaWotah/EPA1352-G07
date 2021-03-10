# README FOR DATA COLLECTION & OUTPUT FOR MESA MODEL

AUTHOR : SHERMAN

## How to use

* ensure that the model_run.py and Plotta.py scripts are in the 'model' directory 
* run the model simulation in model_run.py (by default it's set for Scenario 8)
* RETRIEVAL: after model completion, the pandas dataframe can be retrieved by 'sim_model.datacollected', also in model_run.py. Example is available in the model_run.py version dated 1st March 2021 
* sim_model.datacollected contains two columns for now, the start time and end time of the trucks. Cleaning of this dataframe is done by the Plotta.py script.

## Operating mechanism: datacollection alternative

The datacollection method operates between the model.py script and components.py script. The former is for the model-level definition, latter is for agent-level.

(Model-level: model.py script)
Under the BangladeshModel class, the function 'adhoc_datacollector()' is called during __init__. This creates an empty pandas DataFrame with the required columns (and their names), which the agent-level processes will fill in. The reason this is here is so the user can retrieve the object on the model level (instead of going into schedule/agent level). 

IMPORTANT: Additionally, this can be called as a model-level reporter for Mesa batchrunner (I think), but again, Mesa documentation is a bit lacking.

(Agent-level: components.py script)
Under the Vehicle class, line 234 (as of the 1st Mar version) in the __init__ section, is the 1st part. It checks whether the Pandas dataframe is created, accesses the dataframe in the model level, and then creates an entry when a truck is created (id = index). This section encodes ONLY the creation time and a placeholder for None for the end time (it is assumed to be overwritten)

Under the Vehicle class, line 316 (1st Mar ver.) in the drive_to_next method, is the 2nd part. It accesses the dataframe in the model level again, and adds the end time (using the id as index). This encodes ONLY end time, if the trucks do not reach the Sink after end of run, they will have None for end time.

## Operating mechanism: post-simulation data cleaning

The post-simulation data cleaning is in the Plotta.py file, where it takes the pickle saved from model_run.py (so I can test stuff without having to run the entire model). The script creates a new column for travel time (the one we're interested in), deletes unfinished journeys, and then plots it in a simple Seaborn scatterplot (for now). 

The scatterplot from this has the IDs on the x axis, and the travel time on the y axis.