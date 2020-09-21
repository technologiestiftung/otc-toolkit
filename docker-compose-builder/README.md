This part of the tool is **DEPRECATED** since opendatacam switched to a docker-compose setup.


# Opendatacam docker-compose.yml Builder

Note: This is deprecated work. ODC switched to a docker-compose setup. Only the additional containers and the mongo as replica-set is relevant. The docker-compose generating process is not needed anymore. Needs clenaup @fabianmonronzirfas
This is a small tool for generating `docker-compose.yml` and `docker-compose.overrides.yml`. The current process of setting up the volumnes that should be accesable for the opendatacam image and starting the container is not extendable enough. This tool takes some parts of [the script `run-docker.sh`](https://raw.githubusercontent.com/opendatacam/opendatacam/master/docker/run-jetson/run-docker.sh) and packs them up in a docker-compose setup.

## Prerequisites

- Node.js
- git
- docker-compose

## Usage

Tested on jetson nano

```bash
git clone [THIS REPO]
cd [THIS REPO]
npm install
# find all the folders we need
# and write them into a yml file
./bootstrap-templates.sh
# build the js
npm run ts:build
# run the script
npm start
```

This will output two files into the root of the repo

- docker-compose.yml
- docker-compose.overrides.yml

You need to copy them into the folder where you first executed [the installation command](https://github.com/opendatacam/opendatacam#2-install-and-start-opendatacam-) (**!Hint:** It is the folder where `opendatacam_videos/`, `install-opendatacam.sh`, `config.json`, `run-docker.sh` and `run-opendatacam.sh` are located).

If you want more control over the script run

```
npm run ts:build
node dist/cli.js -h

```
