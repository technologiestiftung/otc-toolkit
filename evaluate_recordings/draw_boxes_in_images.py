"""
1. Splits all videos in subdirectories of <PATH_TO_RECORDINGS> into images with timestamps (TODO)
2. For each image, finds the ODC tracking event with closest timestamp
3. TODO
"""
import os

import pytz

from helpers import find_elem_with_closest_ts

utc = pytz.utc

from config import PATH_TO_RECORDINGS

import pandas as pd
from PIL import Image, ImageFont, ImageDraw
from os.path import join

from datetime import datetime as dt
import datetime
import pytz

utc = pytz.utc
from glob import glob

TO_DETECT = ['car', 'traffic light', 'person']


def draw_bounding_box(image_name, bounding_box_dimensions):
    source_img = Image.open(image_name)
    draw = ImageDraw.Draw(source_img)
    # print("image : ", image_name)

    bounding_boxes = [item for item in bounding_box_dimensions if item['name'] in TO_DETECT]
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


def delete_images_with_bounding_box(path_to_dir):
    """Delete old images with bounding boxes"""
    files = glob(join(path_to_dir, "*_boxes.png"))
    for f in files:
        os.remove(f)


def extract_timestamp_from_file_name(image_file_name, video_start):
    image_file_name = image_file_name.split("/")[-1]
    milisec = int(image_file_name.replace("out", "").replace(".png", ""))  # TODO: too hacky, replace this
    image_time = video_start + datetime.timedelta(milliseconds=milisec + 250)  # TODO 200 is an artificial delay
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
    recordings = [item.split("/")[1] for item in glob(join(PATH_TO_RECORDINGS, "**"))]
    print(recordings)

    for rec in recordings:
        print(f"recording: {rec}")
        try:
            delete_images_with_bounding_box(join(PATH_TO_RECORDINGS, rec))

            ffmpeg_start_time = dt(*tuple(int(x) for x in rec.split("-")), tzinfo=utc) + datetime.timedelta(hours=-2)

            images = glob(join(PATH_TO_RECORDINGS, rec, "*.png"))
            images = sorted(images)
            image_to_rectime = dict(
                zip(images, [extract_timestamp_from_file_name(i, ffmpeg_start_time) for i in images]))

            tracker_data = pd.read_json(join(PATH_TO_RECORDINGS, rec, rec + "_tracker.json"))

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
