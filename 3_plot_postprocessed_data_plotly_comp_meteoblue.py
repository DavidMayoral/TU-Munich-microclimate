import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import os

##################################
# DEFINITIONS
##################################

input_folder = os.path.join("2_postprocessed_data", "comp_meteoblue")
input_ext = ".csv"
output_folder = os.path.join("3_dataplots","plotly_comp_meteoblue")

##################################
# IMPORTING DATA
##################################

print("\nStarting importing data")

df_ranges_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_monthly_city' + input_ext))

df_dir2_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_windrose_fine_city' + input_ext))

print("Ending importing data")

##########
# PLOTTING
##########

print("\nStarting plotting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Wind speed ranges
# for comparison with MeteoBlue data:
# they have ranges in km/h: "<1","1-5","5-12","12-19","19-28","28-38","38-50","50-61",">61"
# the conversion factor is dividing by 3.6 to get to m/s
# km/h -> [1.00, 5.00, 12.00, 19.00, 28.00, 38.00, 50.00, 61.00]
# m/s  -> [0.28, 1.39,  3.33,  5.28,  7.78, 10.56, 13.89, 16.95]
ranges = [0.28, 1.39, 3.33, 5.28, 7.78, 10.56, 13.89, 16.95]
ranges_kmh = [1.00, 5.00, 12.00, 19.00, 28.00, 38.00, 50.00, 61.00]
range_labels = ["<" + str(ranges_kmh[0])]
range_labels.extend([str(ranges_kmh[i])+"-"+str(ranges_kmh[i+1]) for i in [*range(len(ranges_kmh)-1)]])
range_labels.append(str(ranges_kmh[-1]) + ">")

# MONTHLY WINDS (city)
fig2 = px.bar(df_ranges_c, x=df_ranges_c.index, y=range_labels, title='Monthly winds in Munich city', labels={'index':'Month','value':'Frequency'}, template="plotly_white", color_discrete_sequence= px.colors.sequential.Plasma_r)
fig2.write_html(os.path.join(output_folder,"02_MonthWinds_city.html"))
fig2.write_image(os.path.join(output_folder,"02_MonthWinds_city.png"))
fig2.write_image(os.path.join(output_folder,"02_MonthWinds_city.svg"))

# PRECISE WINDROSE (city)
fig6 = px.bar_polar(df_dir2_c, r="Frequency", theta="Direction", color="SpeedRange [km/h]", title='Wind direction and intensity in Munich city', template="plotly_white", color_discrete_sequence= px.colors.sequential.Plasma_r)
fig6.write_html(os.path.join(output_folder,"06_WindRose_precise_city.html"))
fig6.write_image(os.path.join(output_folder,"06_WindRose_precise_city.png"))
fig6.write_image(os.path.join(output_folder,"06_WindRose_precise_city.svg"))

print("\nEnding plotting data")