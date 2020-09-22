# Crontab


## Recording All Day

Below is an example crontab for recording all day and do a restart of the opendatacam every hour.
If this is running on the tx2 you should set the PLATFORM=tx2 variable for all Xavier and Nano (the docker based platforms) set it to PLATFORM=docker 


### The cron expression
1. A variable for the used platform (PLATFORM=docker or PLATFORM=tx2)
2. The path to the executable called record-all-day.sh
3. The path to the folder where the docker-compose.yml is stored
4. The path to the folder where the recording scripts are located
5. The > path/to/logfile.log 2>&1 dumps all the output into a file so we can review if something went wrong

```bash
# this crontab below is for recording all day and restarting th camera on an hourly basis
# - $1 path to the folder with the docker-compose.yml or opendatacam install
# - $2 path to where the scripts are stored (e.g. otc-toolkit/recording)

0 * * * * PLATFORM=tx2 /home/otc-admin/otc/otc-toolkit/recording/record-all-day.sh /home/otc-admin/opendatacam /home/otc-admin/otc/otc-toolkit/recording > /home/otc-admin/otc/record-all-day.log 2>&1
```
