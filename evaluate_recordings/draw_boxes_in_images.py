import os

import pytz

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


def find_elem_with_closest_ts(json_df, video_start):
    """Find index of row whose timestamp is closest to the video starting time"""
    s = abs(json_df["timestamp"] - video_start)
    return s.idxmin()


def reduce_tracker_json(json_df, start_time, number_images):
    start_index = find_elem_with_closest_ts(json_df, start_time)
    stop_index = start_index + number_images
    return json_df.loc[start_index:stop_index].reset_index()


def merge(json_df, image_file_names):
    return dict(zip(image_file_names, json_df["objects"]))


def draw_bounding_box(image_name, image_to_objects):
    # Set bounding boxes path to same directory as images.
    detects = [item for item in image_to_objects[image_name] if item['name'] in TO_DETECT]
    source_img = Image.open(image_name)
    draw = ImageDraw.Draw(source_img)
    for item in detects:
        x = item["x"]
        y = item["y"]
        w = item["w"]
        h = item["h"]
        name = item["name"]
        draw.rectangle(((x - w / 2, y - h / 2), (x + w / 2, y + h / 2)), fill=None, outline="red")
        draw.text((x - w / 2, y - h / 2), name, font=ImageFont.truetype('Pillow/Tests/fonts/Arial.ttf'),
                  fill="red")
    source_img.save(image_name.replace(".png", "_boxes.png"))


recordings = [item.split("/")[1] for item in glob(join(PATH_TO_RECORDINGS, "**"))]
print(recordings)


def delete_images_with_bounding_box(path_to_dir):
    files = glob(join(path_to_dir, "*_boxes.png"))
    print(files)
    for f in files:
        os.remove(f)


if __name__ == '__main__':
    for rec in recordings:
        print(f"recording: {rec}")
        delete_images_with_bounding_box(join(PATH_TO_RECORDINGS, rec))

        images = glob(join(PATH_TO_RECORDINGS, rec, "*.png"))
        images = sorted(images)
        # print(images)

        ffmpeg_start_time = dt(*tuple(int(x) for x in rec.split("-")), tzinfo=utc) + datetime.timedelta(hours=-2)

        tracker_data = pd.read_json(join(PATH_TO_RECORDINGS, rec, rec + "_tracker.json"))

        """use below if you want to to join on frames instead of timestamps"""
        #########
        tracker_data.drop_duplicates(subset=["frameId"], inplace=True, ignore_index=True)
        #########
        tracker_data = reduce_tracker_json(tracker_data, ffmpeg_start_time, len(images))

        merged = merge(tracker_data, images)
        print(len(merged))
        print(merged.items())

        for i in images:
            draw_bounding_box(i, merged)
