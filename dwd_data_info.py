'''
DWD - Deutsche Wetterdienst - German Weather Service

Information:
    Hourly:
        https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/

        EN: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/DESCRIPTION_obsgermany_climate_hourly_wind_en.pdf
        
        DE: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/BESCHREIBUNG_obsgermany_climate_hourly_wind_de.pdf

        => from here of interest:
            F: wind speed m/s
            D: wind direction

    10-minutes:
        Mean wind:
            https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/
            
            EN: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/DESCRIPTION_obsgermany_climate_10min_wind_en.pdf
            
            DE: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/BESCHREIBUNG_obsgermany_climate_10min_wind_de.pdf

        => from here of interest:
            FF_10: "10-min mean" = mean wind speed during the previous 10 minutes

            DD_10: mean wind direction during the previous 10 minutes

        Extreme wind: 
            https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/
            
            EN: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/DESCRIPTION_obsgermany_climate_10min_extreme_wind_en.pdf
            
            DE: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/BESCHREIBUNG_obsgermany_climate_10min_extreme_wind_de.pdf
        
        => from here of interest:
            FX_10: "10-min max" = maximum of wind speed during the previous 10 minutes
            
            DX_10: wind direction of the maximum wind speed during the previous 10 minutes

        alternatively
            FMX_10 "3-s gut of 10 min" = mean 3-second maxima of the wind speed during the previous 10 minutes

Data naming:
    Hourly:
        specifier: "ff"
        in folder: /climate_environment/CDC/observations_germany/climate/hourly/wind/
        file format: produkt_ff_stunde_<StartDate:YYYYMMDD>_<EndDate:YYYYMMDD>_<LocationID>.txt
    
    10-minutes:
        Mean:
            specifier: "ff"
            in folder: /climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/
            file format: produkt_zehn_min_ff_<StartDate:YYYYMMDD>_<EndDate:YYYYMMDD>_<LocationID>.txt
       
        Extreme wind:
            specifier: "fx"
            in folder: /climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/
            file format: produkt_zehn_min_fx_<StartDate:YYYYMMDD>_<EndDate:YYYYMMDD>_<LocationID>.txt

LocationID:
    City: 033379
    Airport: 01262
    
'''

dwd_data_info = {
    # City -> with identifier at end: 03379
    # Hourly
    # From 01.01.1985 to 31.12.2022
    "CityHourlyMean":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/historical/stundenwerte_FF_03379_19850101_20221231_hist.zip",
        "file_name": "produkt_ff_stunde_19850101_20221231_03379.txt"
    },
    # 10-minutes mean
    # From 12.07.1997 to 31.12.1999
    "City10MinMean1":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_03379_19970712_19991231_hist.zip",
        "file_name": "produkt_zehn_min_ff_19970712_19991231_03379.txt"
    },
    # From 01.01.2000 to 31.12.2009
    "City10MinMean2":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_03379_20000101_20091231_hist.zip",
        "file_name": "produkt_zehn_min_ff_20000101_20091231_03379.txt"
    },
    # From 01.01.2010 to 31.12.2019
    "City10MinMean3":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_03379_20100101_20191231_hist.zip",
        "file_name": "produkt_zehn_min_ff_20100101_20191231_03379.txt"
    },
    # From 01.01.2010 to 31.12.2022
    "City10MinMean4":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_03379_20200101_20221231_hist.zip",
        "file_name": "produkt_zehn_min_ff_20200101_20221231_03379.txt"
    },
    # 10-minutes extreme
    # From 12.07.1997 to 31.12.1999
    "City10MinMax1":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_19970712_19991231_hist.zip",
        "file_name": "produkt_zehn_min_fx_19970712_19991231_03379.txt"
    },
    # From 01.01.2000 to 31.12.2009
    "City10MinMax2":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_20000101_20091231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20000101_20091231_03379.txt"
    },
    # From 01.01.2010 to 31.12.2019
    "City10MinMax3":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_20100101_20191231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20100101_20191231_03379.txt"
    },
    # From 01.01.2010 to 31.12.2022
    "City10MinMax4":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_03379_20200101_20221231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20200101_20221231_03379.txt"
    },
    # Airport -> with identifier at end: 01262
    # Hourly
    # From 19.05.1992 to 31.12.2022
    "AirpHourlyMean":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/historical/stundenwerte_FF_01262_19920519_20221231_hist.zip",
        "file_name": "produkt_ff_stunde_19920519_20221231_01262.txt"
    },
    # 10-minutes mean
    # From 20.05.1992 to 31.12.1999
    "Airp10MinMean1":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_01262_19920520_19991231_hist.zip",
        "file_name": "produkt_zehn_min_ff_19920520_19991231_01262.txt"
    },
    # From 01.01.2000 to 31.12.2009
    "Airp10MinMean2":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_01262_20000101_20091231_hist.zip",
        "file_name": "produkt_zehn_min_ff_20000101_20091231_01262.txt"
    },
    # From 01.01.2010 to 31.12.2019
    "Airp10MinMean3":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_01262_20100101_20191231_hist.zip",
        "file_name": "produkt_zehn_min_ff_20100101_20191231_01262.txt"
    },
    # From 01.01.2020 to 31.12.2022
    "Airp10MinMean4":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_01262_20200101_20221231_hist.zip",
        "file_name": "produkt_zehn_min_ff_20200101_20221231_01262.txt"
    },
    # 10-minutes extreme
    # From 20.05.1992 to 31.12.1999
    "Airp10MinMax1":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_19920520_19991231_hist.zip",
        "file_name": "produkt_zehn_min_fx_19920520_19991231_01262.txt"
    },
    # From 01.01.2000 to 31.12.2009
    "Airp10MinMax2":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_20000101_20091231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20000101_20091231_01262.txt"
    },
    # From 01.01.2010 to 31.12.2019
    "Airp10MinMax3":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_20100101_20191231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20100101_20191231_01262.txt"
    },
    # From 01.01.2020 to 31.12.2022
    "Airp10MinMax4":{
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_extrema_wind_01262_20200101_20221231_hist.zip",
        "file_name": "produkt_zehn_min_fx_20200101_20221231_01262.txt"
    }
}
