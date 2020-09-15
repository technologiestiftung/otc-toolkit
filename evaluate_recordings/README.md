
1. Run first the following to fetch weather data for ECDF. Already done for citylab.

```bash
python fetch_weather_data.py --start 2020-08-01 --station ecdf
```

2. Create a directory `data`. Within `data`, create subdirectories `<station>/<board>`, e.g. `ecdf/nano`.
3. For every combination of `station` and ``board` run

```bash
python count_objects_in_video.py --station <station> --board <board>
```
This will create CSV files with counts of objects per class in the top directory. These files need to be edited by
adding manual counts.

4. For every combination of `station` and ``board` run

```bash
python add_weather_info.py --station <station> --board <board>
```

This will add columns with weather information to the corresponding CSV file created in the previous step. The weather
data are obtained from an API providing historical weather data from a nearby station. This information should be checked
manually.

5. For every combination of `station` and ``board` run

```bash
python estimate_luminosity.py --station <station> --board <board>
```

This will add a column with estimated video luminosity to the corresponding CSV file.

6. TODO: Run script that draws counting lines into videos