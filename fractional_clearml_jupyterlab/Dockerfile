# # Start from your existing base image
# FROM clearml/fractional-gpu:u22-cu12.3-8gb

# # Set environment variables for Jupyter
# ENV DEBIAN_FRONTEND=noninteractive \
#     LANG=C.UTF-8 \
#     LC_ALL=C.UTF-8 \
#     PYTHONUNBUFFERED=1

# # Install pip, JupyterLab, and useful extensions
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     python3-pip python3-dev git curl \
#     && pip3 install --upgrade pip \
#     && pip3 install jupyterlab notebook jupyterhub \
#     && pip3 install jupyterlab-git jupyterlab_widgets ipywidgets \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# # Create a working directory
# WORKDIR /workspace

# # Expose Jupyter port
# EXPOSE 8888

# # Default command (JupyterHub will override this with its spawner)
# CMD ["jupyter-lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]



# # Use the ClearML fractional GPU image as the base image
# FROM clearml/fractional-gpu:u22-cu12.3-8gb

# # Set the maintainer label
# LABEL maintainer="yixuan.chia@dell.com"

# # Set the environment variables for Python and JupyterLab
# ENV LANG C.UTF-8
# ENV LC_ALL C.UTF-8

# # Update apt and install dependencies
# RUN apt-get update && apt-get upgrade -y && \
#     apt-get install -y \
#     python3-pip \
#     python3-dev \
#     wget \
#     && rm -rf /var/lib/apt/lists/*

# # Install JupyterLab and any other common packages you might need
# RUN pip3 install --upgrade pip && \
#     pip3 install \
#     jupyterlab \
#     notebook \
#     numpy \
#     pandas \
#     matplotlib

# # Expose JupyterLab port
# EXPOSE 8888

# # Set the command to run JupyterLab on container startup
# CMD ["jupyter-lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]


# Use the ClearML fractional GPU image as the base image
FROM clearml/fractional-gpu:u22-cu12.3-8gb

# Set the maintainer label
LABEL maintainer="yixuan.chia@dell.com"

# Set the environment variables for Python and JupyterLab
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Update apt and install dependencies (including useradd for JupyterHub)
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    python3-pip \
    python3-dev \
    wget \
    sudo \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install JupyterLab and other required packages
RUN pip3 install --upgrade pip && \
    pip3 install \
    jupyterlab \
    notebook \
    numpy \
    pandas \
    matplotlib \
    jupyterhub

# Add a jupyterhub user and group for proper permissions
RUN groupadd -r jupyterhub && useradd -m -r -g jupyterhub jupyterhub

# Switch to the jupyterhub user
USER jupyterhub

# Expose JupyterLab port
EXPOSE 8888

# Set the default command to run JupyterLab when container starts
CMD ["jupyter-lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
