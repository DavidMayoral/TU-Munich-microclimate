'''
DWD - Deutsche Wetterdienst - German Weather Service

Data naming:
    Mean: produkt_ff_stunde_<StartDate:YYYYMMDD>_<EndDate:YYYYMMDD>_<LocationID>.txt
    Gust: produkt_zehn_min_fx_<StartDate:YYYYMMDD>_<EndDate:YYYYMMDD>_<LocationID>.txt

LocationID:
    City: 033379
    Airport: 01262
'''

dwd_data_info = {
    # City -> with identifier at end: 03379
    # Mean
    # From 01.01.1985 to 31.12.2022
    "CityMean":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/historical/stundenwerte_FF_03379_19850101_20221231_hist.zip",
        "file_name": "produkt_ff_stunde_19850101_20221231_03379.txt"
    },
    # Gust
    # From 12.07.1997 to 31.12.1999
    "CityGust1":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_19970712_19991231_hist.zip",
        "file_name": "produkt_zehn_min_fx_19970712_19991231_03379.txt"
    },
    # From 01.01.2000 to 31.12.2009
    "CityGust2":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_20000101_20091231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20000101_20091231_03379.txt"
    },
    # From 01.01.2010 to 31.12.2019
    "CityGust3":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_20100101_20191231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20100101_20191231_03379.txt"
    },
    # From 01.01.2010 to 31.12.2022
    "CityGust4":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_20200101_20221231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20200101_20221231_03379.txt"
    },
    # Airport -> with identifier at end: 01262
    # Mean
    # From 19.05.1992 to 31.12.2022
    "AirpMean":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/historical/stundenwerte_FF_01262_19920519_20221231_hist.zip",
        "file_name": "produkt_ff_stunde_19920519_20221231_01262.txt"
    },
    # Gust
    # From 20.05.1992 to 31.12.1999
    "AirpGust1":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_19920520_19991231_hist.zip",
        "file_name": "produkt_zehn_min_fx_19920520_19991231_01262.txt"
    },
    # From 01.01.2000 to 31.12.2009
    "AirpGust2":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_20000101_20091231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20000101_20091231_01262.txt"
    },
    # From 01.01.2010 to 31.12.2019
    "AirpGust3":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_20100101_20191231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20100101_20191231_01262.txt"
    },
    # From 01.01.2020 to 31.12.2022
    "AirpGust4":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_20200101_20221231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20200101_20221231_01262.txt"
    }
}