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

# apply cylc styling to jupyterhub
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
