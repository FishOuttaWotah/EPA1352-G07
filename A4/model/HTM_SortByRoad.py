import pandas as pd
import shutil
from os import listdir
from os.path import isfile, join, abspath

# get htm to save per road
class TrafficDensity:
    def __init__(sf, road_csv_path=None, htm_source_path=None, htm_save_path=None):
        if road_csv_path == None:
            sf.htm_in_roads = "../data/df_road_N1andN2.csv"
        if htm_source_path == None:
            sf.htm_directory = "D:\Downloads\@Books\@TPM\@AS_1352\A1\RMMS traffic"  # only works for Sherman
        if htm_save_path == None:
            sf.save_directory = '../data/HTMs'  # relative path for Git usage
            
        csv_read = pd.read_csv(sf.htm_in_roads, header=0, index_col=0)
        sf.roads = csv_read.road.unique()   # list of roads, returned as numpy ndarray
        
    def copy_HTM_to_directory(sf):
        # match for items in folder, all HTM items
        htm_lists = [f for f in listdir(sf.htm_directory) if f.split('.')[0] in sf.roads]
        for htm_file in htm_lists:
            full_file_name = join(sf.htm_directory, htm_file)
            if isfile(full_file_name) and not isfile(abspath(join(sf.save_directory, htm_file))):
                shutil.copy(full_file_name, abspath(sf.save_directory))
            else:
                print(f'{htm_file} exists in HTM folder')

    
    def get_aadt_raw(sf):
        sf.aadt_raw = pd.DataFrame()
        colnames = None
        for epoch, htm_file in enumerate(listdir(sf.save_directory)):
            roadname = htm_file.split('.')[0]  # split N1.traffic.htm by '.' character, take first one (aka N1)
            raw = pd.read_html(join(sf.save_directory, htm_file))[-1]
            raw.insert(1, 'road', roadname)
            if epoch == 0:  # only do this once, at first iteration
                colnames = raw.iloc[2].values.flatten().tolist()
                colnames[0] = 'road_segment'
                colnames[2] = 'segment_name'
                colnames[3:6] = [name + '_start' for name in colnames[3:6]]
                colnames[6:9] = [name + '_end' for name in colnames[6:9]]
                colnames[9] = 'length'
                colnames = dict(zip(raw.columns, colnames))
    
            raw = raw.iloc[3:]
            sf.aadt_raw = sf.aadt_raw.append(raw)
            # if epoch == 3:  # TODO: take out when done
            #     break
        sf.aadt_raw.rename(columns=colnames, inplace=True)
        sf.aadt_raw.reset_index(drop=True,inplace=True)
        return sf.aadt_raw

    def aadt_vehicles_only(sf):
        if hasattr(sf,'aadt_raw'): # if AADT raw does not exist, run it
            sf.get_aadt_raw()
        sf.aadt_vehicles_only = sf.aadt_raw.drop(columns=['segment_name','LRP_start','Offset_start','Chainage_start',
                                                          'LRP_end','Offset_end','Chainage_end', 'length']).\
                                                copy(deep=False)
        return sf.aadt_vehicles_only





if __name__ == '__main__':
    htm_item = TrafficDensity()
    htm_read = htm_item.get_aadt_raw()

