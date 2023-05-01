# TU Munich microclimate
In this repository I will record the relevant information regarding the wind climate conditions in Munich. The aim is to provide data supporting wind simulations for the TU Munich inner city campus.

## 1. Data extraction from the DWD Database
The Deutsche Wetterdienst (DWD) provides information on many weather parameters. Relevant for us is only the wind information.
[https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate)


## 2. Resolution of the wind data provided
### Mean wind speed
![Resolution of DWD data](https://github.com/DavidMayoral/TU-Munich-microclimate/blob/main/QualityofDWDdata.png)

### Gust speed ("extreme winds")


## 3. Detailed information about the weather stations

- **Munich city**
  - Location: 48.1632ᵒN 11.5429ᵒE (north-west sector of Munich, located at the DWD branch office in Munich)
  - Height: 29.28 m
  - Automatic wind information since: 07-1997

- **Munich airport**
  - Location: 48.3477ᵒN 11.8134ᵒE (east part of the airport, near to the threshold of runway 26L )
  - Height: 10 m
  - Automatic wind information since: 05-1992

## 4. Post-processing of raw data
`postprocessing.py`


## 5. Plotting
`plotting.py`
