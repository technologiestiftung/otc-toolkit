## Prepare recordings

1. Create directory `data` in this directory; create for each station and each board type a subdirectory, e.g. `citylab/tx2`.
2. Copy all zip files from the SSDs to the respective subdirectories
3. Unzip the folders into subfolders with the same naming convention as the original ones:

```bash
for file in *.zip; do unzip "${file}" -d "${file:0:26}"; done
```
4. Check recordings and remove those that are not useful for evaluation; Remove all zip-files

## Prepare a CSV file for evaluation


1. Run first the following to fetch weather data for ECDF (and citylab).

```bash
python fetch_weather_data.py --start 2020-08-01 --station ecdf
```

2. Create a directory `data`. Within `data`, create subdirectories `<station>/<board>`, e.g. `ecdf/nano`.
3. For every combination of `station` and `board` (ignore `nano` for now) run

```bash
python count_objects_in_video.py --station <station> --board <board>
```

This will create CSV files with counts of objects per class in the top directory. These files need to be edited by
adding manual counts.

4. For every combination of `station` and `board` (ignore `nano` for now) run

```bash
python add_weather_info.py --station <station> --board <board>
```

This will add columns with weather information to the corresponding CSV file created in the previous step. The weather
data are obtained from an API providing historical weather data from a nearby station. This information should be checked
manually.

5. For every combination of `station` and ``board` (ignore `nano` for now) run

```bash
python estimate_luminosity.py --station <station> --board <board>
```

This will add a column with estimated video luminosity to the corresponding CSV file.

## Manual evaluation

1. open the CSV file in an editor of your choice. Add an additional column at the end for remarks.
Note that a row in the CSV file represents the counts across one line
with a specified direction (could also be bi-directional) in a single recording. Make sure you have checked the
direction in which the cars are counted before you start evaluating.

2. In order to open the video for a given row number `r` in the CSV file, run the following script:

```bash
python draw_counter_lines_in_video.py --station <station> --board <board> --row r
```

E.g.

```
python draw_counter_lines_in_video.py --station citylab --board tx2 --row 3
```

will open the video displaying the scenery of row 3.

3. Make sure you check the values in the weather columns `weather_condition`, `weather_category`, `day_or_night`.
These need to be either approved or completed if missing.

Run script that draws counting lines into videos
