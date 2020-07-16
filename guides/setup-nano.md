# Setup Nano

- flash nano
- login to nano
  This might help [finding the nano in the local network](https://apple.stackexchange.com/questions/310061/how-to-find-all-devices-ip-address-hostname-mac-address-on-local-network)
  
- set hostname

```bash
# https://linuxize.com/post/how-to-change-hostname-on-ubuntu-18-04/githu
hostnamectl
sudo hostnamectl set-hostname NEWHOSTNAME
# Open the /etc/hosts file and change the old hostname to the new one.
sudo vim /etc/hosts
```

- install openssh
- enable openssh

```bash
sudo apt update
sudo apt install openssh-server
sudo systemctl status ssh
sudo systemctl enable ssh
sudo systemctl start ssh
```

- create ssh key
- add ssh key to GitHub otcboter

```bash
ls -al ~/.ssh
# Lists the files in your .ssh directory, if they exist
ssh-keygen -t rsa -b 4096 -C "roboter@opentrafficcount.de"
# dont use a password
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
# login to otcboter gituhb account
# copy paste into new key
# name it based on hostname
```

- install zsh
- install curl

```bash
sudo apt-get update && sudo apt-get install zsh curl
```

- install oh-my-zsh

```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# ask to change login shell
# maybe edit ~/.zshrc
vim ~/.zshrc
# change theme to agnoster
```

- SpaceVim
- enable python editing
  
```bash
curl -sLf https://spacevim.org/install.sh | bash
# https://spacevim.org/use-vim-as-a-python-ide/
# edit SpaceVim config
vim ~/.SpaceVim.d/init.toml
# add the following
[[layers]]
name = "lang#python"
```

- check python 3.7

```bash
which python
whereis python
# should show python3.7 if not install it
# https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
# When prompted press Enter to continue:
sudo apt install python3.7
```

- install pip3
- install docker-compose

```bash
sudo apt install python3-pip
sudo apt-get install -y libffi-dev
sudo apt-get install -y python-openssl
sudo apt-get install libssl-dev
sudo pip3 install docker-compose
```

- install opendatacam

```bash
mkdir -p ~/otc/opendatacam
cd ~/otc/opendatacam
# https://github.com/opendatacam/opendatacam#2-install-and-start-opendatacam-
wget -N https://raw.githubusercontent.com/opendatacam/opendatacam/v3.0.1/docker/install-opendatacam.sh
# Give exec permission
chmod 777 install-opendatacam.sh
# NB: You will be asked for sudo password when installing the docker container
# You might want to stop all docker container running before starting OpenDataCam
# sudo docker stop $(sudo docker ps -aq)

# Install command for Jetson Nano
# NB: Will run from demo file, you can change this after install, see "5. Customize OpenDataCam"
./install-opendatacam.sh --platform nano

```

- test opendatacam on network
- clone otc-toolkit + create folder for recordings + create folder for archiving files (needs to be changed to external drive)

```bash
git clone git@github.com:technologiestiftung/otc-toolkit.git ~/otc/toolkit
mkdir -p ~/otc/{recordings,tmp}
```

- test recordings script

```bash
cd ~/otc/toolkit/recording
 ./record.sh /home/otc-admin/otc/opendatacam /home/otc-admin/otc/recordings /home/otc-admin/otc/toolkit/recording /home/otc-admin/otc/tmp > /home/otc-admin/otc/recordings/cron.log 2>&1
```

- add it to the root users crontab

```bash
#you will need the path of the user (otc-admin) and of root user 
echo $PATH
sudo echo $PATH
# combine them into one path vriable and add it to the crontab
# below is only an example

sudo crontab -e
# takes you into vim
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
*/30 * * * * /home/otc-admin/otc/toolkit/recording/record.sh /home/otc-admin/otc/opendatacam /home/otc-admin/otc/recordings /home/otc-admin/otc/toolkit/recording /home/otc-admin/otc/tmp > /home/otc-admin/otc/recordings/cron.log 2>&1
```