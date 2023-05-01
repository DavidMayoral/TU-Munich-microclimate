import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px

file = ["produkt_ff_stunde_19850101_20221231_03379.txt",
        "produkt_ff_stunde_19920519_20221231_01262.txt"]

df_city = pd.read_csv(file[0], sep=";")
df_airp = pd.read_csv(file[1], sep=";")

##################################
# FILTERING AND PROCESSING OF DATA
##################################
df_city['MESS_DATUM'] = pd.to_datetime(df_city['MESS_DATUM'], format='%Y%m%d%H')
df_airp['MESS_DATUM'] = pd.to_datetime(df_airp['MESS_DATUM'], format='%Y%m%d%H')

df_city = df_city.rename(columns={'MESS_DATUM':'Date', 'STATIONS_ID':'Station', 'QN_3':'QualityLevel', '   F':'WindSpeed', '   D':'WindDirection'})
df_city = df_city.set_index(['Date'])
df_airp = df_airp.rename(columns={'MESS_DATUM':'Date', 'STATIONS_ID':'Station', 'QN_3':'QualityLevel', '   F':'WindSpeed', '   D':'WindDirection'})
df_airp = df_airp.set_index(['Date'])
# df = df.iloc[:, 0:-1]
del df_city['eor']
del df_airp['eor']
df_city = df_city[df_city.WindSpeed >= 0]
df_airp = df_airp[df_airp.WindSpeed >= 0]
df_city = df_city[df_city.WindDirection >= 0]
df_airp = df_airp[df_airp.WindDirection >= 0]
date_lim = datetime(1997, 7, 1)
df_city = df_city[df_city.index > date_lim]

# Wind speed ranges
df1a = df_airp[df_airp.WindSpeed < 1]
df2a = df_airp[(df_airp.WindSpeed > 1) & (df_airp.WindSpeed < 3)]
df3a = df_airp[(df_airp.WindSpeed > 3) & (df_airp.WindSpeed < 6)]
df4a = df_airp[(df_airp.WindSpeed > 6) & (df_airp.WindSpeed < 10)]
df5a = df_airp[df_airp.WindSpeed > 10]
dataframes_a = [df1a, df2a, df3a, df4a, df5a]

df1c = df_city[df_city.WindSpeed < 1]
df2c = df_city[(df_city.WindSpeed > 1) & (df_city.WindSpeed < 3)]
df3c = df_city[(df_city.WindSpeed > 3) & (df_city.WindSpeed < 6)]
df4c = df_city[(df_city.WindSpeed > 6) & (df_city.WindSpeed < 10)]
df5c = df_city[df_city.WindSpeed > 10]
dataframes_c = [df1c, df2c, df3c, df4c, df5c]

months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
directions2 = np.arange(0, 360, 10).tolist()

# Wind ranges per month
ranges_a = np.zeros((12,5))
ranges_c = np.zeros((12,5))
for i in range(12):
    for j, df in enumerate(dataframes_a):
        ranges_a[i,j] = len(df.loc[df.index.month == i+1].WindSpeed)
    for j, df in enumerate(dataframes_c):
        ranges_c[i,j] = len(df.loc[df.index.month == i+1].WindSpeed)
df_ranges_a = pd.DataFrame(ranges_a, index=months, columns=["<1","1-3","3-6","6-10",">10"])
df_ranges_c = pd.DataFrame(ranges_c, index=months, columns=["<1","1-3","3-6","6-10",">10"])

# Wind ranges per direction
dir_a = np.zeros((8,5))
dir_c = np.zeros((8,5))
for j, df in enumerate(dataframes_a):
    dir_a[0,j] = len(df[(df.WindDirection > 360-22.5) | (df.WindDirection < 22.5)])
for j, df in enumerate(dataframes_c):
    dir_c[0,j] = len(df[(df.WindDirection > 360-22.5) | (df.WindDirection < 22.5)])
for i in range(1,8):
    for j, df in enumerate(dataframes_a):
        dir_a[i,j] = len(df[(df.WindDirection > (45*i)-22.5) & (df.WindDirection < (45*i)+22.5)])        
    for j, df in enumerate(dataframes_c):
        dir_c[i,j] = len(df[(df.WindDirection > (45*i)-22.5) & (df.WindDirection < (45*i)+22.5)]) 

df_dir_a = pd.DataFrame(dir_a, index=directions, columns=["<1","1-3","3-6","6-10",">10"])
df_dir_c = pd.DataFrame(dir_c, index=directions, columns=["<1","1-3","3-6","6-10",">10"])
df_dir_a = pd.melt(df_dir_a.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')
df_dir_c = pd.melt(df_dir_c.reset_index(), id_vars=['index'], var_name='SpeedRange [m/s]', value_name='Frequency')
df_dir_a.rename(columns={'index': 'Direction'}, inplace=True)
df_dir_c.rename(columns={'index': 'Direction'}, inplace=True)

# Wind ranges per direction (precise)
dir2_a = np.zeros((36,5))
dir2_c = np.zeros((36,5))
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

fig4 = px.bar_polar(df_dir2_a, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich airport', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig4.show()
fig4.write_html("windrose_precise_airp.html")

fig5 = px.bar_polar(df_dir_c, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich city', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig5.show()
fig5.write_html("windrose_city.html")

fig6 = px.bar_polar(df_dir2_c, r="Frequency", theta="Direction", color="SpeedRange [m/s]", title='Wind direction and intensity in Munich city', template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
# fig6.show()
fig6.write_html("windrose_precise_city.html")
