"""
Reads a CSV file with ODC countings  and computes luminosity for every video.
"""
import argparse
import os
import shutil
from glob import glob
from os.path import join

import numpy as np
import pandas as pd
from PIL import Image

from config import STATIONS
from helpers import split_video_into_images, build_file_path_for_countings

parser = argparse.ArgumentParser(description='Estimate luminosity of videos and add to evaluation file')
parser.add_argument('--station', type=str, required=True, choices=STATIONS,
                    help='one of our two stations')
parser.add_argument('--board', type=str, required=True, choices=['nano', 'tx2', 'xavier'],
                    help='type of board')

args = parser.parse_args()


def calculate_brightness(img):
    # https://gist.github.com/kmohrf/8d4653536aaa88965a69a06b81bcb022#file-brightness-py
    greyscale_image = img.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale


def estimate_luminosity_of_video(rec):
    path = "tmp_images"
    os.mkdir(path)

    split_video_into_images(rec, path)

    total_brightness = []
    images = glob(join(path, "*.png"))
    for file in images:
        img = Image.open(file)
        brightness = calculate_brightness(img)
        total_brightness.append(brightness)
        # print("%s\t%s" % (file, brightness))
    video_brightness = np.mean(total_brightness)

    shutil.rmtree(path)
    return video_brightness


if __name__ == '__main__':
    file = build_file_path_for_countings(args.station, args.board)
    df = pd.read_csv(file)
    df["luminosity"] = df["movie_file"].map(estimate_luminosity_of_video)
    df["luminosity"] = df["luminosity"].map(lambda x: np.round(x, 4))
    df.to_csv(file, index=False)
