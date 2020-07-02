# Recording

## Install dependencies

```bash
pip install -r requirements.txt
```

## Notes from the LAB

### How to setup PM2 daemon

```bash
cd path/to/opendatacam
PORT=8080 NODE_ENV=production pm2 start node --name otc -- server.js
```
Then you can start and stop processes by the defined `--name`

```bash
pm2 start otc
# or to stop it
pm2 stop otc

```

## Record.sh Script

The scripts needs sudo rights to run the `docker-compose start` command

Arguments:

- $1 path to the folder with the docker-compose.yml
- $2 path to where the recordings are stored
- $3 path to where the scripts are stored (e.g. otc-toolkit/recording)
- $4 path to where the archives should be moved

## Crontab Example

Note: Don't add a trailing slash to the paths
Note: To make docker-compose availalbe we need to add the roots users `$PATH` to the crontab

```bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
*/30 * * * * /path/to/otc-toolkit/recording/record.sh /absolute/path/to/the/folder/of/docker-compose-yml /absolute/path/where/the/recordings/should/be/stored /absolute/path/where/the/scripts/of/otc-toolkit/recording/is /absolute/path/where/the/archives/should/be/moved/to/at/the/end > /path/to/where/you/want/the/logs/cron.log 2>&1
```


## Useful Shell Commands

```bash
zip –sf <archive_name>
```
