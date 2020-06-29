import requests

URL = "http://localhost:8080/counter/areas"
params = 
{
        "countingAreas": {
          "5287124a-4598-44e7-abaf-394018a7278b": {
            "color": "yellow",
            "location": {
              "point1": {
                "x": 221,
                "y": 588
              },
              "point2": {
                "x": 673,
                "y": 546
              },
              "refResolution": {
                "w": 1280,
                "h": 666
              }
            },
            "name": "Counter line 1",
            "type": "bidirectional"
          }
        }
      }

#params = {"point1": {"x": 221, "y": 300}}, "point2": {"x": 400, "y": 200}, "refResolution": {"w": 640, "h": 360},"Direction": "bidirectional"}
r = requests.post(URL, data=params)
