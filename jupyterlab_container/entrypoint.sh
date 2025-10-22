#!/usr/bin/env bash
set -e

# If JUPYTERHUB_USER is provided, create that user and give it passwordless sudo.
if [ -n "$JUPYTERHUB_USER" ]; then
  USERNAME="$JUPYTERHUB_USER"
  # default passwordless (no passwd needed)
  useradd -m -s /bin/bash -G sudo "$USERNAME" || true

  # create home dir and copy skeleton if empty
  HOMEDIR="/home/$USERNAME"
  mkdir -p "$HOMEDIR"
  chown -R "$USERNAME":"$USERNAME" "$HOMEDIR"

  # give passwordless sudo for users in sudo group
  if ! grep -q "^%sudo" /etc/sudoers.d/jupyterhub 2>/dev/null; then
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/jupyterhub
    chmod 0440 /etc/sudoers.d/jupyterhub
  fi

  # optionally set a password if JUPYTER_USER_PASS is provided (not recommended)
  if [ -n "$JUPYTER_USER_PASS" ]; then
    echo "$USERNAME:$JUPYTER_USER_PASS" | chpasswd
  fi

  # If you want the container to run as that user, exec with gosu
  exec gosu "$USERNAME" "$@"
else
  # No JUPYTERHUB_USER provided: fall back to jovyan user from base image
  exec "$@"
fi
