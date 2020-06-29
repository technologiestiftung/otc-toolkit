#!/bin/sh
cd /home/otc-xavier/otc-toolkit/recording
last_recordings=`ls *.mp4`
for entry in $last_recordings
do
    NAME=`echo $entry | cut -d'.' -f1` # get name of mp4-file without ending
    mkdir $NAME
    mv $entry $NAME
    mv ${NAME}_tracker.json $NAME
    mv ${NAME}_counter.json $NAME
    cd $NAME
    ffmpeg -i $entry ${NAME}_%03d.png
    cd ..
done


