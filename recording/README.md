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
## Define valid/ detectable classes

By default, ODC tries to detect all classes form the COCO dataset on which YOLO was trained. However, certain classes such as moving bicycles are often detected as persons, which is why we recommend to focus on the relvant classes only.

Thus, in `config.json` replace 

`"VALID_CLASSES": [*]` by `"VALID_CLASSES: ["bus", "car", "bicycle", "truck", "motorbike"]`.

## Record.sh Script

The scripts needs sudo rights to run the `docker-compose start` command

Arguments:

- $1 path to the folder with the docker-compose.yml
- $2 path to where the recordings are stored
- $3 path to where the scripts are stored (e.g. otc-toolkit/recording)
- $4 path to where the archives should be moved

## Crontab Example

For the Docker based setup (in our case Nano and Xavier) you need to edit the crontab of the `root` user.

```bash
sudo crontab -e
```

For bare metal Node.js setups (TX2 in our case)

```bash
crontab  -e
```

Note: Don't add a trailing slash to the paths
Note: To make docker-compose available we need to add the roots users `$PATH` to the crontab

```bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
*/30 * * * * /path/to/otc-toolkit/recording/record.sh /absolute/path/to/the/folder/of/docker-compose-yml /absolute/path/where/the/recordings/should/be/stored /absolute/path/where/the/scripts/of/otc-toolkit/recording/is /absolute/path/where/the/archives/should/be/moved/to/at/the/end > /path/to/where/you/want/the/logs/cron.log 2>&1
```

An example crontab for a nano is like the following
```bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
*/30 * * * * /home/otc-admin/otc/otc-toolkit/recording/record.sh /home/otc-admin/otc /home/otc-admin/otc-recordings /home/otc-admin/otc/otc-toolkit/recording /home/otc-admin/tmp > /home/otc-admin/otc-recordings/cron.log 2>&1

```

## Useful Shell Commands

See content of zip archive

```bash
zip –sf <archive_name>
```

See content of file while there is written to it (follow logs)

```bash
tail -F path/to/cron.log
```

If the boards are connected to a wifi or wired connection you should be able to log into them using ssh

```bash
ssh otc-admin@otc-nano.local

ssh otc-admin@otc-tx2-1.local

ssh otc-admin@otc-xavier.local
```
