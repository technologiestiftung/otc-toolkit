import argparse

import cv2
import pandas as pd

from config import STATIONS, BOARDS, COUNTER_LINE_COORDS
from helpers import build_file_path_for_countings

parser = argparse.ArgumentParser(description='Run video listed in a CSV file and draw a line in it')
parser.add_argument('-r', '--row', type=int, required=True,
                    help='row number of CSV file')
parser.add_argument('--station', type=str, required=True, choices=STATIONS,
                    help='one of our two stations')
parser.add_argument('--board', type=str, required=True, choices=BOARDS,
                    help='type of board')
args = parser.parse_args()

"""Run e.g.
python draw_counter_lines_in-video.py --board tx2 --station citylab --row 3
"""


def extract_recording(s, b):
    csv_file_path = build_file_path_for_countings(s, b)
    return pd.read_csv(csv_file_path)


if __name__ == '__main__':

    df = extract_recording(args.station, args.board)
    path_to_video = df[df["row_number"] == args.row]['movie_file'].values[0]
    print(path_to_video)
    vc = cv2.VideoCapture(path_to_video)
    if args.station == "citylab" and args.board == "tx2":
        scaling_factor_x = 640 / 1440
        scaling_factor_y = 360 / 815
        line_location = COUNTER_LINE_COORDS[args.station]
        pt1 = (
            int(line_location["point1"]["x"] * scaling_factor_x), int(line_location["point1"]["y"] * scaling_factor_y))
        pt2 = (
            int(line_location["point2"]["x"] * scaling_factor_x), int(line_location["point2"]["y"] * scaling_factor_y))
    else:  # TODO implement for ECDF once we see the data
        scaling_factor_x = 640 / 1440
        scaling_factor_y = 360 / 815
        line_direction = df.loc[args.row, 'direction']  # it seems that I don't need it
        line_area = df.loc[args.row, 'area']
        line_location = COUNTER_LINE_COORDS[args.station][args.board][line_area]["location"]
        print(line_location)

        pt1 = (
            int(line_location["point1"]["x"] * scaling_factor_x), int(line_location["point1"]["y"] * scaling_factor_y))
        pt2 = (
            int(line_location["point2"]["x"] * scaling_factor_x), int(line_location["point2"]["y"] * scaling_factor_y))
        # path_to_counter_file = path_to_video.replace('.mp4', '_counter.json')
        print(pt1, pt2)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if cv2.waitKey(1) and key == 27:

            # exit on ESC
            break
        else:
            cv2.line(img=frame, pt1=pt1, pt2=pt2, color=(255, 0, 0), thickness=3, lineType=8, shift=0)

    vc.release()
    # cv2.destroyWindow("preview")
