#!/bin/bash

#sh /home/otc-xavier/otc-toolkit/recording/start_odc.sh

#sleep 60;

python3 /home/otc-xavier/otc-toolkit/recording/init_odc.py

sleep 10

python3 /home/otc-xavier/otc-toolkit/recording/start_odc_recording.py

sleep 10

sh /home/otc-xavier/otc-toolkit/recording/ffmpeg_recording.sh

sleep 30

python3 /home/otc-xavier/otc-toolkit/recording/stop_odc_recording.py

sleep 5

python3 /home/otc-xavier/otc-toolkit/recording/download_tracker_data.py

sleep 5

sh /home/otc-xavier/otc-toolkit/recording/ffmpeg_split.sh

#sleep 60

#sh /home/otc-xavier/otc-toolkit/recording/stop_odc.sh
