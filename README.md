# multi-user-jupyterhub-gpu


# Setup Steps
## Build necessary containers
Build DockerSpawner JupyterHub container
```
docker build -t jupyterhub-container:latest .
```

Build user JupyterLab containers
```
cd ./jupyterlab_container
docker build -t jupyterlab-container:latest .
```

## Deploy using Docker Compose
```
cd ../
docker compose up -d --build
```