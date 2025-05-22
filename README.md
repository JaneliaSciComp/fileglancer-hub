# fileglancer-hub

Scripts and configuration files for deploying Fileglancer with all its bells and whistles. Deploys a [fileglancer-central](https://github.com/JaneliaSciComp/fileglancer-central) server and a JupyterHub customized with the [fileglancer](https://github.com/JaneliaSciComp/fileglancer) extension.

## Installation

- clone this repository
```bash
git clone git@github.com:JaneliaSciComp/fileglancer-hub.git
cd fileglancer-hub
```

## Deployment

### Development

- Assumes you have a working [pixi](https://pixi.sh) installation.

- Start the Fileglancer Central server
```bash
pixi run -e central start
```

- Start the Fileglancer Hub server
```bash
pixi run -e hub start
```

### Production

In production the servers need to run as root in order to allow for setuid priviledge. 

1. Download and install pixi into `/usr/local/bin`
```bash
curl -fsSL https://pixi.sh/install.sh -o install.sh
sudo PIXI_HOME=/usr/local sh install.sh
```

2. Modify the service file to point to the correct working directory
```bash
sudo nano fileglancer.service
```
- change the `WorkingDirectory` to point to the directory where you cloned this repository

3. Install the systemd service files
```bash
sudo cp fileglancer-central.service /etc/systemd/system/fileglancer-central.service
sudo cp fileglancer-hub.service /etc/systemd/system/fileglancer-hub.service
```
4. Enable the services
```bash
sudo systemctl enable fileglancer-central
sudo systemctl enable fileglancer-hub
```
5. Start the service
```bash
sudo systemctl start fileglancer-central
sudo systemctl start fileglancer-hub
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

## Administration

### Hub status checks

```bash
sudo systemctl status fileglancer-central
sudo systemctl status fileglancer-hub
```

### Check the logs of the services

```bash
sudo journalctl -u fileglancer-central
sudo journalctl -u fileglancer-hub
```
