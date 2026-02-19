# multi-user-jupyterhub-gpu


# Setup Steps
## Build necessary containers
**Build DockerSpawner JupyterHub container**
```
docker build -t localhost/jupyterhub-container:latest .
```

**Build user JupyterLab containers**
OPTION 1 - Normal JupyterLab without GPU Fractioning:
```
cd ./jupyterlab_container # OR BUILD fractional_jupyterlab
docker build -t localhost/jupyterlab-container:latest .
# docker build -f Dockerfile-sudo-permissions -t localhost/jupyterlab-container:latest . # if you want to have sudoless root for users
```

OPTION 2 - JupyterLab with GPU Fractioning:
```
cd ./fractional_clearml_jupyterlab
docker build -t localhost/jupyterlab-container:latest .
# docker build -f Dockerfile-sudo-permissions -t localhost/jupyterlab-container:latest . # if you want to have sudoless root for users
```

## Deploy JupyterHub using Docker Compose
```
cd ../
docker compose up -d --build
```

## Deploy JupyterLab using Docker
```
docker run -it --rm --gpus all --ipc=host --pid=host -p 8888:8888 -e JUPYTER_TOKEN='password' localhost/jupyterlab-container:latest
```
