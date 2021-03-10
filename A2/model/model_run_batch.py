from model import BangladeshModel
from mesa.batchrunner import BatchRunner
import pandas as pd

"""
    Run simulations for multiple scenarios & iterations
    Save output as separate .csv files per scenario
"""
## -------------------------------------------------------------
## Input parameters
scenario_first = 0  # Lowest scenario number to run in batch
scenario_last = 1   # Highest scenario number to run in batch
num_iterations =  1  # Number of iterations per scenario
num_steps = 5*24*60   # Number of steps for each scenario, 1 tick = 1 minute

# Specify (scenario) parameters that are changed per batch
# Dictionary - keys: name of parameters to change.  - values: range of parameters values to run
dic_parameters = {"scenario_num": range(scenario_first,scenario_last+1)}
# Specify agent parameters that will be reported on:
# Dictionary - keys: name of parameters to report on.  - values: name in model of parameters to report on
dic_agent_reporters = {"Arrays_of_removal": "array_of_removal"}


## --------------------------------------------------------------
## Run the model

# Batch run the model, for the specified scenarios and number of iterations.
batch_run = BatchRunner(BangladeshModel, variable_parameters=dic_parameters,
                        display_progress=True, iterations=num_iterations, max_steps=num_steps,
                        agent_reporters=dic_agent_reporters)
# 'agent_reporters' gives the agent variables that are reported on
# 'model_reporters' could be added to report on model variables

batch_run.run_all()  # Run all simulations
df_batch = batch_run.get_agent_vars_dataframe()  # Get agent variables from all simulations in a dataframe

## --------------------------------------------------------------
## Post-processing of recorded data
# Only keep rows that contain relevant agent data for Sink
df_sinks = df_batch[[bool(x) for x in df_batch['Arrays_of_removal']]] # Select cells with non-empty lists
print(df_sinks.head())

#Convert lists in cells into multiple cells
df_sinks = df_sinks.explode('Arrays_of_removal')  # New row for every vehicle
df_sinks = df_sinks.reset_index()   # Reset index for join function
# Split array into 3 columns
df_sinks_list_as_columns = pd.DataFrame(df_sinks.Arrays_of_removal.to_list(), columns=['truck_id','start_time','end_time'])
# Join dataframes into 1 output dataframe and remove useless columns
df_sinks_output = df_sinks.join(df_sinks_list_as_columns)
df_sinks_output.drop(columns=['index','AgentId','Arrays_of_removal'],inplace=True)

## --------------------------------------------------------------
## Output data of each scenario to a separate .csv file
for i in range(scenario_first, scenario_last+1):   # Loop over all scenario numbers
    df_sinks_output[df_sinks_output["scenario_num"]==i].to_csv("scenario"+str(i)+".csv", index=False)

