#!/bin/sh

#ffmpeg -i test03.mp4 -vcodec libx264 -crf 28 testJ3.mp4
import os
cd recording
last_recording = `ls *.mp4`
sep_string="_1"
for entry in $last_recording
do 
    NAME = `echo $entry | cut -d'.' -f1`
    mkdir $NAME
    mv $entry $NAME
    cd $NAME
    img_filename="$NAME$sep_string"
    ls -la
    echo $img_filename
    echo
