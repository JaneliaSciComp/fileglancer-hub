# Releasing Fileglancer

## Release Fileglancer to PyPI

Follow the [release steps](https://github.com/JaneliaSciComp/fileglancer/blob/main/RELEASE.md) to push a new version of `fileglancer` to [PyPI](https://pypi.org/project/fileglancer/).

## Release Fileglancer Central to PyPI

If there are changes to the central server code, follow the [release steps](https://github.com/JaneliaSciComp/fileglancer-central/blob/main/RELEASE.md) to push a new version of `fileglancer-central` to [PyPI](https://pypi.org/project/fileglancer-central/).

## Update versions in Fileglancer Hub

Update the versions in `pixi.toml` (in this repo) to point to the latest versions of both `fileglancer` and `fileglancer-central`. Push these changes to GitHub.

## Dev Deployment

SSH to the Fileglancer development server and update the fileglancer-hub code:

```
cd /opt/deploy/fileglancer-hub
git pull
```

Announce a deployment in progress in the #fileglancer-support channel on Slack, and stop the services:
```
sudo systemctl stop fileglancer
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

