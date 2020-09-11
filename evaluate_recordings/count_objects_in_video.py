"""
Creates a CSV file for evaluation of ODC countings.

1. Reads counter history from exported counter JSON
2. Reduces JSON to time frame of corresponding mp4 recording, since ODC recording starts earlier and stops later
3. Adds columns for manual evaluation
4. TODO: add columns for luminosity, day/night, weather
"""

# TODO: activate sampling later

import argparse
import json
from glob import glob

import ffmpeg
import numpy as np
import pandas as pd
import pytz

from config import *
from helpers import build_file_path_for_countings

utc = pytz.utc
from datetime import datetime as dt
import datetime

RESULTS = {}

CLASSES = ["car", "person", "truck", "bicycle", "bus", "motorbike"]

FINAL_COLS = ["movie_file", "direction", "ODC_car", "car", "ODC_person", "person", "ODC_truck", "truck", "ODC_bicycle",
              "bicycle", "ODC_bus", "bus", "ODC_motorbike", "motorbike"]

parser = argparse.ArgumentParser(description='Prepare file for evaluation of ODC counts')
parser.add_argument('-d', '--delay', type=int, default=250,
                    help='number of milliseconds to add as delay to ODC records')
parser.add_argument('--station', type=str, required=True, choices=STATIONS,
                    help='one of our two stations')
parser.add_argument('--board', type=str, required=True, choices=['nano', 'tx2', 'xavier'],
                    help='type of board')
args = parser.parse_args()


def load_counter_history(file_path):
    data = json.load(open(file_path))
    df = pd.DataFrame(data["counterHistory"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["timestamp"] = df["timestamp"] + datetime.timedelta(milliseconds=args.delay)
    return df


def count_objects_for_reduced_timeframe(start_time, end_time, counter_df, counting_direction=None):
    if counting_direction is not None:
        df = counter_df[counter_df["countingDirection"] == counting_direction]
    else:
        df = counter_df.copy()

    df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]
    return df.name.value_counts()


def postproces_odc_counting_cols(df):
    df = df.rename({"level_0": "movie_file", "level_1": "direction"}, axis="columns")
    df = df.fillna(value={c: 0 for c in CLASSES})
    for c in CLASSES:
        if c not in df.columns:
            df[c] = 0
        df[c] = df[c].astype(int)
    return df.rename({c: "ODC_" + c for c in CLASSES}, axis="columns")


def add_eval_cols(df):
    for c in CLASSES:
        df[c] = np.nan
    return df


def main(r):
    global RESULTS
    video_file = glob(join(r, "*.mp4"))[0]  # there is always only one mp4 file per directory
    duration_milliseconds = np.float(ffmpeg.probe(video_file)['format']['duration']) * 1000
    counter_file = glob(join(r, "*_counter.json"))[0]
    # counter_file = join(PATH_TO_RECORDINGS, "2020-08-20-16-31-20-174967",
    #                  "2020-08-20-16-31-20-174967_counter.json")
    counter_history = load_counter_history(counter_file)
    directions = counter_history["countingDirection"].unique()
    recording_date = r.split("/")[-1]
    ffmpeg_start_time = dt(*tuple(int(x) for x in recording_date.split("-")), tzinfo=utc) + datetime.timedelta(
        hours=-2)
    for d in directions:
        object_counts = count_objects_for_reduced_timeframe(start_time=ffmpeg_start_time,
                                                            end_time=ffmpeg_start_time + datetime.timedelta(
                                                                milliseconds=duration_milliseconds),
                                                            counter_df=counter_history, counting_direction=d)
        RESULTS[video_file] = {**RESULTS.get(video_file, {}), **{d: object_counts}}


if __name__ == "__main__":

    recordings = glob(join(PATH_TO_RECORDINGS, "*"))
    # sample_size = len(recordings) // 3
    # recordings = random.sample(recordings, sample_size)
    print(recordings)

    for rec in recordings:
        main(rec)

    RESULTS = pd.DataFrame.from_dict({(i, j): RESULTS[i][j]
                                      for i in RESULTS.keys()
                                      for j in RESULTS[i].keys()},
                                     orient='index')
    RESULTS.reset_index(inplace=True)

    RESULTS = postproces_odc_counting_cols(RESULTS)
    RESULTS = add_eval_cols(RESULTS)
    file = build_file_path_for_countings(args.station, args.board)
    RESULTS[FINAL_COLS].to_csv(file, index=False)
