# Use the ClearML fractional GPU base
FROM clearml/fractional-gpu:u22-cu12.3-8gb

LABEL maintainer="yixuan.chia@dell.com"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    SHELL=/bin/bash \
    NB_USER=jovyan \
    NB_UID=1000 \
    NB_GID=100 \
    HOME=/home/jovyan

# System deps + tini (init) + cleanup
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    python3-pip python3-dev wget curl ca-certificates sudo tini \
    # helpful editors & locales if you want:
    # vim nano locales \
    && rm -rf /var/lib/apt/lists/*

# Python packages
RUN python3 -m pip install --upgrade pip && \
    pip3 install \
    jupyterhub \
    jupyterlab \
    notebook \
    numpy \
    pandas \
    matplotlib
# # Create jovyan user matching Jupyter Docker Stacks convention
# # Use existing users if present, else create; ensure home & work dir
# RUN groupadd -g ${NB_GID} users || true && \
#     useradd -m -s /bin/bash -N -u ${NB_UID} -g ${NB_GID} ${NB_USER} && \
#     mkdir -p /home/${NB_USER}/work && \
#     chown -R ${NB_UID}:${NB_GID} /home/${NB_USER}
# # Set working dir
# WORKDIR /home/${NB_USER}


# Create jovyan (UID 1000) if not already created, add to sudo group, and enable passwordless sudo
ENV NB_USER=jovyan NB_UID=1000 NB_GID=100
RUN groupadd -g ${NB_GID} users || true && \
    id -u ${NB_USER} >/dev/null 2>&1 || useradd -m -s /bin/bash -N -u ${NB_UID} -g ${NB_GID} ${NB_USER} && \
    mkdir -p /home/${NB_USER}/work && chown -R ${NB_UID}:${NB_GID} /home/${NB_USER} && \
    usermod -aG sudo ${NB_USER} && \
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/010-sudo-nopasswd && \
    chmod 0440 /etc/sudoers.d/010-sudo-nopasswd

# Expose default singleuser port (Hub passes a port anyway)
EXPOSE 8888

# Switch to non-root
USER ${NB_UID}
# Use tini for signal handling; run the Hub-aware singleuser server
ENTRYPOINT ["tini", "-g", "--"]
CMD ["jupyterhub-singleuser", "--ip=0.0.0.0", "--port=8888"]