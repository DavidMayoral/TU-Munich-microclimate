import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os

##################################
# DEFINITIONS
##################################

input_folder = "postprocessed_data"
input_ext = ".csv"
output_folder = os.path.join("dataplots","matplotlib")

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
'''
# AVERAGE WINDS PER YEAR
plt.figure(figsize=(10.5,5))
plt.title('Average winds in Munich city and airport')

years = [np.arange(1997, 2023, 1),
         np.arange(1992, 2023, 1)]
yearly_winds1 = df_city_m.groupby(df_city_m.index.to_period('A')).mean()    # city
yearly_winds2 = df_airp_m.groupby(df_airp_m.index.to_period('A')).mean()    # airport

plt.subplot(121)
plt.bar(years[0], yearly_winds1['WindSpeed'])
plt.xlabel('Year')
plt.ylabel('[m/s]')
plt.title('Munich city')
plt.ylim([0,4])

plt.subplot(122)
plt.bar(years[1], yearly_winds2['WindSpeed'])
plt.xlabel('Year')
plt.ylabel('[m/s]')
plt.title('Munich airport')
plt.ylim([0,4])

plt.show()
'''

print("\nStarting plotting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# MONTHLY WINDS (airport)
fig = plt.figure(1)
plt.title("Monthly winds in Munich airport")
for idx, range_label in enumerate(["<1","1-3","3-6","6-10",">10"]):
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
for idx, range_label in enumerate(["<1","1-3","3-6","6-10",">10"]):
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
plt.title("Wind intenstiy distribution in Munich airport")
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
plt.title("Wind intenstiy distribution in Munich city")
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

plt.show()

print("\nEnding plotting data")