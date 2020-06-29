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

