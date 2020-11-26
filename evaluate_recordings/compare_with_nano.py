"""Compares the counts from TX2 and Nano or Xavier and Nano"""
import json
from glob import glob
from os.path import join

import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from config import PATH_TO_RECORDINGS


def load_counter_history(file_path):
    print(file_path)
    file_path = join(file_path, file_path.split("/")[-1] + "_counter.json")
    data = json.load(open(file_path))
    start_datetime = pd.to_datetime(data["dateStart"])
    end_datetime = pd.to_datetime(data["dateEnd"])
    print("start: ", start_datetime)
    print("stop: ", end_datetime)
    cols = ['timestamp', 'name','area', 'countingDirection']
    try:
        df = pd.DataFrame(data["counterHistory"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        # df["timestamp"] = df["timestamp"] + datetime.timedelta(milliseconds=args.delay)

        return df[cols], start_datetime, end_datetime
    except KeyError:
        return pd.DataFrame(columns=cols), start_datetime, end_datetime


def compare_time_range(r1, r2):
    counter_1, start_dt_1, stop_dt_1 = load_counter_history(r1)
    counter_2, start_dt_2, stop_dt_2 = load_counter_history(r2)
    max_start_dt = max(start_dt_1, start_dt_2)
    min_stop_dt = min(stop_dt_1, stop_dt_2)
    print(min_stop_dt-max_start_dt)
    try:
        return counter_1[(counter_1["timestamp"] >= max_start_dt) & (counter_1["timestamp"] <= min_stop_dt)], counter_2[
            (counter_2["timestamp"] >= max_start_dt) & (counter_2["timestamp"] <= min_stop_dt)]
    except:
        cols = ['timestamp', 'name','area', 'countingDirection']
        return pd.DataFrame(columns=cols), pd.DataFrame(columns=cols)


if __name__ == "__main__":
    recordings = glob(join(PATH_TO_RECORDINGS, "citylab", "tx2-august", "*"))
    # TODO: check the geometry of the counter lines between Nano and TX2 --> are they comparable


    for r in recordings[:5]:
        #print(r)

        dirs = r.split("-")  # wouldn't work on Windows
        nano_dir = "-".join(dirs[:-2]).replace("tx2-august", "nano")
        # print(glob(nano_dir + "-*"))
        nano_dir = glob(nano_dir + "-*")[0]
        #print(nano_dir)

        c1, c2 = compare_time_range(r, nano_dir)

        print(c1.sort_values(by="timestamp"))
        print(len(c1))
        print(c2.sort_values(by="timestamp"))
        print(len(c2))
