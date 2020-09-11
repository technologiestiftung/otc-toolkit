"""
Fetch weather data for specified ODC station, start and end date.
E.g. in order to fetch the data from the weather station closest to ECDF from September 1st until September 15th, run:
python fetch_weather_data.py --station ecdf --start 2020-09-01 --end 2020-09-15
Data is dumped to a JSON file and can be used later to match with ODC counts.
"""
import argparse
import datetime as dt
import json

import requests

# folder = "2020-04-21-15-31-14-753487"
from config import STATIONS

URL = "https://api.brightsky.dev/weather"

STATION_LAT_LON = {'ecdf': ('52.5184', '13.3807'), 'citylab': ('52.4837929', '13.3863135')}

parser = argparse.ArgumentParser(description='Extract historical weather data')
parser.add_argument('--start', type=str, default='2020-08-01',
                    help='start date as string of the form YYYY-MM-DD, e.g. 2020-08-17')
parser.add_argument('--end', type=str, default=dt.datetime.today().strftime('%Y-%m-%d'),
                    help='end date as string of the form YYYY-MM-DD, e.g. 2020-09-01')
parser.add_argument('--station', type=str, required=True, choices=STATIONS,
                    help='one of our two stations')

args = parser.parse_args()


# def extract_date(f):
#     # e.g. 2020-08-11 from 2020-08-11-15-31-14-753487
#     return f[:10]


# def extract_datetime(f):
#     date_time_obj = dt.datetime.strptime(f, '%Y-%m-%d-%H-%M-%S-%f')
#     return date_time_obj


def filter_weather_info(w):
    return {k: v for k, v in w.items() if k in ['timestamp', 'condition', 'icon']}


def filter_station_info(w):
    return {k: v for k, v in w.items() if k in ['lat', 'lon', 'station_name', 'distance']}


def make_request(lat, lon, date):
    params = {"lat": lat, "lon": lon, "date": date}
    r = requests.get(URL, params=params)
    r = r.json()
    weather = r["weather"]
    station = r["sources"]
    return [filter_weather_info(item) for item in weather], [filter_station_info(item) for item in station]


if __name__ == '__main__':
    weather_data = []
    start_date = dt.datetime.strptime(args.start, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(args.end, '%Y-%m-%d').date()
    LAT, LON = STATION_LAT_LON[args.station]
    d = start_date
    while d <= end_date:
        print(d)
        resp = make_request(LAT, LON, d)
        weather_data.extend(resp[0])
        if d == start_date:
            station_info = resp[1]

        d += dt.timedelta(days=1)

    dump_file = '_'.join(['weather_data', args.station, args.start, args.end, '.json'])
    with open(dump_file, 'w') as f:
        json.dump({'weather': weather_data, 'station': station_info}, f)
