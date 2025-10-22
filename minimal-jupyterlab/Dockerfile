FROM jupyter/minimal-notebook:latest

USER root

# Install sudo and other utils
RUN apt-get update && apt-get install -y sudo gosu procps && rm -rf /var/lib/apt/lists/*

# Add an entrypoint script that will create a user at container start
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Make sure /etc/skel is used for new users, adjust permissions
RUN chown -R root:root /etc/skel

# Default workdir (not strictly required)
WORKDIR /home

# Use the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["start-notebook.sh"]
