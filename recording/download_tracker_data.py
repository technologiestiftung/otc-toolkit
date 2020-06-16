import requests
import json
import os
from glob import glob

os.chdir("/home/otc-xavier/otc-toolkit/recording")
# Get _id of the last recording
recordings = requests.get("http://localhost:8080/recordings", params={"limit":1})
recordings = recordings.json()
recording_id = recordings["recordings"][0]["_id"]
# Get tracker data for the last recording
tracker_data = requests.get("http://localhost:8080/recording/" + recording_id + "/tracker")
#Get counter data
counter_data = requests.get("http://localhost:8080/recording/" + recording_id + "/counter")
# get name of last mp4 file
mp4_files = glob("*.mp4")
mp4_files = sorted(mp4_files, reverse=True)
last_mp4_file = mp4_files[0]
file_name = last_mp4_file.split(".")[0] # take only the name and throw away the file ending
# check that no JSON-file with that name exists
json_file = glob(file_name + ".json")
if len(json_file)==0:
    # store tracker and counter data to JSON file
    with open(file_name + "_tracker.json", "w") as f: 
        json.dump(tracker_data.json(), f)
    with open(file_name + "_counter.json", "w") as f: 
        json.dump(counter_data.json(), f)


