#!/bin/sh

#Start recording
#echo "recording starting now"
cd /home/otc-xavier/otc-toolkit/recording

#ffmpeg -use_wallclock_as_timestamps 1 -f mjpeg -i "http://localhost:8080/webcam/stream" -vf "scale=320:-1" -c:v copy -t 00:00:10 -y $(date "+%Y-%m-%d-%H-%M-%S-%6N").mp4
ffmpeg -use_wallclock_as_timestamps 1 -f mjpeg -i "http://localhost:8080/webcam/stream" -t 00:00:10 -c:v copy -y $(date "+%Y-%m-%d-%H-%M-%S-%6N").mp4
#ffmpeg -use_wallclock_as_timestamps 1 -f mjpeg -i "http://localhost:8080/webcam/stream" -filter_complex "[0:v]scale=640/2:-1[v]" -map "[v]" -map 0:a -c:a copy  -t 00:00:10 -y $(date "+%Y-%m-%d-%H-%M-%S-%6N").mp4

#sleep 10
#echo "recording done"

#Check duration Change time
#ffmpeg -i test7.mp4 -c copy -f null -

