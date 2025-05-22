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
curl -fsSL https://pixi.sh/install.sh | sh
sudo cp /groups/scicompsoft/home/$USER/.pixi/bin/pixi /usr/local/bin/
```

2. Create the working directories
```bash
sudo mkdir -p /opt/deploy/fileglancer-central
sudo mkdir -p /opt/deploy/fileglancer-hub
```

3. Create a file at `/opt/deploy/fileglancer-hub/.env` with the following content:
```bash
FGC_DB_URL=sqlite:////opt/data/fileglancer-central/sqlite.db

FGC_CONFLUENCE_URL=https://wikis.janelia.org
FGC_CONFLUENCE_TOKEN=<token here>

FGC_JIRA_URL=https://issues.hhmi.org/issues
FGC_JIRA_TOKEN=<token here>
```

4. Install the systemd service files
```bash
sudo cp fileglancer-central.service /etc/systemd/system/fileglancer-central.service
sudo cp fileglancer-hub.service /etc/systemd/system/fileglancer-hub.service
```
5. Enable the services
```bash
sudo systemctl enable fileglancer-central
sudo systemctl enable fileglancer-hub
```
6. Start the service
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
3. disable the default server block
- comment out the default server block `server {}`
```bash
sudo nano /etc/nginx/nginx.conf
```

4. obtain the SSL certificate for *.int.janelia.org and install it in `/etc/nginx/certs/`
```bash
sudo mkdir -p /etc/nginx/certs/
sudo cp cert.pem /etc/nginx/certs/default.crt
sudo cp key.pem /etc/nginx/certs/default.key
```
- make sure the permissions are correct
```bash
sudo chown root:root /etc/nginx/certs/default.crt
sudo chown root:root /etc/nginx/certs/default.key
sudo chmod 644 /etc/nginx/certs/default.crt
sudo chmod 600 /etc/nginx/certs/default.key
```

5. enable the service
```bash
sudo systemctl enable nginx
```
6. start the service
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
sudo journalctl -u fileglancer-central -f
sudo journalctl -u fileglancer-hub -f
```
