import datetime
from os.path import join

import ffmpeg
import pytz

utc = pytz.utc
from datetime import datetime as dt


# def split_video_into_images(v):
# needed for drawing of boxes
#     # res = subprocess.check_output(["ffmpeg", "-skip_frame", "nokey", "-i", v, "-vsync", "0", "-frame_pts", "true", "-r", "1000", "out%d.png"])
#     # for line in res.splitlines():
#     bashCommand = "ffmpeg -skip_frame nokey -i " + v + " -vsync 0 -frame_pts true -r 1000 hw%d.png"
#     output = subprocess.check_output(['bash', '-c', bashCommand])

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
    return dt(*tuple(int(x) for x in r.split("-")), tzinfo=utc) + datetime.timedelta(hours=-2)


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
