import requests

URL = "http://localhost:8080/counter/areas"

params = {"point1": {"x": 221, "y": 300}}, "point2": {"x": 400, "y": 200}, "refResolution": {"w": 640, "h": 360},"Direction": "bidirectional"}
r = requests.post(URL, data=params)
