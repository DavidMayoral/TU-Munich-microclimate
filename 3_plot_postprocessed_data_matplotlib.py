import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os

##################################
# DEFINITIONS
##################################

input_folder = os.path.join("2_postprocessed_data", "general")
input_ext = ".csv"
output_folder = os.path.join("3_dataplots","matplotlib")

##################################
# IMPORTING DATA
##################################

print("\nStarting importing data")

df_ranges_a = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_monthly_airp' + input_ext))
df_ranges_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_monthly_city' + input_ext))

df_dir_a = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_windrose_coarse_airp' + input_ext))
df_dir_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_windrose_coarse_city' + input_ext))

df_dir2_a = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_windrose_fine_airp' + input_ext))
df_dir2_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_mean_windrose_fine_city' + input_ext))

df_comp_a = pd.read_csv(os.path.join(input_folder,'wind_velocity_comp_gust_vs_mean_airp' + input_ext))
df_comp_c = pd.read_csv(os.path.join(input_folder,'wind_velocity_comp_gust_vs_mean_city' + input_ext))

df_airp_m = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_mean_airp" + input_ext))
df_city_m = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_mean_city" + input_ext))

df_airp_g = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_gust_airp" + input_ext))
df_city_g = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_gust_city" + input_ext))

print("Ending importing data")

##########
# PLOTTING
##########

print("\nStarting plotting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Wind speed ranges
ranges = [2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5]
range_labels = ["<" + str(ranges[0])]
range_labels.extend([str(ranges[i])+"-"+str(ranges[i+1]) for i in [*range(len(ranges)-1)]])
range_labels.append(str(ranges[-1]) + ">")

# MONTHLY WINDS (airport)
fig = plt.figure(1)
plt.title("Monthly winds in Munich airport")
for idx, range_label in enumerate(range_labels):
    if idx == 0:
        plt.bar(df_ranges_a["Months"],df_ranges_a[range_label], label=range_label)
        prev_values = df_ranges_a[range_label]
    else:
        plt.bar(df_ranges_a["Months"],df_ranges_a[range_label], bottom=prev_values, label=range_label)
        prev_values = np.add(prev_values,df_ranges_a[range_label])
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"01_MonthWinds_airp.png"))
plt.savefig(os.path.join(output_folder,"01_MonthWinds_airp.pdf"))

# MONTHLY WINDS (city)
fig = plt.figure(2)
plt.title("Monthly winds in Munich city")
for idx, range_label in enumerate(range_labels):
    if idx == 0:
        plt.bar(df_ranges_c["Months"],df_ranges_a[range_label], label=range_label)
        prev_values = df_ranges_a[range_label]
    else:
        plt.bar(df_ranges_c["Months"],df_ranges_a[range_label], bottom=prev_values, label=range_label)
        prev_values = np.add(prev_values,df_ranges_a[range_label])
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"02_MonthWinds_city.png"))
plt.savefig(os.path.join(output_folder,"02_MonthWinds_city.pdf"))

# Windrose needs: https://python-windrose.github.io/windrose/index.html
# pip install windrose
# remains as WIP

# WIND SPEED DISTRIBUTION (airport)
fig = plt.figure(9)
plt.title("Wind intensity distribution in Munich airport")
data = df_airp_m['WindSpeed']
binwidth = 1
bins=range(int(min(data)), int(max(data)) + binwidth, binwidth)
# using weights and fixed bins to properly normalize
plt.hist(data, density=True, cumulative=False, weights=np.ones_like(data)*100./len(data), bins=bins)
shape, loc, scale = stats.weibull_min.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.weibull_min.pdf(x_line, shape, loc, scale)
plt.plot(x_line, y_line, 'r-', label='Weibull distribution')
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"09_Histogram_airp.png"))
plt.savefig(os.path.join(output_folder,"09_Histogram_airp.pdf"))

# WIND SPEED DISTRIBUTION (city)
fig = plt.figure(10)
plt.title("Wind intensity distribution in Munich city")
data = df_city_m['WindSpeed']
binwidth = 1
bins=range(int(min(data)), int(max(data)) + binwidth, binwidth)
# using weights and fixed bins to properly normalize
plt.hist(data, density=True, cumulative=False, weights=np.ones_like(data)*100./len(data), bins=bins)
shape, loc, scale = stats.weibull_min.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.weibull_min.pdf(x_line, shape, loc, scale)
plt.plot(x_line, y_line, 'r-', label='Weibull distribution')
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"10_Histogram_city.png"))
plt.savefig(os.path.join(output_folder,"10_Histogram_city.pdf"))

# WIND SPEED DISTRIBUTION (airport)
fig = plt.figure(11)
plt.title("Gust intensity distribution in Munich airport")
data = df_airp_g['MaxSpeed']
binwidth = 1
bins=range(int(min(data)), int(max(data)) + binwidth, binwidth)
# using weights and fixed bins to properly normalize
plt.hist(data, density=True, cumulative=False, weights=np.ones_like(data)*100./len(data), bins=bins)
shape, loc, scale = stats.weibull_min.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.weibull_min.pdf(x_line, shape, loc, scale)
plt.plot(x_line, y_line, 'r-', label='Weibull distribution')
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"11_Histogram_gust_airp.png"))
plt.savefig(os.path.join(output_folder,"11_Histogram_gust_airp.pdf"))

# WIND GUST DISTRIBUTION (city)
fig = plt.figure(12)
plt.title("Gust intensity distribution in Munich city")
data = df_city_g['MaxSpeed']
binwidth = 1
bins=range(int(min(data)), int(max(data)) + binwidth, binwidth)
# using weights and fixed bins to properly normalize
plt.hist(data, density=True, cumulative=False, weights=np.ones_like(data)*100./len(data), bins=bins)
shape, loc, scale = stats.weibull_min.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.weibull_min.pdf(x_line, shape, loc, scale)
plt.plot(x_line, y_line, 'r-', label='Weibull distribution')
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"11_Histogram_gust_city.png"))
plt.savefig(os.path.join(output_folder,"11_Histogram_gust_city.pdf"))

print("\nEnding plotting data")