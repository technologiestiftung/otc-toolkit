"""
Creates a CSV file for evaluation of ODC countings.

1. Reads counter history from exported counter JSON
2. Reduces JSON to time frame of corresponding mp4 recording, since ODC recording starts earlier and stops later
3. Adds columns for manual evaluation
"""

import argparse
import json
import pickle
import random
from glob import glob

import ffmpeg
import numpy as np
import pandas as pd
import pytz

from config import *
from helpers import build_file_path_for_countings, get_datetime_of_recording

utc = pytz.utc
import datetime

RESULTS = {}
LEFTOVERS = []

CLASSES = ["car", "person", "truck", "bicycle", "bus", "motorbike"]

FINAL_COLS = ["movie_file", "area", "direction", "ODC_car", "car", "ODC_person", "person", "ODC_truck", "truck",
              "ODC_bicycle",
              "bicycle", "ODC_bus", "bus", "ODC_motorbike", "motorbike"]

parser = argparse.ArgumentParser(description='Build file for evaluation of ODC counts')
parser.add_argument('-d', '--delay', type=int, default=250,
                    help='number of milliseconds to add as delay to ODC records')
parser.add_argument('--station', type=str, required=True, choices=STATIONS,
                    help='one of our two stations')
parser.add_argument('--board', type=str, required=True, choices=BOARDS,
                    help='type of board')
args = parser.parse_args()


def load_counter_history(file_path):
    data = json.load(open(file_path))
    try:
        df = pd.DataFrame(data["counterHistory"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["timestamp"] = df["timestamp"] + datetime.timedelta(milliseconds=args.delay)

        return df
    except KeyError:
        return None


def count_objects_for_reduced_timeframe(start_time, end_time, counter_df, area, counting_direction=None):
    df = counter_df[counter_df["area"] == area]
    if counting_direction is not None:
        df = df[df["countingDirection"] == counting_direction]
    else:
        df = df.copy()

    df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]
    values = df.name.value_counts().keys().tolist()
    counts = df.name.value_counts().tolist()
    value_dict = dict(zip(values, counts))
    return value_dict


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
    global LEFTOVERS
    video_file = glob(join(r, "*.mp4"))[0]  # there is always only one mp4 file per directory
    duration_milliseconds = np.float(ffmpeg.probe(video_file)['format']['duration']) * 1000
    counter_file = glob(join(r, "*_counter.json"))[0]
    # counter_file = join(PATH_TO_RECORDINGS, "2020-08-20-16-31-20-174967",
    #                  "2020-08-20-16-31-20-174967_counter.json")
    counter_history = load_counter_history(counter_file)
    if counter_history is not None:
        directions = counter_history["countingDirection"].unique()
        areas = counter_history["area"].unique()
        recording_date = r.split("/")[-1]
        ffmpeg_start_time = get_datetime_of_recording(recording_date)
        for a in areas:
            for d in directions:
                object_counts = count_objects_for_reduced_timeframe(start_time=ffmpeg_start_time,
                                                                    end_time=ffmpeg_start_time + datetime.timedelta(
                                                                        milliseconds=duration_milliseconds),
                                                                    counter_df=counter_history, area=a,
                                                                    counting_direction=d)
                RESULTS[video_file] = {**RESULTS.get(video_file, {}), **{a + '+' + d: object_counts}}
    else:
        LEFTOVERS.append(r)


def sample_recordings(r, factor=3):
    random.seed(30)
    length = len(r) // factor
    return random.sample(r, length)


if __name__ == "__main__":

    recordings = glob(join(PATH_TO_RECORDINGS, args.station, args.board, "*"))
    """random sampling of data"""
    recordings = sample_recordings(recordings, factor=2)  # for citylab tx2 we have less data

    for rec in recordings:
        main(rec)
    RESULTS = pd.DataFrame.from_dict({(i, j): RESULTS[i][j]
                                      for i in RESULTS.keys()
                                      for j in RESULTS[i].keys()},
                                     orient='index')
    RESULTS.reset_index(inplace=True)
    RESULTS = postproces_odc_counting_cols(RESULTS)
    RESULTS[['area', 'direction']] = RESULTS["direction"].str.split("+", expand=True, )
    RESULTS = add_eval_cols(RESULTS)
    file = build_file_path_for_countings(args.station, args.board)
    RESULTS[FINAL_COLS].to_csv(file, index=False)
    with open(file.replace('.csv', 'leftovers.pkl'), 'wb') as f:
        pickle.dump(LEFTOVERS, f)
