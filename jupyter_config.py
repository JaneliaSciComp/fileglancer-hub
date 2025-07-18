# Copyright (C) NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Configuration file for jupyterhub.

from pathlib import Path
import pkg_resources
import os


# the command the hub should spawn for the user. It is a single user jupyter
# server, that defaults to the fileglancer UI
c.Spawner.cmd = ['jupyterhub-singleuser']
c.Spawner.args = [
    # point the default URL at the fileglancer handler
    "--ServerApp.default_url=/fg/",
    #
    "--config=" + str(Path(__file__).parent / 'jupyter_server_config.py'),
]


# the spawner to invoke this command
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'

# environment variables to pass to the spawner (if defined)
c.Spawner.environment = {}
# this auto-spawns uiservers without user interaction
c.JupyterHub.implicit_spawn_seconds = 0.01

# apply styling to jupyterhub
c.JupyterHub.template_vars = {
    'hub_title': 'Fileglancer',
    'hub_subtitle': ''
}

# only bind to localhost to prevent unsecured external access
c.JupyterHub.bind_url = 'http://127.0.0.1:8000'


c.JupyterHub.log_datefmt = '%Y-%m-%dT%H:%M:%S'  # ISO8601 (expanded)
c.JupyterHub.template_paths = [Path(__file__).parent / 'templates']

# store JupyterHub runtime files in the user config directory
c.JupyterHub.cookie_secret_file = 'cookie_secret'
c.JupyterHub.db_url = 'jupyterhub.sqlite'
c.ConfigurableHTTPProxy.pid_file = 'jupyterhub-proxy.pid'

# Define the authorization-policy for Jupyter Server.
# This prevents users being granted full access to extensions such as Jupyter
# Lab as a result of being granted the ``access:servers`` permission in Jupyter
# Hub.
c.Authenticator.allow_all = True

# set up oauth service
c.JupyterHub.authenticator_class = 'generic-oauth'

# OAuth2 application info
# -----------------------
c.GenericOAuthenticator.client_id = os.environ.get("OAUTH_CLIENT_ID")
c.GenericOAuthenticator.client_secret = os.environ.get("OAUTH_CLIENT_SECRET")

# Identity provider info
# ----------------------
provider_domain = os.environ.get("OAUTH_DOMAIN")
callback_domain = os.environ.get("OAUTH_CALLBACK_DOMAIN")


c.GenericOAuthenticator.authorize_url = f"https://{provider_domain}/oauth2/v1/authorize"
c.GenericOAuthenticator.token_url = f"https://{provider_domain}/oauth2/v1/token"
c.GenericOAuthenticator.userdata_url = f"https://{provider_domain}/oauth2/v1/userinfo"
c.GenericOAuthenticator.oauth_callback_url = f"https://{callback_domain}/hub/oauth_callback"


# What we request about the user
# ------------------------------
# scope represents requested information about the user, and since we configure
# this against an OIDC based identity provider, we should request "openid" at
# least.
#
# In this example we include "email" and "groups" as well, and then declare that
# we should set the username based on the "email" key in the response, and read
# group membership from the "groups" key in the response.
#
c.GenericOAuthenticator.scope = ["openid", "profile"]
c.GenericOAuthenticator.username_claim = "displayName"
# c.GenericOAuthenticator.auth_state_groups_key = "oauth_user.groups"
