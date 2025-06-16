# fileglancer-hub

Scripts and configuration files for deploying Fileglancer in production at Janelia. This includes a [fileglancer-central](https://github.com/JaneliaSciComp/fileglancer-central) server and a JupyterHub instance customized with the [fileglancer](https://github.com/JaneliaSciComp/fileglancer) extension, as well as an Nginx reverse proxy server.

## Development

Assumes you have a working [Pixi](https://pixi.sh) installation.

1. Clone this repository
```bash
git clone git@github.com:JaneliaSciComp/fileglancer-hub.git
cd fileglancer-hub
```

2. Start the Fileglancer Central server
```bash
pixi run -e central start
```

3. Start the Fileglancer Hub server
```bash
pixi run -e hub start
```

## Production

In production the servers need to run as root in order to allow for setuid priviledge. 

1. Download and install Pixi into `/usr/local/bin`
```bash
curl -fsSL https://pixi.sh/install.sh | sh
sudo cp /groups/scicompsoft/home/$USER/.pixi/bin/pixi /usr/local/bin/
```

2. Create the working directories
```bash
sudo install -d -m 2775 -o $USER -g $(id -gn) /opt/deploy /opt/data
mkdir -p /opt/deploy/fileglancer-hub
mkdir -p /opt/deploy/fileglancer-central
mkdir -p /opt/data/fileglancer-central
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
sudo yum install nginx
```
2. set up the static path for the fileglancer assets
```bash
find /opt/deploy/fileglancer-hub/ -name "assets"
```
Use this path to replace the `<path_to_fileglancer_assets>` placeholder of the nginx configuration file `nginx.conf` in this repository.

3. copy the nginx configuration file to `/etc/nginx/conf.d/fileglancer.conf`
```bash
sudo cp nginx.conf /etc/nginx/conf.d/fileglancer.conf
```
4. disable the default server block
- comment out the default server block `server {}`
```bash
sudo nano /etc/nginx/nginx.conf
```

5. obtain the SSL certificate for *.int.janelia.org and install it in `/etc/nginx/certs/`
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

6. enable the service
```bash
sudo systemctl enable nginx
```
7. start the service
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
