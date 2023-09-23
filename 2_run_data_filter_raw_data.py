import pandas as pd
import numpy as np
from datetime import datetime
import os

from dwd_data_info import dwd_data_info

##################################
# DEFINITIONS
##################################

input_folder = "1_downloaded_data_files"
output_folder = os.path.join("2_filtered_data")
output_ext = ".csv"

##################################
# READING DATA
##################################

print("\nStarting reading data")
# City hourly wind information
df_city_hourly_mean = pd.read_csv(os.path.join(input_folder, dwd_data_info["CityHourlyMean"]["file_name"]), sep=";")    
# City 10-minutes mean wind information
df_city_10min_mean = pd.concat([pd.read_csv(os.path.join(input_folder, dwd_data_info["City10MinMean1"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["City10MinMean2"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["City10MinMean3"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["City10MinMean4"]["file_name"]), sep=";")])    

# City 10-minutes gust wind information
df_city_10min_max = pd.concat([pd.read_csv(os.path.join(input_folder, dwd_data_info["City10MinMax1"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["City10MinMax2"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["City10MinMax3"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["City10MinMax4"]["file_name"]), sep=";")])    

# Airport hourly mean wind information
df_airp_hourly_mean = pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpHourlyMean"]["file_name"]), sep=";")
# Airport 10-minutes mean wind information
df_airp_10min_mean = pd.concat([pd.read_csv(os.path.join(input_folder, dwd_data_info["Airp10MinMean1"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["Airp10MinMean2"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["Airp10MinMean3"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["Airp10MinMean4"]["file_name"]), sep=";")])    

# Airport 10-minutes gust wind information
df_airp_10min_max = pd.concat([pd.read_csv(os.path.join(input_folder, dwd_data_info["Airp10MinMax1"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["Airp10MinMax2"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["Airp10MinMax3"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["Airp10MinMax4"]["file_name"]), sep=";")])    

raw_data = {
    'hourly_mean': [df_city_hourly_mean, df_airp_hourly_mean],
    '10-minutes_mean':[df_city_10min_mean, df_airp_10min_mean],
    '10-minutes_max':[df_city_10min_max,df_airp_10min_max]
    }
print("Ending reading data")

##################################
# FILTERING DATA
##################################

print("\nStarting filtering data")

# case-specific formatting and filtering
for rw in raw_data:   
    if 'hourly' in rw:
        columns_to_keep = ['MESS_DATUM', '   F', '   D']
        for idx, rw_df in enumerate(raw_data[rw]):
            rw_df = rw_df[columns_to_keep]
            rw_df['MESS_DATUM'] = pd.to_datetime(rw_df['MESS_DATUM'], format='%Y%m%d%H')
            rw_df = rw_df.rename(columns={'MESS_DATUM':'Date',                                    # Renaming columns to more descriptive names
                                    '   F':'WindVelocity',
                                    '   D':'WindDirection'})
            # save changes
            raw_data[rw][idx] = rw_df
    elif '10-minutes' in rw:
        if 'mean' in rw:
            columns_to_keep = ['MESS_DATUM', 'FF_10', 'DD_10']
            for idx, rw_df in enumerate(raw_data[rw]):
                rw_df = rw_df[columns_to_keep]
                rw_df['MESS_DATUM'] = pd.to_datetime(rw_df['MESS_DATUM'], format='%Y%m%d%H%M')
                rw_df = rw_df.rename(columns={'MESS_DATUM':'Date',                                    # Renaming columns to more descriptive names
                        'FF_10':'WindVelocity',
                        'DD_10':'WindDirection'})
                # save changes
                raw_data[rw][idx] = rw_df         
        elif 'max' in rw:
            columns_to_keep = ['MESS_DATUM', 'FX_10', 'DX_10']
            for idx, rw_df in enumerate(raw_data[rw]):
                rw_df = rw_df[columns_to_keep]
                rw_df['MESS_DATUM'] = pd.to_datetime(rw_df['MESS_DATUM'], format='%Y%m%d%H%M')
                rw_df = rw_df.rename(columns={'MESS_DATUM':'Date',                                    # Renaming columns to more descriptive names
                        'FX_10':'WindVelocity',
                        'DX_10':'WindDirection'})
                # save changes
                raw_data[rw][idx] = rw_df
                
# general formatting and filtering
for rw in raw_data:
    for idx, rw_df in enumerate(raw_data[rw]):
        rw_df = rw_df.set_index(['Date'])

        # only take positive value to ba able to postprocess
        rw_df = rw_df[rw_df.WindVelocity >= 0]
        rw_df = rw_df[rw_df.WindDirection >= 0]
        
        # NOTE: enable this to only have data from automated readings in the city
        # instead of starting from 1985 have samples from 1997
        # if rw == 'hourly_mean' and idx == 0:
        #     # for the hourly of the station in the city city
        #     # using only data generated by automated stations
        #     date_lim = datetime(1997, 7, 1)
        #     rw_df = rw_df[rw_df.index > date_lim]
            
        # save changes
        raw_data[rw][idx] = rw_df

print("Ending filtering data")

##################################
# EXPORTING DATA
##################################

print("\nStarting exporting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

raw_data['hourly_mean'][0].to_csv(os.path.join(output_folder,'wind_hourly_mean_city' + output_ext))
raw_data['hourly_mean'][1].to_csv(os.path.join(output_folder,'wind_hourly_mean_airp' + output_ext))

raw_data['10-minutes_mean'][0].to_csv(os.path.join(output_folder,'wind_10min_mean_city' + output_ext))
raw_data['10-minutes_mean'][1].to_csv(os.path.join(output_folder,'wind_10min_mean_airp' + output_ext))

raw_data['10-minutes_max'][0].to_csv(os.path.join(output_folder,'wind_10min_max_city' + output_ext))
raw_data['10-minutes_max'][1].to_csv(os.path.join(output_folder,'wind_10min_max_airp' + output_ext))

print("Ending exporting data")