import networkx as nx
import pandas as pd

aadt_path = '../data/aadt_N1N2.csv'
aadt_raw = pd.read_csv(aadt_path,index_col=0)
aadt_raw.drop(axis='columns',columns=['segment_name','LRP_start','Offset_start','Offset_end','LRP_end','length','Total AADT'],inplace=True)

# Average out the L and R sides
aadt_lr_sections = aadt_raw[(aadt_raw.road_segment.str[-1] == 'R') | (aadt_raw.road_segment.str[-1] == 'L')].copy(deep=False)
aadt_lr_sections.drop(columns=['road_segment','N1'],inplace=True)
aadt_l_idx = aadt_lr_sections[(aadt_raw.road_segment.str[-1] == 'L')].index
print("*** S: Don't worry about this warning, it still works ***")
aadt_lr_avg = (aadt_lr_sections.iloc[aadt_l_idx].reset_index() + aadt_lr_sections.iloc[aadt_l_idx + 1].reset_index()) / 2
aadt_lr_avg.set_index('index',inplace=True)
aadt_lr_avg.index = aadt_lr_avg.index.astype(int)
aadt_lr_avg = aadt_lr_avg.astype('uint16') # saving some space, ignoring averaging mistakes
aadt_lr_avg['road_segment'] = aadt_raw.iloc[aadt_l_idx,0].str[:-1]

aadt_avgd = aadt_raw.copy(deep=True)
aadt_avgd.update(aadt_lr_avg)
aadt_avgd.drop(index=(aadt_l_idx+1),inplace=True)
aadt_avgd.reset_index(drop=True,inplace=True)
end_col = aadt_avgd.columns.get_loc('Small Truck') # could put in Micro Bus, Utility, or Car

aadt_trucks = aadt_avgd.iloc[:,:end_col+1]
aadt_trucks['Mean'] = aadt_trucks.loc[:,'Heavy Truck':].mean(axis=1)
aadt_trucks.to_csv('../data/aadt_trucks_only.csv')



# putting in the bridge data into roads
# bridge_path = '../data/BMMS_overview_processed.xlsx'
# bridge_raw = pd.read_excel(bridge_path,usecols='A,B,D,G,R,S',engine='openpyxl')
# bridge_raw = bridge_raw[bridge_raw.road.isin(aadt_raw.N1.unique())]
# bridge_raw.drop_duplicates('LRPName',inplace=True)

# bridge_path = '../data/BMMS_truncated.csv'
# bridge_raw.to_csv(bridge_path)

# aadt_avg = aad
