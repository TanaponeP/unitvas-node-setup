#!/bin/bash

# === Tailscale Identity Reset and SSH Setup ===

# Stop the Tailscale service to ensure files aren't in use
sudo systemctl stop tailscaled

# Remove all Tailscale identity and state data
# This clears the node key, cache, and socket data
sudo rm -rf /var/lib/tailscale /var/run/tailscale*

# Start the Tailscale service again
sudo systemctl start tailscaled

# Bring the device online with:
# - a new identity (due to reset)
# - a recognizable hostname
# - headless authentication via authkey
sudo tailscale up --authkey <your-authkey-here> --hostname=<hostname> --reset

# Enable Tailscale SSH (optional if already included above)
# This allows SSH access via the Tailscale network
sudo tailscale up --ssh --hostname=<hostname>