# CUDA 13.0, cuDNN, Ubuntu 24.04 (official NVIDIA base)
# Use -devel if you may compile Python/CUDA extensions; switch to -runtime for a smaller image
FROM nvidia/cuda:13.0.0-cudnn-devel-ubuntu24.04

LABEL maintainer="yixuan.chia@dell.com"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    SHELL=/bin/bash \
    NB_USER=jovyan \
    NB_UID=1000 \
    NB_GID=100 \
    HOME=/home/jovyan

# ------------------------------------------------------------
# System deps + tini
# ------------------------------------------------------------
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
      python3 python3-pip python3-dev \
      wget curl ca-certificates sudo tini git \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Python bootstrap
# ------------------------------------------------------------
RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir \
      jupyterhub jupyterlab notebook \
      numpy pandas matplotlib \
      genv

# ------------------------------------------------------------
# Preinstall PyTorch (GPU) matching CUDA 13.0 (cu130 wheels)
# NOTE:
#  - We pull wheels from PyTorch's official CUDA-13 index (cu130).
#  - If you prefer to pin exact versions, replace unpinned packages below
#    with the specific versions listed in the cu130 index directory.
# ------------------------------------------------------------
RUN pip3 install --no-cache-dir --index-url https://download.pytorch.org/whl/cu130 \
      torch torchvision torchaudio

# ------------------------------------------------------------
# Create jovyan user & workspace
# ------------------------------------------------------------
RUN groupadd -g ${NB_GID} users || true && \
    useradd -m -s /bin/bash -N -u ${NB_UID} -g ${NB_GID} ${NB_USER} && \
    mkdir -p /home/${NB_USER}/work && \
    chown -R ${NB_UID}:${NB_GID} /home/${NB_USER}

WORKDIR /home/${NB_USER}
USER ${NB_UID}

# ------------------------------------------------------------
# Built-in startup: Genv limits, then JupyterHub singleuser
# ------------------------------------------------------------
# Allow overrides at runtime via env (handy for profiles)
ENV GENV_NAME=lab \
    GENV_GPUS=1 \
    GENV_VRAM=12GB \
    JUPYTER_PORT=8888

# Startup script that:
# 1) creates/activates Genv env
# 2) attaches 1 GPU and caps VRAM to 12GB
# 3) execs jupyterhub-singleuser
RUN printf '%s\n' \
  '#!/usr/bin/env bash' \
  'set -euo pipefail' \
  '' \
  'echo "[startup] Genv environment: ${GENV_NAME}"' \
  'echo "[startup] GPUs: ${GENV_GPUS} | VRAM cap: ${GENV_VRAM}"' \
  '' \
  'if ! genv activate "${GENV_NAME}" 2>/dev/null; then' \
  '  echo "[startup] Creating Genv env: ${GENV_NAME}"' \
  '  genv activate -c "${GENV_NAME}"' \
  'fi' \
  'genv config --gpus "${GENV_GPUS}" --memory "${GENV_VRAM}"' \
  'genv status || true' \
  '' \
  'exec jupyterhub-singleuser --ip=0.0.0.0 --port="${JUPYTER_PORT}"' \
  > /usr/local/bin/start-singleuser.sh && \
  chmod +x /usr/local/bin/start-singleuser.sh

# Entrypoint/CMD for JupyterHub singleuser
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-singleuser.sh"]