from os.path import dirname, abspath, join

DIR_PATH = dirname(abspath(__file__))
OTC_TOOLKIT_PATH = abspath(join(DIR_PATH, '..'))
PATH_TO_RECORDINGS = "data"
STATIONS = ['ecdf', 'citylab']
BOARDS = ['nano', 'tx2', 'xavier']
