# fileglancer-hub
Jupyterhub launcher configuration for the fileglancer application


## Installation
- clone this repository
```bash
git clone git@github.com:JaneliaSciComp/fileglancer-hub.git
cd fileglancer-hub
```

## Development
- assumes you have a working [pixi](https://pixi.sh) installation
- start the server
```bash
pixi run start
```

## Production Installation

### Hub installation
1. follow the installation instructions above.

2. download and install pixi
```bash
curl -L https://github.com/prefix-dev/pixi/releases/download/v0.47.0/pixi-x86_64-unknown-linux-musl -o pixi
chmod +x pixi
sudo mv pixi /usr/local/bin/
```
3. modify the service file to point to the correct working directory
```bash
sudo nano fileglancer.service
```
- change the `WorkingDirectory` to point to the directory where you cloned this repository

4. copy the systemd service file to `/etc/systemd/system/fileglancer.service`
```bash
sudo cp fileglancer.service /etc/systemd/system/fileglancer.service
```
5. enable the service
```bash
sudo systemctl enable fileglancer
```
6. start the service
```bash
sudo systemctl start fileglancer
```
### Proxy Installation
1. install nginx
```bash
yum install nginx
```
2. copy the nginx configuration file to `/etc/nginx/conf.d/fileglancer.conf`
```bash
sudo cp nginx.conf /etc/nginx/conf.d/fileglancer.conf
```
3. enable the service
```bash
sudo systemctl enable nginx
```
4. start the service
```bash
sudo systemctl start nginx
```

### Hub status checks

- check the status of the service
```bash
sudo systemctl status fileglancer
```
- check the logs of the service
```bash
sudo journalctl -u fileglancer
```
