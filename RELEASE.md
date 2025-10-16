# Releasing Fileglancer

## Release Fileglancer to PyPI

Follow the Fileglancer [release steps](https://github.com/JaneliaSciComp/fileglancer/blob/main/docs/Release.md) to push a new version of `fileglancer` to [PyPI](https://pypi.org/project/fileglancer/).

## Update versions in Fileglancer Hub

Update the version in `pixi.toml` (in this repo) to point to the latest version of `fileglancer`.

Run the install, to update the `pixi.lock` file:
```
pixi install
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
sudo systemctl stop fileglancer
```

Start `fileglancer` and check the logs to ensure it came up without errors:

```
sudo systemctl start fileglancer
sudo journalctl -u fileglancer -f
```

Smoke test the installation to make sure everything is working as expected.

## Prod Deployment

Repeat the above instructions on the production server.

