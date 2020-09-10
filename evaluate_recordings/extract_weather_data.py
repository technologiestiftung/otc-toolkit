import requests

folder = "2020-04-21-15-31-14-753487"  # TODO: later make this an argument for the script

URL = "https://api.brightsky.dev/weather"

LAT = 52  # TODO: replace by correct values for ecdf; add somewhere alsy citylab lat/lon;  later give an argument to sistinguish between ecdf and citylab
LON = 7.6


def extract_date(f):
    # e.g. 2020-08-11 from 2020-08-11-15-31-14-753487
    return f[:10]

def extract_hour():
    pass


def make_request(lat, lon, date):
    params = {"lat": lat, "lon": lon, "date": date}
    r = requests.get(URL, params=params)
    return r.json()


if __name__ == '__main__':
    date = extract_date(folder)
    print(date)
    print(make_request(LAT, LON, date))
