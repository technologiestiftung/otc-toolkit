import argparse

import pandas as pd

from config import STATIONS
from helpers import build_file_path_for_countings, get_datetime_of_recording, find_elem_with_closest_ts

parser = argparse.ArgumentParser(description='Estimate luminosity of videos and add to evaluation file')
parser.add_argument('--station', type=str, required=True, choices=STATIONS,
                    help='one of our two stations')
parser.add_argument('--board', type=str, required=True, choices=['nano', 'tx2', 'xavier'],
                    help='type of board')

args = parser.parse_args()
WEATHER_DATA = pd.read_json('_'.join(['weather_data', args.station, '.json']))


def extract_weather_info(v):
    global WEATHER_DATA
    rec_date = get_datetime_of_recording(v.split("/")[-2])
    print(rec_date)
    idx = find_elem_with_closest_ts(df=WEATHER_DATA, video_start=rec_date, time_diff_tolerance=None)
    row = WEATHER_DATA.loc[idx]
    print(row)
    day_or_night = row["icon"].split('-')[-1]
    weather_category = row["icon"].replace(day_or_night, '').rstrip('-')
    return row["condition"], weather_category, day_or_night


if __name__ == '__main__':
    file = build_file_path_for_countings(args.station, args.board)
    df = pd.read_csv(file)
    df["weather_condition"], df["weather_category"], df["day_or_night"] = \
        zip(*df["movie_file"].map(lambda x: extract_weather_info(x)))
    df.to_csv(file, index=False)
