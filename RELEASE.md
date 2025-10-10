# Releasing Fileglancer

## Release Fileglancer Central to PyPI

If there are changes to the central server code, follow its [release steps](https://github.com/JaneliaSciComp/fileglancer-central/blob/main/RELEASE.md) to push a new version of `fileglancer-central` to [PyPI](https://pypi.org/project/fileglancer-central/).

## Release Fileglancer to PyPI

Follow the Fileglancer [release steps](https://github.com/JaneliaSciComp/fileglancer/blob/main/docs/Release.md) to push a new version of `fileglancer` to [PyPI](https://pypi.org/project/fileglancer/).

## Update versions in Fileglancer Hub

Update the versions in `pixi.toml` (in this repo) to point to the latest versions of both `fileglancer` and `fileglancer-central`. 

Run the installs, to update the `pixi.lock` file:
```
pixi install -e central
pixi install -e hub
```

Push all of these changes to GitHub.

## Dev Deployment

SSH to the Fileglancer development server and update the fileglancer-hub code:

```
cd /opt/deploy/fileglancer-hub
git pull
```

Announce a deployment in progress in the #fileglancer-support channel on Slack, and stop the services:
```
sudo systemctl stop fileglancer-hub
sudo systemctl stop fileglancer-central
```

Start `fileglancer-central` and check the logs to ensure it came up without errors:

```
sudo systemctl start fileglancer-central
sudo journalctl -u fileglancer-central -f
```

Start `fileglancer-hub` and check the logs to ensure it
 came up without errors:

```
sudo systemctl start fileglancer-hub
sudo journalctl -u fileglancer-hub -f
```

Smoke test the installation to make sure everything is working as expected.

## Prod Deployment

Repeat the above instructions on the production server.

