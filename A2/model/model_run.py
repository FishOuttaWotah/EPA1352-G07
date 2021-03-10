from model import BangladeshModel
import seaborn as sns
import pickle
import pandas as pd
from mesa.batchrunner import BatchRunner, FixedBatchRunner

"""
    Run simulation
    Print output at terminal
"""
# ---------------------------------------------------------------
# Pickle operations:
# TODO: explain pickle method in documentation
def save_to_pickle(object, pickleName):
    with open(pickleName,'wb') as toPickle:
        pickle.dump(object, toPickle)
    print(f'Saved as pickle: {pickleName}' )

# ----------------------------------------------------------------
# Pickle loading function: MAKE SURE YOU CAN TRUST THE PICKLE FILE!
def load_from_pickle(pickleName):
    with open(pickleName,'rb') as toUnpickle:
        f = pickle.load(toUnpickle)
    print(f'Loaded pickle: {pickleName}')
    return f

# ---------------------------------------------------------------
def model_multi_run(n_runs=2, seed=1234567, run_days=2, multi_scenario=True, scenario=8):
    """
    Runs the sim for N times, recording the sim's datacollected obj
    :return:
    """

    def something():

        pass
    # data_big = pd.DataFrame(columns=['start_time', 'end_time', 'travel_time',
    #                                  'scenario', 'sim_run'])
    run_length = run_days * 24 * 60
    if multi_scenario:
        br_item = BatchRunner(BangladeshModel,variable_parameters={'scenario':range(1,9,1)},
                    iterations=n_runs, max_steps=run_length,
                    model_reporters={'datacollected':lambda m : m.datacollected})
    elif not multi_scenario and (1<= scenario <=8):
        br_item = FixedBatchRunner(BangladeshModel,fixed_parameters={'scenario':scenario},
                    iterations=n_runs, max_steps=run_length,
                    model_reporters={'datacollected':lambda m : m.datacollected})
    else:
        raise ValueError("Scenario value should be within 1-8, or multi_scenario should be a bool")
    br_item.run_all()
    output_verbose = br_item.get_model_vars_dataframe()
    # extract datacollection column, create column about
    return output_verbose

# ---------------------------------------------------------------

if __name__ == "__main__":
    # run time 5 x 24 hours; 1 tick 1 minute
    run_length = 2 * 24 * 60

    # run time 1000 ticks
    # run_length = 1000

    seed = 1234567

    # sim_model = BangladeshModel(seed=seed)
        # Check if the seed is set
    # print("SEED " + str(sim_model._seed))
    #
    # # One run with given steps
    # for i in range(run_length):
    #     sim_model.step()
    #     if i % int(24 * 30) == 0:
    #         print(f"\t *** DAY {i/24/60 +1} COMPLETE ***")

    big_boi = model_multi_run()
    save_to_pickle(big_boi, "../data/sim_output.df")

    # print(sim_model.datacollected) # retrieve datacollected


# probably batchrunner can collect the model-level datacollected item?
# some form of collection, formatting and outputting in seaborn is needed (dependent on batchrun tho)