from os.path import dirname, abspath, join

DIR_PATH = dirname(abspath(__file__))
OTC_TOOLKIT_PATH = abspath(join(DIR_PATH, '..'))
PATH_TO_RECORDINGS = "data"
STATIONS = ['ecdf', 'citylab']
BOARDS = ['nano', 'tx2', 'xavier']

COUNTER_LINE_COORDS = {'ecdf':
                           {'ecdf-lindner': {"point1": {"x": 718, "y": 173},
                                             "point2": {"x": 702, "y": 864}},  # yellow
                            "cross": {"point1": {"x": 515, "y": 494},
                                      "point2": {"x": 932, "y": 377}}},  # turquise
                       'citylab':
                           {"point1": {"x": 34, "y": 740}, "point2": {"x": 1433,
                                                                      "y": 103}}}  # tx2: same line for both directions going across two lanes
CLASSES = ["car", "truck", "bicycle", "bus", "motorbike"]
