FROM jupyterhub/jupyterhub:latest

RUN pip install --no-cache-dir jupyter_server notebook jupyterlab dockerspawner