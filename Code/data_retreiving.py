# -*- coding: utf-8 -*-

import requests
import io
import zipfile

urls = ["https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/historical/stundenwerte_FF_01262_19920519_20221231_hist.zip",
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/historical/stundenwerte_FF_03379_19850101_20221231_hist.zip",
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_19920520_19991231_hist.zip",
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_20000101_20091231_hist.zip",
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_20100101_20191231_hist.zip",
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_20200101_20221231_hist.zip",
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_19970712_19991231_hist.zip",
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_20000101_20091231_hist.zip",
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_20100101_20191231_hist.zip",
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_20200101_20221231_hist.zip"]
          
# REQUEST FROM DATABASE
response = [None] * len(urls)   # this will store the response of the server for each url
errorcount = 0
for i, url in enumerate(urls):
    response[i] = requests.get(url)
    '''
    if response[i].status_code == 404:
        print("Error: File not found")
    if response[i].status_code == 503:
        print("Error: Service unavailable")
    if response[i].status_code == 401:
        print("Error: Unauthorised (Authentication required)")
    if response[i].status_code == 403:
        print("Error: Forbidden")
    '''
    if response[i].status_code == 200:
        # print("Download successful")
        pass
    else:
        errorcount += 1
print("Request terminated with", errorcount, "errors.")

files = [r"produkt_ff_stunde_19920519_20221231_01262.txt",
         r"produkt_ff_stunde_19850101_20221231_03379.txt",
         r"produkt_zehn_min_fx_19920520_19991231_01262.txt",
         r"produkt_zehn_min_fx_20000101_20091231_01262.txt",
         r"produkt_zehn_min_fx_20100101_20191231_01262.txt",
         r"produkt_zehn_min_fx_20200101_20221231_01262.txt",
         r"produkt_zehn_min_fx_19970712_19991231_03379.txt",
         r"produkt_zehn_min_fx_20000101_20091231_03379.txt",
         r"produkt_zehn_min_fx_20100101_20191231_03379.txt",
         r"produkt_zehn_min_fx_20200101_20221231_03379.txt"]

# FILE EXTRACTION FROM ZIP
for i, file in enumerate(files):
    with zipfile.ZipFile(io.BytesIO(response[i].content)) as z:
        #z.extractall("C:\Users\david\TRABAJO\HiWi Windingenieurwesen\Wind microclimate\Einstellung")
        z.extract(file, path=r"DataFiles/")