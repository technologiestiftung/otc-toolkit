# Setup TX2

The TX2 has currently no docker images available. Due to that fact we need to do a installation in bare metal. Follow the instructions in the opendatacam repo for that case.

Some topics are already documented for the nano in [setup-nano.md](./setup-nano.md). 

- setting up openssh and ssh keys
- adding the keys to your github account
- adding git user and email
- setting the hostname
- installing curl, zsh, ffmpeg, oh-my-zsh, SpaceVim
- checking and installing python 3.7
  

After that:

- install opendatacam
- test opendatacam on network
- clone otc-toolkit + create folder for recordings + create folder for archiving files (needs to be changed to external drive)

```bash
git clone git@github.com:technologiestiftung/otc-toolkit.git ~/otc/toolkit
mkdir -p ~/otc/{recordings,tmp}
```

For the TX2 we currently have a second branch that holds some modifications on that start/stop scripts for the opendatacam. You will have to checkout that branch and use the scripts there (these might eventually be merged back into master once they are tested to work on bare metal and with docker).

```bash
git fetch
git checkout -t origin/tx2

```

Install [nvm](https://github.com/nvm-sh/nvm) and use node version v10.20.1

```bash
# follow the instructions frm the link above then run
nvm install v10.20.1
nvm alias default v10.20.1
```

Install pm2

We use [pm2](https://pm2.keymetrics.io/) to start and stop the otc cam. 

```bash
npm install pm2 -g
```

Within the otc-toolkit repo (in the tx2 branch) is a file called ecosystem.config.js. This file holds infos for pm2 to start and stop otc.

Make sure the paths in that file match your location of the opedatacam repo.

If done run:

```bash
pm2 start /path/to/ecosystem.config.js
```

Test if you can find the otc in the local network. If it works run

```bash
pm2 stop /path/to/ecosystem.config.js
# this makes sure you can ressurect all services on startup
pm2 save
```

Review all paths in the record.sh script to match your locations then run. Then test the recording script.

```bash
cd ~/otc/toolkit/recording
 ./record.sh /home/otc-admin/otc/opendatacam /home/otc-admin/otc/recordings /home/otc-admin/otc/toolkit/recording /home/otc-admin/otc/tmp > /home/otc-admin/otc/recordings/cron.log 2>&1
```

- add it to the users crontab (not the root user)

```bash
#you will need the path of the user (otc-admin) and of root user 
echo $PATH
sudo echo $PATH
# combine them into one path vriable and add it to the crontab
# below is only an example

crontab -e
# takes you into vim
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

# recreates all services after boot
@reboot pm2 resurrect

*/30 * * * * /home/otc-admin/otc/toolkit/recording/record.sh /home/otc-admin/otc/opendatacam /home/otc-admin/otc/recordings /home/otc-admin/otc/toolkit/recording /home/otc-admin/otc/tmp > /home/otc-admin/otc/recordings/cron.log 2>&1
```

If you done everything right you will have zip files in the tmp folder, cron.log in the recordings folder.

