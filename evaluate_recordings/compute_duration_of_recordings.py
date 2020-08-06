"""Compute number of tracked frames and total duration of ODC tracking using downloaded JSON files"""
from glob import glob
from os.path import join

import pytz

utc = pytz.utc
import pandas as pd

from config import PATH_TO_RECORDINGS

tracker_data_files = glob(join(PATH_TO_RECORDINGS, "**/*_tracker.json"))

# print(tracker_data_files)

for f in tracker_data_files:
    print(f"path to JSON file: {f}")
    tracker_data = pd.read_json(f)
    # print(tracker_data.shape)
    print(f"number of rows tracker JSON: {len(tracker_data)}")
    print(f"number of distinct frames in tracker JSON: {tracker_data.frameId.nunique()}")

    frames = tracker_data.groupby("frameId").aggregate(list)
    frames.timestamp = frames.timestamp.map(lambda x: set(x))
    print(f"number of timestamps per frame: {frames.timestamp.map(lambda x: len(x)).value_counts()}")

    print(f"tracking duration: {tracker_data['timestamp'].max() - tracker_data['timestamp'].min()}")
