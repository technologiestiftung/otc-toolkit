"""
1. Splits all videos in subdirectories of <PATH_TO_RECORDINGS> into images with timestamps (TODO)
2. For each image, finds the ODC tracking event with closest timestamp
3. TODO
"""
import argparse
import datetime
import os
from datetime import datetime as dt
from os.path import join

import pandas as pd
import pytz
from PIL import Image, ImageFont, ImageDraw

from config import CLASSES
from helpers import find_elem_with_closest_ts, extract_recording, extract_subpaths_from_video_path, \
    split_video_into_images

utc = pytz.utc
from glob import glob

from config import STATIONS, BOARDS

parser = argparse.ArgumentParser(description='Run video listed in a CSV file and draw a line in it')
parser.add_argument('-r', '--row', type=int, required=True,
                    help='row number of CSV file')
parser.add_argument('--station', type=str, required=True, choices=STATIONS,
                    help='one of our two stations')
parser.add_argument('--board', type=str, required=True, choices=BOARDS,
                    help='type of board')
parser.add_argument('--play_delay', type=int, required=False, default=1,
                    help='delay the video')
parser.add_argument('-d', '--delay', type=int, default=250,
                    help='number of milliseconds to add as delay to ODC records')
args = parser.parse_args()


def draw_bounding_box(image_name, bounding_box_dimensions):
    source_img = Image.open(image_name)
    draw = ImageDraw.Draw(source_img)
    # print("image : ", image_name)

    bounding_boxes = [item for item in bounding_box_dimensions if item['name'] in CLASSES]
    # print(bounding_boxes)
    for item in bounding_boxes:
        x = item["x"]
        y = item["y"]
        w = item["w"]
        h = item["h"]
        name = item["name"]
        # print("coords: ", x, y, w, h, name)
        draw.rectangle(((x - w / 2, y - h / 2), (x + w / 2, y + h / 2)), fill=None, outline="red")
        draw.text((x - w / 2, y - h / 2), name, font=ImageFont.truetype('Pillow/Tests/fonts/Arial.ttf'),
                  fill="red")
    source_img.save(image_name.replace(".png", "_boxes.png"))


def delete_images(path_to_dir, with_bounding_box_only=True):
    """Delete old images with bounding boxes"""
    if with_bounding_box_only:
        files = glob(join(path_to_dir, "*_boxes.png"))
    else:
        files = glob(join(path_to_dir, "*.png"))
    for f in files:
        os.remove(f)


def extract_timestamp_from_file_name(image_file_name, video_start):
    image_file_name = image_file_name.split("/")[-1]
    milisec = int(image_file_name.replace(".png", ""))  # image file name are the miliseconds elapsed since video start
    image_time = video_start + datetime.timedelta(milliseconds=milisec + args.delay)
    return image_time


def assign_tracking_to_image_via_rec_time(images_with_time, json_df):
    result = {}
    for im, t in images_with_time.items():
        print(im, t)
        json_df_idx = find_elem_with_closest_ts(json_df, t)
        print(json_df_idx)
        if json_df_idx is not None:
            result[im] = json_df.loc[json_df_idx, "objects"]
        else:
            print(f"no close tracker entry found for this image: {im}")
    return result


if __name__ == '__main__':
    df = extract_recording(args.station, args.board)
    path_to_video = df[df["row_number"] == args.row]['movie_file'].values[0]
    print(path_to_video)
    rec_dir, rec_date, video_file = extract_subpaths_from_video_path(path_to_video)
    try:
        delete_images(rec_dir, with_bounding_box_only=False) # delete all PNGs to save storage; otherwise next line should not be executed more than once
        split_video_into_images(rec_dir, path_to_video)

        ffmpeg_start_time = dt(*tuple(int(x) for x in rec_date.split("-")), tzinfo=utc) + datetime.timedelta(hours=-2)
        images = glob(join(rec_dir, "*.png"))
        image_to_rectime = dict(
            zip(images, [extract_timestamp_from_file_name(i, ffmpeg_start_time) for i in images]))
        tracker_data = pd.read_json(join(rec_dir, rec_date + "_tracker.json"))

        """use below if you want to to join on frames instead of timestamps"""
        #########
        # tracker_data.drop_duplicates(subset=["frameId"], inplace=True, ignore_index=True)
        #########

        # tracker_data = reduce_tracker_json(tracker_data, ffmpeg_start_time, len(images))
        # print(f"number of images: {len(images)}")
        # print(f"JSON entries: {len(tracker_data)}")

        # merged = merge(tracker_data, images)
        merged = assign_tracking_to_image_via_rec_time(image_to_rectime, tracker_data)
        print(len(merged))
        # print(merged.items())
        #
        for i, obj in merged.items():
            # print(i)
            try:
                draw_bounding_box(i, obj)
            except:
                print(f"image not found: {i}")

    except:
        print("did not work")
