import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
# import plotly.express as px

import os

from dwd_data_info import dwd_data_info

##################################
# DEFINITIONS
##################################

input_folder = "downloaded_data_files"
output_folder = "postprocessed_data"
output_ext = ".csv"

##################################
# READ DATA AND INITIALIZE PANDAS
##################################

print("\nStarting reading and initializing")
# City mean wind information
df_city_m = pd.read_csv(os.path.join(input_folder, dwd_data_info["CityMean"]["file_name"]), sep=";")    
# City gust wind information
df_city_g = pd.concat([pd.read_csv(os.path.join(input_folder, dwd_data_info["CityGust1"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["CityGust2"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["CityGust3"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["CityGust4"]["file_name"]), sep=";")])    

# Airport mean wind information
df_airp_m = pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpMean"]["file_name"]), sep=";")
# Airport gust wind information
df_airp_g = pd.concat([pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpGust1"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpGust2"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpGust3"]["file_name"]), sep=";"), 
                      pd.read_csv(os.path.join(input_folder, dwd_data_info["AirpGust4"]["file_name"]), sep=";")])    

dataframes = [df_airp_m, df_city_m, df_airp_g, df_city_g]
print("Ending reading and intializing")

##################################
# FILTERING AND PROCESSING OF DATA
##################################

print("\nStarting filtering and postprocessing")

for i, df in enumerate(dataframes):
    if i < 2:
        df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H')      # Converting to datetime format
    else:
        df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H%M')
    df = df.rename(columns={'MESS_DATUM':'Date',                                    # Renaming columns to more descriptive names
                            'STATIONS_ID':'Station',
                            'QN':'QualityLevel',
                            'QN_3':'QualityLevel',
                            '   F':'WindSpeed',
                            '   D':'WindDirection',
                            'FX_10':'MaxSpeed',
                            'DX_10':'MaxDir',
                            'FMX_10':'MaxMean',
                            'FNX_10':'MinSpeed'})
    df = df.set_index(['Date'])
    try:
        # NOTE: this throws and error, why?
        del df['eor'] # Deleting end Of Report column
    except:
        pass
    
    if i < 2:
        df = df[df.WindSpeed >= 0]                                                  # Keeping only positive values
        df = df[df.WindDirection >= 0]
    else:
        df = df[df.MaxSpeed >= 0]
        df = df.replace({-999.0: np.nan})                                           # Not available data are stored as "-999.0"
    dataframes[i] = df
[df_airp_m, df_city_m, df_airp_g, df_city_g] = dataframes[:]                              # Assigning the obtained values back to the original variables

date_lim = datetime(1997, 7, 1)                                                     # Using only data generated by automated stations (from 1997 for the city station)
df_city_m = df_city_m[df_city_m.index > date_lim]

### 1.- MEAN

# Wind speed ranges
ranges = [1, 3, 6, 10]      # Slices into which the wind intensity is to be divided into
dataframes_a = []           # Stores the different subsets of data based on the wind intensity. dataframes_a[0] will only have the entries where the wind was at lowest intensity
dataframes_c = []
dataframes_a.append(df_airp_m[df_airp_m.WindSpeed < ranges[0]])
dataframes_c.append(df_city_m[df_city_m.WindSpeed < ranges[0]])
for i in range(1, len(ranges)):
    dataframes_a.append(df_airp_m[(df_airp_m.WindSpeed > ranges[i-1]) & (df_airp_m.WindSpeed < ranges[i])])
    dataframes_c.append(df_city_m[(df_city_m.WindSpeed > ranges[i-1]) & (df_city_m.WindSpeed < ranges[i])])
dataframes_a.append(df_airp_m[df_airp_m.WindSpeed > ranges[-1]])
dataframes_c.append(df_city_m[df_city_m.WindSpeed > ranges[-1]])

months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
directions2 = np.arange(0, 360, 10).tolist()     # 10-degree steps

# Wind speed ranges per month
ranges_a = np.zeros((12,len(ranges)+1))             # Stores how often in month (i+1) the wind has been blowing with intensity j
ranges_c = np.zeros((12,len(ranges)+1))
for i in range(12):
    for j, df in enumerate(dataframes_a):
        ranges_a[i,j] = len(df.loc[df.index.month == i+1].WindSpeed)
    for j, df in enumerate(dataframes_c):
        ranges_c[i,j] = len(df.loc[df.index.month == i+1].WindSpeed)
df_ranges_a = pd.DataFrame(ranges_a, index=months, columns=["<1","1-3","3-6","6-10",">10"])
df_ranges_c = pd.DataFrame(ranges_c, index=months, columns=["<1","1-3","3-6","6-10",">10"])

for i,month in enumerate(months):       # Rescaling the frequency value to the number of days in each month
    if i==0 or i==2 or i==4 or i==6 or i==7 or i==9 or i==11:
        df_ranges_a.loc[month] = df_ranges_a.loc[month] / df_ranges_a.loc[month].sum() * 31
        df_ranges_c.loc[month] = df_ranges_c.loc[month] / df_ranges_c.loc[month].sum() * 31
    elif i==1:
        df_ranges_a.loc[month] = df_ranges_a.loc[month] / df_ranges_a.loc[month].sum() * 28
        df_ranges_c.loc[month] = df_ranges_c.loc[month] / df_ranges_c.loc[month].sum() * 28
    else:
        df_ranges_a.loc[month] = df_ranges_a.loc[month] / df_ranges_a.loc[month].sum() * 30
        df_ranges_c.loc[month] = df_ranges_c.loc[month] / df_ranges_c.loc[month].sum() * 30

# Wind ranges per direction (8 Himmelrichtungen)
dir_a = np.zeros((8,len(ranges)+1))                  # Stores how often the wind of intensity j has been blowing in direction 45*i degrees
dir_c = np.zeros((8,len(ranges)+1))
for j, df in enumerate(dataframes_a):
    dir_a[0,j] = len(df[(df.WindDirection > 360-22.5) | (df.WindDirection < 22.5)])
for j, df in enumerate(dataframes_c):
    dir_c[0,j] = len(df[(df.WindDirection > 360-22.5) | (df.WindDirection < 22.5)])
for i in range(1,8):
    for j, df in enumerate(dataframes_a):
        dir_a[i,j] = len(df[(df.WindDirection > (45*i)-22.5) & (df.WindDirection < (45*i)+22.5)])       
    for j, df in enumerate(dataframes_c):
        dir_c[i,j] = len(df[(df.WindDirection > (45*i)-22.5) & (df.WindDirection < (45*i)+22.5)]) 

df_dir_a = pd.DataFrame(dir_a, index=directions, columns=["<1","1-3","3-6","6-10",">10"])   # Creating a df from the arrays obtained
df_dir_c = pd.DataFrame(dir_c, index=directions, columns=["<1","1-3","3-6","6-10",">10"])
df_dir_a = pd.melt(df_dir_a.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')   # Changes df type from "wide" to "long"
df_dir_c = pd.melt(df_dir_c.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')
df_dir_a.rename(columns={'index': 'Direction'}, inplace=True)
df_dir_c.rename(columns={'index': 'Direction'}, inplace=True)

# Wind ranges per direction (10-degree precision)
dir2_a = np.zeros((36,len(ranges)+1))
dir2_c = np.zeros((36,len(ranges)+1))
for j,df in enumerate(dataframes_a):
    dir2_a[0,j] = len(df[(df.WindDirection > 360-5) | (df.WindDirection < 5)])
for j,df in enumerate(dataframes_c):
    dir2_c[0,j] = len(df[(df.WindDirection > 360-5) | (df.WindDirection < 5)])
for i in range(1,36):
    for j, df in enumerate(dataframes_a):
        dir2_a[i,j] = len(df[(df.WindDirection > (10*i)-5) & (df.WindDirection < (10*i)+5)])
    for j, df in enumerate(dataframes_c):
        dir2_c[i,j] = len(df[(df.WindDirection > (10*i)-5) & (df.WindDirection < (10*i)+5)])   

df_dir2_a = pd.DataFrame(dir2_a, index=directions2, columns=["<1","1-3","3-6","6-10",">10"])
df_dir2_c = pd.DataFrame(dir2_c, index=directions2, columns=["<1","1-3","3-6","6-10",">10"])
df_dir2_a = pd.melt(df_dir2_a.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')    
df_dir2_c = pd.melt(df_dir2_c.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')
df_dir2_a.rename(columns={'index': 'Direction'}, inplace=True)
df_dir2_c.rename(columns={'index': 'Direction'}, inplace=True)

### 2.- GUST

# Comparison mean vs gust speed per month
df_comp_a = pd.DataFrame(index=months, columns=["Mean", "Gust"])        # Stores monthly average of the mean and gust winds
df_comp_c = pd.DataFrame(index=months, columns=["Mean", "Gust"])
df_comp_a['Mean'] = df_airp_m.groupby(df_airp_m.index.month).mean().WindSpeed.to_list()
df_comp_a['Gust'] = df_airp_g.groupby(df_airp_g.index.month).mean().MaxSpeed.to_list()
df_comp_c['Mean'] = df_city_m.groupby(df_city_m.index.month).mean().WindSpeed.to_list()
df_comp_c['Gust'] = df_city_g.groupby(df_city_g.index.month).mean().MaxSpeed.to_list()

print("Ending filtering and postprocessing")

##################################
# EXPORTING DATA
##################################

print("\nStarting exporting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df_ranges_a.to_csv(os.path.join(output_folder,'wind_velocity_mean_monthly_airp' + output_ext))
df_ranges_c.to_csv(os.path.join(output_folder,'wind_velocity_mean_monthly_city' + output_ext))

df_dir_a.to_csv(os.path.join(output_folder,'wind_velocity_mean_windrose_coarse_airp' + output_ext))
df_dir_c.to_csv(os.path.join(output_folder,'wind_velocity_mean_windrose_coarse_city' + output_ext))

df_dir2_a.to_csv(os.path.join(output_folder,'wind_velocity_mean_windrose_fine_airp' + output_ext))
df_dir2_c.to_csv(os.path.join(output_folder,'wind_velocity_mean_windrose_fine_airp' + output_ext))

df_comp_a.to_csv(os.path.join(output_folder,'wind_velocity_comp_gust_vs_mean_airp' + output_ext))
df_comp_c.to_csv(os.path.join(output_folder,'wind_velocity_comp_gust_vs_mean_city' + output_ext))

df_airp_m.to_csv(os.path.join(output_folder,"wind_velocity_distrib_mean_airp" + output_ext))
df_city_m.to_csv(os.path.join(output_folder,"wind_velocity_distrib_mean_city" + output_ext))

df_airp_g.to_csv(os.path.join(output_folder,"wind_velocity_distrib_gust_airp" + output_ext))
df_city_g.to_csv(os.path.join(output_folder,"wind_velocity_distrib_gust_city" + output_ext))

print("Ending exporting data")

# ##########
# # PLOTTING
# ##########
# '''
# # AVERAGE WINDS PER YEAR
# plt.figure(figsize=(10.5,5))
# plt.title('Average winds in Munich city and airport')

# years = [np.arange(1997, 2023, 1),
#          np.arange(1992, 2023, 1)]
# yearly_winds1 = df_city_m.groupby(df_city_m.index.to_period('A')).mean()    # city
# yearly_winds2 = df_airp_m.groupby(df_airp_m.index.to_period('A')).mean()    # airport

# plt.subplot(121)
# plt.bar(years[0], yearly_winds1['WindSpeed'])
# plt.xlabel('Year')
# plt.ylabel('[m/s]')
# plt.title('Munich city')
# plt.ylim([0,4])

# plt.subplot(122)
# plt.bar(years[1], yearly_winds2['WindSpeed'])
# plt.xlabel('Year')
# plt.ylabel('[m/s]')
# plt.title('Munich airport')
# plt.ylim([0,4])

# plt.show()
# '''
# # MONTHLY WINDS (airport)
# fig1 = px.bar(df_ranges_a, x=df_ranges_a.index, y=["<1","1-3","3-6","6-10",">10"], title='Monthly winds in Munich airport', labels={'index':'Month','value':'Frequency'}, color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig1.write_html("Relevant graphs/01_MonthWinds_airp.html")
# fig1.write_image("Relevant graphs/01_MonthWinds_airp.png")
# fig1.write_image("Relevant graphs/01_MonthWinds_airp.svg")

# # MONTHLY WINDS (city)
# fig2 = px.bar(df_ranges_c, x=df_ranges_c.index, y=["<1","1-3","3-6","6-10",">10"], title='Monthly winds in Munich city', labels={'index':'Month','value':'Frequency'}, color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig2.write_html("Relevant graphs/02_MonthWinds_city.html")
# fig2.write_image("Relevant graphs/02_MonthWinds_city.png")
# fig2.write_image("Relevant graphs/02_MonthWinds_city.svg")

# # WINDROSE (airport)
# fig3 = px.bar_polar(df_dir_a, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich airport', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig3.write_html("Relevant graphs/03_WindRose_airp.html")
# fig3.write_image("Relevant graphs/03_WindRose_airp.png")
# fig3.write_image("Relevant graphs/03_WindRose_airp.svg")

# # WINDROSE (city)
# fig4 = px.bar_polar(df_dir_c, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich city', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig4.write_html("Relevant graphs/04_WindRose_city.html")
# fig4.write_image("Relevant graphs/04_WindRose_city.png")
# fig4.write_image("Relevant graphs/04_WindRose_city.svg")

# # PRECISE WINDROSE (airport)
# fig5 = px.bar_polar(df_dir2_a, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich airport', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig5.write_html("Relevant graphs/05_WindRose_precise_airp.html")
# fig5.write_image("Relevant graphs/05_WindRose_precise_airp.png")
# fig5.write_image("Relevant graphs/05_WindRose_precise_airp.svg")

# # PRECISE WINDROSE (city)
# fig6 = px.bar_polar(df_dir2_c, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich city', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig6.write_html("Relevant graphs/06_WindRose_precise_city.html")
# fig6.write_image("Relevant graphs/06_WindRose_precise_city.png")
# fig6.write_image("Relevant graphs/06_WindRose_precise_city.svg")

# # GUST vs MEAN (airport)
# fig7 = px.line(df_comp_a, x=df_comp_a.index, y=["Gust", "Mean"], title='Mean vs Gust intensity in Munich airport')
# fig7.update_yaxes(range=[0,6])
# fig7.write_html("Relevant graphs/07_GustvsMean_airp.html")
# fig7.write_image("Relevant graphs/07_GustvsMean_airp.png")
# fig7.write_image("Relevant graphs/07_GustvsMean_airp.svg")

# # GUST vs MEAN (city)
# fig8 = px.line(df_comp_c, x=df_comp_c.index, y=["Gust", "Mean"], title='Mean vs Gust intensity in Munich city')
# fig8.update_yaxes(range=[0,6])
# fig8.write_html("Relevant graphs/08_GustvsMean_city.html")
# fig8.write_image("Relevant graphs/08_GustvsMean_city.png")
# fig8.write_image("Relevant graphs/08_GustvsMean_city.svg")

# # WIND SPEED DISTRIBUTION (airport)
# fig9 = px.histogram(df_airp_m, x='WindSpeed', nbins=100, title='Wind intenstiy distribution in Munich airport')
# fig9.update_layout(bargap = 0.05)
# fig9.update_xaxes(range=[0,20])
# shape, loc, scale = stats.weibull_min.fit(df_airp_m['WindSpeed'])     # Weibull distribution fit
# x_line = np.linspace(np.min(df_airp_m['WindSpeed']), np.max(df_airp_m['WindSpeed']), 100)
# y_line = stats.weibull_min.pdf(x_line, shape, loc, scale) * 125000
# df_line = pd.DataFrame({"x": x_line, "y": y_line})
# fig9.add_scatter(x=df_line["x"], y=df_line["y"], mode="lines", name="Weibull Distribution")
# fig9.write_html("Relevant graphs/09_Histogram_airp.html")
# fig9.write_image("Relevant graphs/09_Histogram_airp.png")
# fig9.write_image("Relevant graphs/09_Histogram_airp.svg")

# # WIND SPEED DISTRIBUTION (city)
# fig10 = px.histogram(df_city_m, x='WindSpeed', nbins=100, title='Wind intenstiy distribution in Munich city')
# fig10.update_layout(bargap = 0.05)
# fig10.update_xaxes(range=[0,20])
# shape, loc, scale = stats.weibull_min.fit(df_city_m['WindSpeed'])     # Weibull distribution fit
# x_line = np.linspace(np.min(df_city_m['WindSpeed']), np.max(df_city_m['WindSpeed']), 100)
# y_line = stats.weibull_min.pdf(x_line, shape, loc, scale) * 40450
# df_line = pd.DataFrame({"x": x_line, "y": y_line})
# fig10.add_scatter(x=df_line["x"], y=df_line["y"], mode="lines", name="Weibull Distribution")
# fig10.write_html("Relevant graphs/10_Histogram_city.html")
# fig10.write_image("Relevant graphs/10_Histogram_city.png")
# fig10.write_image("Relevant graphs/10_Histogram_city.svg")

# # WIND GUST DISTRIBUTION (airport)
# fig11 = px.histogram(df_airp_g, x='MaxSpeed', nbins=200, title='Gust intenstiy distribution in Munich airport')
# fig11.update_layout(bargap = 0.05)
# fig11.update_xaxes(range=[0,20])
# fig11.write_html("Relevant graphs/11_Histogram_gust_airp.html")
# fig11.write_image("Relevant graphs/11_Histogram_gust_airp.png")
# fig11.write_image("Relevant graphs/11_Histogram_gust_airp.svg")

# # WIND GUST DISTRIBUTION (city)
# fig12 = px.histogram(df_city_g, x='MaxSpeed', nbins=200, title='Gust intensity distribution in Munich city')
# fig12.update_layout(bargap = 0.05)
# fig12.update_xaxes(range=[0,20])
# fig12.write_html("Relevant graphs/12_Histogram_gust_city.html")
# fig12.write_image("Relevant graphs/12_Histogram_gust_city.png")
# fig12.write_image("Relevant graphs/12_Histogram_gust_city.svg")
