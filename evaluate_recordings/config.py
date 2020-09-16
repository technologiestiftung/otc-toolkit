from os.path import dirname, abspath, join

DIR_PATH = dirname(abspath(__file__))
OTC_TOOLKIT_PATH = abspath(join(DIR_PATH, '..'))
PATH_TO_RECORDINGS = "data"
STATIONS = ['ecdf', 'citylab']
BOARDS = ['nano', 'tx2', 'xavier']

COUNTER_LINE_COORDS = {'ecdf':
                           {'nano': {'dir1': (), 'dir2': ()}, 'xavier': {'dir1': (), 'dir2': ()}},
                       'citylab':
                           {"point1": {"x": 34, "y": 740}, "point2": {"x": 1433,
                                                                      "y": 103}}}  # tx2: same line for both directions going across two lanes
