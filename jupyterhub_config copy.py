# # Import DockerSpawner at the beginning
# from dockerspawner import DockerSpawner

# Set spawn timeouts (in seconds)
c.Spawner.http_timeout = 120  # HTTP timeout
c.Spawner.start_timeout = 120  # Start timeout for user servers

# jupyterhub_config.py

c = get_config()

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# The Docker image to use for user notebooks (use one with GPU libraries if needed, like tensorflow or pytorch)
c.DockerSpawner.image = 'jupyter/tensorflow-notebook:latest'  # Example with TensorFlow and CUDA support; adjust as needed

# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.network_name = network_name

# Enable GPU support for spawned containers
# This uses the NVIDIA Container Toolkit; assumes it's installed on the host
c.DockerSpawner.extra_host_config = {
    'runtime': 'nvidia'  # For older Docker versions; or use the device_requests below for Docker 19.03+
    # 'device_requests': [{
    #     'Driver': 'nvidia',
    #     'Count': -1,  # All GPUs
    #     'Capabilities': [['gpu']]
    # }]
}

# Persist user data in named volumes (one per user)
c.DockerSpawner.volumes = {
    'jupyterhub-user-{username}': '/home/jovyan/work'
}

# Remove containers when they stop
c.DockerSpawner.remove = True

# Use DummyAuthenticator for testing (insecure; change for production)
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
# c.DummyAuthenticator.password = 'yourpassword'  # Set a password here
# Use the DummyAuthenticator (good for testing)
# c.JupyterHub.authenticator_class = 'dummy'

# Define allowed users
c.DummyAuthenticator.allowed_users = {f"user_{i}" for i in range(1, 11)}

# Map each user to their password
c.DummyAuthenticator.passwords = {f"user_{i}": f"password_{i}" for i in range(1, 11)}

# Admin users
c.Authenticator.admin_users = {'admin'}  # Add your admin usernames

# HTTP proxy
c.JupyterHub.proxy_class = 'jupyterhub.proxy.ConfigurableHTTPProxy'
c.ConfigurableHTTPProxy.api_url = 'http://proxy:8001'
c.ConfigurableHTTPProxy.auth_token = os.environ['CONFIGPROXY_AUTH_TOKEN']

# Note: For a full setup, you might need a separate proxy service if not using the default.
# But for basic use, JupyterHub can run its own proxy.

# Listen on all interfaces
c.JupyterHub.ip = '0.0.0.0'