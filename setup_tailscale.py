#!/usr/bin/env python3
"""
setup_tailscale.py

Reset and initialize Tailscale on a cloned Linux VM.

Usage:
    sudo python3 setup_tailscale.py --authkey tskey-xxxxx --hostname unitvas-node2
"""

import subprocess
import argparse
import os
import sys

def run_command(command):
    """Run shell command with output handling."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] {command}\n{result.stderr.strip()}")
    else:
        print(f"[INFO] Executed: {command}")
    return result

def reset_tailscale():
    """Reset Tailscale identity and remove any prior configuration."""
    print("[*] Resetting Tailscale configuration...")
    run_command("tailscale down")
    run_command("tailscale logout")
    run_command("rm -rf /var/lib/tailscale")
    run_command("tailscaled --cleanup")

def start_tailscale(authkey, hostname):
    """Start and authenticate Tailscale with a new identity."""
    print(f"[*] Starting Tailscale with hostname '{hostname}'...")
    run_command(f"tailscale up --authkey {authkey} --hostname {hostname}")

def main():
    parser = argparse.ArgumentParser(description="Reset and connect Tailscale to a new VM identity.")
    parser.add_argument("--authkey", required=True, help="Tailscale auth key (e.g. tskey-xxxxx...)")
    parser.add_argument("--hostname", required=True, help="Tailscale node hostname")
    args = parser.parse_args()

    reset_tailscale()
    start_tailscale(args.authkey, args.hostname)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️  Please run this script as root: sudo python3 setup_tailscale.py")
        sys.exit(1)
    main()
