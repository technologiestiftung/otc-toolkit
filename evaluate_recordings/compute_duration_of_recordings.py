"""Compute number of tracked frames and total duration of ODC tracking using downloaded JSON files"""
from glob import glob
from os.path import join

import pandas as pd

from config import PATH_TO_RECORDINGS

tracker_data_files = glob(join(PATH_TO_RECORDINGS, "**/*_tracker.json"))

# print(tracker_data_files)

for f in tracker_data_files:
    print(f"path to JSON file: {f}")
    tracker_data = pd.read_json(f)
    print(f"number of frames in tracker JSON: {len(tracker_data)}")
    print(f"tracking duration: {tracker_data['timestamp'].max() - tracker_data['timestamp'].min()}")
