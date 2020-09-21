"""Compute number of tracked frames and total duration of ODC tracking using downloaded JSON files"""
from glob import glob
from os.path import join

import pytz

utc = pytz.utc
import pandas as pd

from config import PATH_TO_RECORDINGS

recordings = glob(join(PATH_TO_RECORDINGS, "*"))

print(recordings)

for r in recordings:
    tracker_file = glob(join(r, "*_tracker.json"))[0]
    print(f"path to JSON file: {tracker_file}")
    tracker_data = pd.read_json(tracker_file)
    # print(tracker_data.shape)
    print(f"number of rows tracker JSON: {len(tracker_data)}")
    print(f"number of distinct frames in tracker JSON: {tracker_data.frameId.nunique()}")

    frames = tracker_data.groupby("frameId").aggregate(list)
    frames.timestamp = frames.timestamp.map(lambda x: set(x))
    print(f"number of timestamps per frame: {frames.timestamp.map(lambda x: len(x)).value_counts()}")
    tracking_duration = tracker_data['timestamp'].max() - tracker_data['timestamp'].min()
    print(f"tracking duration: {tracking_duration}")
    print(f"number of rows per second: {len(tracker_data)/tracking_duration.total_seconds()}")
    print(f"number of distinct frames per second: {tracker_data.frameId.nunique()/tracking_duration.total_seconds()}")

    images = glob(join(r, "*.png"))
    print(f"number of images: {len(images)}")

    print("--------------------")
