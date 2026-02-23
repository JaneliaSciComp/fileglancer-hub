# Releasing Fileglancer

## 1. Make a new pre-release to PyPI

Push a new alpha version of `fileglancer` to [PyPI](https://pypi.org/project/fileglancer/), following the Fileglancer [release steps](https://github.com/JaneliaSciComp/fileglancer/blob/main/docs/Release.md).

## 2. Update versions in Fileglancer Hub

Update the version in `pixi.toml` (in this repo) to point to the latest version of `fileglancer`.

Run the install, to update the `pixi.lock` file:

```
pixi install
```

Push all of these changes to GitHub.

**Note**: if Pixi cannot find the new package version on Pypi, you may need to clear your Pixi Pypi cache.

```
pixi clean cache --pypi
```

If this command fails to clear the cache, manually clear it using the directory it prints out. E.g.,

```
rm -r <path/to/.cache/rattler/cache/uv-cache>
```

## 3. Alpha version (dev) deployment

SSH to the Fileglancer development server and update the fileglancer-hub code:

```
cd /opt/deploy/fileglancer-hub
git pull
```

Stop the services:

```
sudo systemctl stop fileglancer
```

Start `fileglancer` and check the logs to ensure it came up without errors:

```
sudo systemctl start fileglancer
sudo journalctl -u fileglancer -f
```

## 4. Run integration tests against the dev deployment

To test the full application stack prior to a production release, ensure `.env` file in this repo contains the following:

```
FGC_ENABLE_TEST_API_KEY=true
FGC_TEST_API_KEY:'<your-generated-key>'
```

If a FGC_TEST_API_KEY is not already configured, create a new one. Add this key to both the `.env` file for fileglancer-hub and fileglancer-janelia/playwright.

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

The same value for `FGC_TEST_API_KEY` needs to be added to the `.env` file in the repo with your Playwright tests. See the [fileglancer-janelia](https://github.com/JaneliaSciComp/fileglancer-janelia) repo for example Playwright tests and further documentation of this feature.

## 5. Make a new stable release to PyPI

Push a new major, minor, or patch version of `fileglancer` to [PyPI](https://pypi.org/project/fileglancer/), following the Fileglancer [release steps](https://github.com/JaneliaSciComp/fileglancer/blob/main/docs/Release.md).

## 6. Prod Deployment

Announce a deployment in progress in the #fileglancer-support channel on Slack. Then repeat steps 2 and 3 above on the production server.
