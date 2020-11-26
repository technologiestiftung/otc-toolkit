from os.path import dirname, abspath, join

DIR_PATH = dirname(abspath(__file__))
OTC_TOOLKIT_PATH = abspath(join(DIR_PATH, '..'))
PATH_TO_RECORDINGS = "data"
STATIONS = ['ecdf', 'citylab']
BOARDS = ['nano', 'tx2', 'xavier']

COUNTER_LINE_COORDS = {'ecdf':
                       # {'ecdf-lindner': {"point1": {"x": 718, "y": 173}, Coords from first run, bad lines
                       #                   "point2": {"x": 702, "y": 864}},
                       #  "cross": {"point1": {"x": 515, "y": 494},
                       #            "point2": {"x": 932, "y": 377}}},
                           {"bundesstrasse": {"point1": {"x": 1046, "y": 132}, "point2": {"x": 1211, "y": 226}},
                            "lindner": {"point1": {"x": 393, "y": 166}, "point2": {"x": 718, "y": 72}},
                            "walking_bundesstrasse": {"point1": {"x": 1104, "y": 200}, "point2": {"x": 975, "y": 258}},
                            "walking_lindner": {"point1": {"x": 568, "y": 150}, "point2": {"x": 642, "y": 235}}},
                       # 'citylab':
                       #     {"point1": {"x": 34, "y": 740}, "point2": {"x": 1433,
                       #                                                "y": 103}}
                       "citylab": {
                           "platzderluftbruecke": {"point1": {"x": 541, "y": 445}, "point2": {"x": 960, "y": 179}}}
                       }
# tx2: same line for both directions going across two lanes
CLASSES = ["car", "truck", "bicycle", "bus", "motorbike"]
# CLASSES = ["car", "truck", "person", "bus"]  # changed for second ecdf-recording

# COUNTER_LINE_NAMES = {
#     "ecdf": {"a4ad8491-c790-4078-9092-94ac1e3e0b46": "ecdf-lindner", "882e3178-408a-4e3e-884f-d8d2290b47f0": "cross"}}

COUNTER_LINE_NAMES = {"ecdf": {
    "c9f71c06-6baf-47c3-9ca2-4c26676b7336": "bundesstrasse",
    "6c393a8f-a84f-4e31-8670-bfeb9e1cfadc": "lindner",
    "240885bb-636e-41f2-8448-bfcdbabd42b5": "walking_bundesstrasse",
    "25b11f4a-0d23-4878-9050-5b5a06834adc": "walking_lindner"
},
    "citylab": {"a7317e7a-85da-4f08-8efc-4e90a2a2b2b8": "platzderluftbruecke"}
}
