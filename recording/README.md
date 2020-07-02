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


tbd

## Crontab Example

Note: Don't add a trailing slash to the paths

```bash
*/30 * * * * /path/to/otc-toolkit/recording/record.sh /absolute/path/to/the/folder/of/docker-compose-yml/ /absolute/path/where/the/recordings/should/be/stored /absolute/path/where/the/scripts/of/otc-toolkit/recording/is >> /path/to/where/you/want/the/logs/cron.log 2>&1
```



