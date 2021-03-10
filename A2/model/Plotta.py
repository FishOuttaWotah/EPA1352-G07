from model_run import load_from_pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = load_from_pickle('../data/sim_output.df')
# df = load_from_pickle('sim_output.df')
# df = sim_model.datacollected.copy()
df['travel_time'] = df.end_time - df.start_time
print(df)
df.dropna(inplace=True)
sns.scatterplot(x=df.index,y='travel_time',data=df)
plt.show()
