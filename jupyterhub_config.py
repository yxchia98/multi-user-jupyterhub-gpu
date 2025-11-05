from dockerspawner import DockerSpawner
import os

c = get_config()

# Basic config
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
# c.JupyterHub.hub_port = 8000
c.JupyterHub.spawner_class = DockerSpawner


# Set notebook image
c.DockerSpawner.image = 'localhost/fractional-jupyterlab:latest'

# Use same Docker network
c.DockerSpawner.network_name = os.environ.get('DOCKER_NETWORK_NAME', 'jupyterhub_network')

# Notebook directory inside container
notebook_dir = '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# clearml container host config
c.DockerSpawner.extra_host_config = {
    'runtime': 'nvidia',
    'device_requests': [
        {
            "Driver": "nvidia",
            "Count": -1,
            "Capabilities": [["gpu"]],
        }
    ],
    "ipc_mode": "host",
    "pid_mode": "host",
}

# Force all new JupyterLab terminals to start in /home/jovyan
c.ServerApp.terminado_settings = {
        'shell_command': ['/bin/bash', '-l', '-c', 'cd /home/jovyan && exec bash -l']
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
            'user_4': 'password_4',
            'user_5': 'password_5',
            'user_6': 'password_6',
            'user_7': 'password_7',
            'user_8': 'password_8',
            'user_9': 'password_9',
            'user_10': 'password_10',
            # Add more users as needed
        }
        return users

c.JupyterHub.authenticator_class = MyDummyAuthenticator

# Default admin settings (for access control)
c.JupyterHub.admin_access = True

# Set up admin users (optional, can be any user)
c.Authenticator.admin_users = {'user_1', 'user_2'}

# DockerSpawner configuration to stop containers when users log out
c.DockerSpawner.remove = True  # Remove containers after logout
c.DockerSpawner.stop_timeout = 60  # Timeout before forcibly stopping the container
c.DockerSpawner.cleanup_containers = True  # Cleanup any leftover containers after logout