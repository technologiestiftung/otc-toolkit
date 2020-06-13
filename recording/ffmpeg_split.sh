#!/bin/sh
cd recording
last_recordings=`ls *.mp4`
sep_string="_"
json_ext = ".json"
for entry in $last_recordings
do
    NAME=`echo $entry | cut -d'.' -f1` # get name of mp4-file without ending
    mkdir $NAME
    mv $entry $NAME
    mv ${NAME}.json $NAME
    cd $NAME
    img_file_name="$NAME$sep_string"
    ls -la
    echo $img_filename
    echo $entry
    ffmpeg -i $entry $img_file_name%03d.png
    ls -la
    cd ..
done


