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
output_folder = os.path.join("3_dataplots","munich_city_matplotlib")

##################################
# IMPORTING DATA
##################################

print("\nStarting importing data")

df_city_m = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_mean_city" + input_ext))

df_city_g = pd.read_csv(os.path.join(input_folder,"wind_velocity_distrib_gust_city" + input_ext))

print("Ending importing data")

##########
# PLOTTING
##########

print("\nStarting plotting data")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Munich city - mean and gust comparison over the years - as plot over time
fig = plt.figure(1)
# gust
start_year = float(df_city_g["Date"].iloc[0][:4])
end_year = float(df_city_g["Date"].iloc[-1][:4])
pseudo_year_series = np.linspace(start_year, end_year, num=len(df_city_g["Date"]), endpoint=True)
plt.plot(pseudo_year_series, df_city_g["MaxSpeed"], 'r--', label='Gust')
# mean
start_year = float(df_city_m["Date"].iloc[0][:4])
end_year = float(df_city_m["Date"].iloc[-1][:4])
pseudo_year_series = np.linspace(start_year, end_year, num=len(df_city_m["Date"]), endpoint=True)
plt.plot(pseudo_year_series, df_city_m["WindSpeed"], 'b-.', label='Mean')
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"01_MunichCity_GustMean_Yearly.png"))
plt.savefig(os.path.join(output_folder,"01_MunichCity_GustMean_Yearly.pdf"))

# Munich city - mean and gust comparison over the years - as histogram
from scipy.optimize import curve_fit

def gumbel_pdf(x, mu, beta):
    return (1 / beta) * np.exp(-(x - mu) / beta - np.exp(-(x - mu) / beta))

fig = plt.figure(2)
# gust
data = df_city_g['MaxSpeed']
binwidth = 0.5
start_val = min(data)
end_val = max(data)
bins=np.linspace(start_val, end_val, num=int((end_val - start_val)/binwidth), endpoint=True)
# using weights and fixed bins to properly normalize
plt.hist(data, density=True, cumulative=False, weights=np.ones_like(data)*100./len(data), bins=bins)
# gev (generalized extreme value) theory for bm (block maxima)
gev_shape, gev_loc, gev_scale = stats.genextreme.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.genextreme.pdf(x_line, gev_shape, gev_loc, gev_scale)
plt.plot(x_line, y_line, 'r--', label='GEV gust')

# mean
data = df_city_m['WindSpeed']
binwidth = 0.5
start_val = min(data)
end_val = max(data)
bins=np.linspace(start_val, end_val, num=int((end_val - start_val)/binwidth), endpoint=True)
# using weights and fixed bins to properly normalize
plt.hist(data, density=True, cumulative=False, weights=np.ones_like(data)*100./len(data), bins=bins)
# gev (generalized extreme value) theory for bm (block maxima)
gev_shape, gev_loc, gev_scale = stats.genextreme.fit(data)
x_line = np.linspace(np.min(data), np.max(data), 100)
y_line = stats.genextreme.pdf(x_line, gev_shape, gev_loc, gev_scale)
plt.plot(x_line, y_line, 'b-.', label='GEV mean')

plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"02_MunichCity_GustMean_Hist.png"))
plt.savefig(os.path.join(output_folder,"02_MunichCity_GustMean_Hist.pdf"))

gust_sorted = np.sort(df_city_g['MaxSpeed'])
mean_sorted = np.sort(df_city_m['WindSpeed'])

max_rank_gust = len(gust_sorted)
max_rank_mean = len(mean_sorted)

rank_gust = np.arange(1, max_rank_gust + 1) 
rank_mean = np.arange(1, max_rank_mean + 1)

gumbel_prob_nonexc_gust = rank_gust / (max_rank_gust + 1)
gumbel_prob_nonexc_mean = rank_mean / (max_rank_mean + 1)

gumbel_red_var_gust = -np.log(-np.log(gumbel_prob_nonexc_gust))
gumbel_red_var_mean = -np.log(-np.log(gumbel_prob_nonexc_mean))

[gumbel_slope_gust, gumbel_mode_gust] = np.polyfit(gumbel_red_var_gust, gust_sorted, 1)
[gumbel_slope_mean, gumbel_mode_mean] = np.polyfit(gumbel_red_var_mean, mean_sorted, 1)

return_period = np.arange(10, 1000, 10)
gumbel_predicted_gustwind = gumbel_mode_gust + gumbel_slope_gust * (-np.log(-np.log(1-1/return_period)))
gumbel_predicted_meanwind = gumbel_mode_mean + gumbel_slope_mean * (-np.log(-np.log(1-1/return_period)))

n_years_return_period=50
gumbel_predicted_gustwind_rp = gumbel_mode_gust + gumbel_slope_gust * (-np.log(-np.log(1-1/n_years_return_period)))
gumbel_predicted_meanwind_rp = gumbel_mode_mean + gumbel_slope_mean * (-np.log(-np.log(1-1/n_years_return_period)))

fig = plt.figure(3)
# gust
plt.plot(return_period, gumbel_predicted_gustwind, 'r--', label ='Gumbel\'s method - gust')
plt.text(200,gumbel_predicted_gustwind_rp,'Predicted gust wind for ' + str(n_years_return_period) + 
    ' year return period (m/s)\n' + ' Gumbel Method = ' + str(round(gumbel_predicted_gustwind_rp,2)))
# mean
plt.plot(return_period, gumbel_predicted_meanwind, 'b-.', label ='Gumbel\'s method - mean')
plt.text(200,gumbel_predicted_meanwind_rp,'Predicted mean wind for ' + str(n_years_return_period) + 
    ' year return period (m/s)\n' + ' Gumbel Method = ' + str(round(gumbel_predicted_meanwind_rp,2)))
plt.axvline(n_years_return_period, color='k', linestyle='--', label = 'return period = ' + str(n_years_return_period))
plt.ylabel('Predicted wind speed m/s')
plt.xlabel('Return period (Years)')
plt.title('Wind speed prediction')
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"03_MunichCity_GustMean_RP50.png"))
plt.savefig(os.path.join(output_folder,"03_MunichCity_GustMean_RP50.pdf"))

print("\nEnding plotting data")