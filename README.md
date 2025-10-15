# fileglancer-hub

Scripts and configuration files for deploying Fileglancer in production at Janelia. This includes a [fileglancer-central](https://github.com/JaneliaSciComp/fileglancer-central) server and a JupyterHub instance customized with the [fileglancer](https://github.com/JaneliaSciComp/fileglancer) extension, as well as an Nginx reverse proxy server.

## Development Deployment

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

## Production Deployment

When working with a shared server, make sure to set your umask so that everything is writeable by the group:
```bash
umask 002
```

### Fileglancer Installation

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
mkdir -p /opt/data/fileglancer # optional, if you want to use a sqlite database
```
3. Clone the repository into `/opt/deploy/fileglancer-hub`
```bash
cd /opt/deploy/
git clone git@github.com:JaneliaSciComp/fileglancer-hub.git
cd fileglancer-hub
```
4. Create a file at `/opt/deploy/fileglancer-hub/.env` with the following content (modify the `FGC_EXTERNAL_PROXY_URL` to use the server hostname):
```bash
FGC_EXTERNAL_PROXY_URL=https://fileglancer-dev.int.janelia.org/fc/files

FGC_DB_URL=sqlite:////opt/data/fileglancer/sqlite.db
# FGC_DB_URL=postgresql://<username>:<password>@<host>:<port>/<database>
FGC_DB_POOL_SIZE=5
FGC_DB_MAX_OVERFLOW=0

FGC_LOG_LEVEL=DEBUG

FGC_ATLASSIAN_URL=https://wikis.janelia.org
FGC_ATLASSIAN_USERNAME=<username here>
FGC_ATLASSIAN_TOKEN=<token here>

FGC_ENABLE_OKTA_AUTH=True // set to False to enable simple insecure auth for testing

FGC_OAUTH_CLIENT_ID=<client id from okta>
FGC_OAUTH_CLIENT_SECRET=<client secret from okta>
FGC_OAUTH_DOMAIN=<okta domain, e.g. hhmi.okta.com>
FGC_OAUTH_CALLBACK_DOMAIN=<the domain of the hub, e.g. fileglancer.int.janelia.org>
```

6. Install the systemd service files
```bash
sudo cp fileglancer.service /etc/systemd/system/fileglancer.service
```
7. Enable the services
```bash
sudo systemctl enable fileglancer
```
8. Start the service
```bash
sudo systemctl start fileglancer
```

### NGINX Reverse Proxy Installation
1. Install nginx
```bash
sudo yum install nginx
```

2. Copy the nginx configuration file to `/etc/nginx/conf.d/fileglancer.conf`
```bash
sudo cp nginx.conf /etc/nginx/conf.d/fileglancer.conf
```

3. Set up the static path for the Fileglancer assets
```bash
find /opt/deploy/fileglancer-hub/ -name "assets"
```
Use this path to replace the `<path_to_fileglancer_assets>` placeholder in the Nginx configuration file (`/etc/nginx/conf.d/fileglancer.conf`).

```bash
find /opt/deploy/fileglancer-hub/ -name "ui"
```
Use this path to replace the `<path_to_fileglancer_ui_directory>` placeholder in the Nginx configuration file (`/etc/nginx/conf.d/fileglancer.conf`).

4. Disable the default server block
- comment out the default server block in the main Nginx configuration file
```bash
sudo nano /etc/nginx/nginx.conf
```

5. Obtain the SSL certificate for *.int.janelia.org and install it in `/etc/nginx/certs/`
```bash
sudo mkdir -p /etc/nginx/certs/
sudo cp cert.pem /etc/nginx/certs/default.crt
sudo cp key.pem /etc/nginx/certs/default.key
```

- Make sure the permissions are correct
```bash
sudo chown root:root /etc/nginx/certs/default.crt
sudo chown root:root /etc/nginx/certs/default.key
sudo chmod 644 /etc/nginx/certs/default.crt
sudo chmod 600 /etc/nginx/certs/default.key
```

6. Enable the service
```bash
sudo systemctl enable nginx
```

7. Start the service
```bash
sudo systemctl start nginx
```

## Administration

### Updating to a new version

First, update to the version of Fileglancer you want to deploy:
```bash
cd /opt/deploy/fileglancer-hub
git pull
```

Then restart the services:

```bash
sudo systemctl restart fileglancer
sudo systemctl restart nginx
```

Make sure to check the logs and smoketest the service to ensure everything came up correctly.


### Hub status checks

```bash
sudo systemctl status fileglancer
sudo systemctl status nginx
```

### Check the logs of the services

```bash
sudo journalctl -u fileglancer -f
sudo journalctl -u nginx -f
```

### Maintenance Mode

The nginx configuration includes maintenance mode functionality that will display a maintenance page when needed.

#### Enabling Maintenance Mode

1. Copy the example maintenance page to the nginx html directory:
```bash
sudo cp maintenance.html.example /etc/nginx/html/maintenance.html
```

2. Edit the maintenance page to update the estimated completion time:
```bash
sudo nano /etc/nginx/html/maintenance.html
```
Replace `[UPDATE WITH ACTUAL TIME]` with the actual estimated completion time.

3. Reload nginx to activate maintenance mode:
```bash
sudo systemctl reload nginx
```

#### Disabling Maintenance Mode

1. Remove the maintenance page:
```bash
sudo rm /etc/nginx/html/maintenance.html
```

2. Reload nginx:
```bash
sudo systemctl reload nginx
```

**Note:** When maintenance mode is active, all requests to the main site and `/fc/files/` endpoints will show the maintenance page instead of the normal application. Static assets like `/fg/assets/` and `/fg/logo.svg` will continue to work normally to ensure the maintenance page displays correctly.
