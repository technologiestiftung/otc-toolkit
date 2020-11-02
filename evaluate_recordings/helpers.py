import datetime
import os
import zipfile
from os.path import join

import ffmpeg
import pandas as pd
import pytz

utc = pytz.utc
from datetime import datetime as dt


def split_video_into_images(rec_dir, video_file):
    # needed for drawing of boxes
    ffmpeg_split_cmd = "ffmpeg -skip_frame nokey -i " + video_file + " -vsync 0 -frame_pts true -r 1000 " + rec_dir + "/" + "%d.png"
    print(ffmpeg_split_cmd)
    os.system(ffmpeg_split_cmd)


def extract_sample_frames_from_video(video_file, path_for_images):
    try:
        (ffmpeg.input(video_file)
         .filter('fps', fps=2)
         .output(join(path_for_images, '%d.png'),
                 video_bitrate='5000k',
                 sws_flags='bilinear',
                 start_number=0)
         .run(capture_stdout=True, capture_stderr=True))
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))


def build_file_path_for_countings(station, board):
    return '_'.join(['ODC_counts', station, board, '.csv'])


def get_datetime_of_recording(r):
    """Every recording folder is a string representing the recording time on a board, which is two hours behind.
    Convert it to the correct datetime object.
    """
    # 'data/ecdf/xavier/2020-10-25-03-01-19-232469
    clock_change = dt(*tuple(int(x) for x in "2020-10-25-03-00-00-000001".split("-")), tzinfo=utc)
    ts = dt(*tuple(int(x) for x in r.split("-")), tzinfo=utc)
    if ts < clock_change:
        return ts + datetime.timedelta(hours=-2)
    else:
        return ts + datetime.timedelta(hours=-1)


def find_elem_with_closest_ts(df, video_start, time_diff_tolerance=200):
    """Find index of row whose timestamp is closest to video_start. Expects a DataFrame df with a column
    'timestamp'."""
    s = abs(df["timestamp"] - video_start)
    minimal_time_diff = (df.loc[s.idxmin(), "timestamp"] - video_start)
    minimal_time_diff = int(round(minimal_time_diff.total_seconds() * 1e3))
    # print(f"minimal time difference between dataframe time and image time: {minimal_time_diff}")
    if time_diff_tolerance:
        if minimal_time_diff < time_diff_tolerance:
            return s.idxmin()
        else:
            return None
    else:
        return s.idxmin()


def extract_recording(s, b):
    csv_file_path = build_file_path_for_countings(s, b)
    return pd.read_csv(csv_file_path)


def extract_subpaths_from_video_path(v):
    dirs = v.split("/")  # wouldn't work on Windows
    rec_dir = "/".join(dirs[:-1])
    video_file = dirs[-1]
    rec_date = video_file.replace(".mp4", "")
    return rec_dir, rec_date, video_file


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def zipit(dir_list, zip_name):
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for dir in dir_list:
        zipdir(dir, zipf)
    zipf.close()
