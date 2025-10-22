FROM jupyter/minimal-notebook:latest

USER root

# Install sudo
RUN apt-get update && apt-get install -y sudo && rm -rf /var/lib/apt/lists/*

# Allow jovyan to run sudo without a password
RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY ./content/ /home/jovyan/work/

# Set the default user back to jovyan
USER jovyan

# Default workdir (not strictly required)
WORKDIR /home/jovyan/work

# Use the default entrypoint
CMD ["start-notebook.sh"]
