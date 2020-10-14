# Crontab

<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Crontab](#crontab)
  - [Setup](#setup)
  - [Recording All Day](#recording-all-day)
  - [(Sudo) Crontab](#sudo-crontab)
    - [The Cron Expression](#the-cron-expression)

<!-- /code_chunk_output -->


## Setup 


Clone the repo to the machine or update

```bash
git clone git@github.com:technologiestiftung/otc-toolkit.git ~/otc/toolkit

# or 

cd ~/otc/toolkit/
git pull origin master
```


## Recording All Day

The script we are going to run is derived from the original recording script and uses just the already existing sup-scripts.  You can find it under [github.com/technologiestiftung/otc-toolkit/recording/record-all-day.sh](https://github.com/technologiestiftung/otc-toolkit/blob/master/recording/record-all-day.sh)

To make the scripts for usable for the TX2 (bare metal install) and the Docker boards (Nano and Xavier) we introduced an environment variable called `PLATFORM` which can either be `docker` or `tx2`.

This variable needs to be set for a crontab to allow the scripts to run.

The script will try to stop the running opendatacam, restart it, initialize the ODC and start recording again. This should be done every hour.


## (Sudo) Crontab

If running on TX2 (bare metal) you don't need the sudo crontab. For Docker boards you need it.

To open it run the following commands.

```bash
echo $PATH
# then
sudo crontab -e
# or on TX2
crontab -e 
```

We need the `PATH` to give the crontab access to all executables we need for the scripts.   



### The Cron Expression

Below is an example crontab for recording all day and do a restart of the opendatacam every hour.
If this is running on the `tx2` you should set the `PLATFORM=tx2` variable for all Xavier and Nano (the docker based platforms) set it to `PLATFORM=docker` 

1. A variable for the used platform (`PLATFORM=docker` or `PLATFORM=tx2`)
2. The path to the executable called `record-all-day.sh`
3. The path to the folder where the `docker-compose.yml` is stored
4. The path to the folder where the recording scripts are located
5. The `> path/to/logfile.log 2>&1` dumps all the output into a file so we can review if something went wrong

```bash
# this crontab below is for recording all day and restarting th camera on an hourly basis
# - $1 path to the folder with the docker-compose.yml or opendatacam install
# - $2 path to where the scripts are stored (e.g. otc-toolkit/recording)

0 * * * * PLATFORM=tx2 /home/otc-admin/otc/otc-toolkit/recording/record-all-day.sh /home/otc-admin/opendatacam /home/otc-admin/otc/otc-toolkit/recording > /home/otc-admin/otc/record-all-day.log 2>&1
```
