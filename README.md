# TU Munich microclimate
In this repository I will record the relevant information regarding the wind climate conditions in Munich. The aim is to provide data supporting wind simulations for the TU Munich inner city campus.

## 1. Data extraction from the DWD Database
The Deutsche Wetterdienst (DWD) provides information on many weather parameters. 
[https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate)

Relevant for us is only the wind information (both mean and gust values).

`Code`\`00_data_extracting.ipynb`

## 2. Resolution of the wind data provided
All the data being currently recorded by the DWD follow the WMO guidelines, which help minimize the local effects. 

The records are accompanied by comprehensive station metadata.
### Mean wind speed
![Resolution of DWD data](https://github.com/DavidMayoral/TU-Munich-microclimate/blob/main/QualityofDWDdata.png)

- **10-minute log**
  - Mean wind speed and direction of the last 10 minutes. 
  - Quality:
  
- **Hourly log**
  - Average of the six 10-minute intervals measured during the previous hour
  - Quality: 


### Gust speed ("extreme winds")
The following information is provided in 10-minute time windows:
- Maximum (peak) wind speed and direction.
- Minimum wind speed.
- Maximum 10-minute average during the previous 10-minutes.

## 3. Detailed information about the weather stations

- **Munich city**
  - Location: 48.1632ᵒN 11.5429ᵒE (north-west sector of Munich, located at the DWD branch office in Munich)
  - Height: 29.28 m
  - Automatic wind information since: 07-1997

- **Munich airport**
  - Location: 48.3477ᵒN 11.8134ᵒE (east part of the airport, near to the threshold of runway 26L)
  - Height: 10 m
  - Automatic wind information since: 05-1992

## 4. Post-processing of raw data
`Code`\`01_postprocessing.py`

## 5. Plotting
The following plots can be found in the `Relevant graphs` folder:
- Average wind speeds per year.
- Average wind speeds per month.
- Wind roses (direction & wind intensity).

**Note**: The .html graphs have to be downloaded in order to be visualized correctly.
