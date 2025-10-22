from dockerspawner import DockerSpawner
import os

c = get_config()

# Basic config
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
# c.JupyterHub.hub_port = 8000
c.JupyterHub.spawner_class = DockerSpawner

# Set notebook image
c.DockerSpawner.image = os.environ.get('DOCKER_JUPYTER_IMAGE', 'jupyter/minimal-notebook:latest')

# Use same Docker network
c.DockerSpawner.network_name = os.environ.get('DOCKER_NETWORK_NAME', 'jupyterhub_network')

# Notebook directory inside container
notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# Set the runtime to nvidia to enable GPU support
c.DockerSpawner.extra_host_config = {
    'runtime': 'nvidia',
    'device_requests': [
        {
            "Driver": "nvidia",
            "Count": -1,
            "Capabilities": [["gpu"]],
        }
    ]
}

# Authentication: simple dummy (for testing)
from jupyterhub.auth import DummyAuthenticator
# c.JupyterHub.authenticator_class = DummyAuthenticator
# c.DummyAuthenticator.password = "password"  # Replace this for real use

# Authentication: DummyAuthenticator for multiple users
class MyDummyAuthenticator(DummyAuthenticator):
    def get_users(self):
        # List of users and their passwords
        users = {
            'user_1': 'password_1',
            'user_2': 'password_2',
            'user_3': 'password_3',
            # Add more users as needed
        }
        return users

c.JupyterHub.authenticator_class = MyDummyAuthenticator

# Set up admin users (optional, can be any user)
c.Authenticator.admin_users = {'user_1'}

# Default admin settings (for access control)
c.JupyterHub.admin_access = True