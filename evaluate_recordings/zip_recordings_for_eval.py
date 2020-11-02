"""
Create a zip with all recording folders required for evaluation - instead of having to store all recordings"""
import argparse
import os
from glob import glob
from os.path import join
from shutil import copytree

import numpy as np
import pandas as pd
from PIL import Image

from config import STATIONS
from helpers import extract_sample_frames_from_video, zipit, build_file_path_for_countings


parser = argparse.ArgumentParser(description='Estimate luminosity of videos and add to evaluation file')
parser.add_argument('--station', type=str, required=True, choices=STATIONS,
                    help='one of our two stations')
parser.add_argument('--board', type=str, required=True, choices=['nano', 'tx2', 'xavier'],
                    help='type of board')

args = parser.parse_args()


if __name__ == '__main__':
    file = build_file_path_for_countings(args.station, args.board)
    df = pd.read_csv(file)
    eval_dirs = ["/".join(p.split("/")[:-1]) for p in df["movie_file"].unique()]
    zipit(eval_dirs, "eval_dirs.zip")
