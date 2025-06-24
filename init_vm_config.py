#!/usr/bin/env python3
"""
init_vm_config.py

Automates the initial configuration of a cloned Linux VM by:
1. Setting a new hostname (provided via --hostname argument)
2. Detecting the primary network interface
3. Configuring the interface for DHCP using Netplan

This script is designed for post-cloning initialization tasks
in environments such as Unitvas, private cloud, or dev lab setups.

Author: TOM's Automation Suite
"""

import subprocess
import os
import re
import sys
import argparse

def run_command(command):
    """Run a shell command and return its result."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {command}\n{result.stderr.strip()}")
    else:
        print(f"[INFO] Executed: {command}")
    return result

def detect_primary_interface():
    """Detect the main network interface, excluding virtual and loopback."""
    result = run_command("ip -o link show | awk -F': ' '{print $2}'")
    interfaces = result.stdout.strip().split('\n')
    for iface in interfaces:
        if iface.startswith(("lo", "docker", "br", "tailscale")):
            continue
        return iface
    return None

def configure_dhcp_netplan(interface_name):
    """Write a Netplan config to enable DHCP for the specified interface."""
    netplan_content = f"""network:
  version: 2
  renderer: networkd
  ethernets:
    {interface_name}:
      dhcp4: true
"""
    config_path = "/etc/netplan/99-dhcp-config.yaml"
    try:
        with open(config_path, "w") as f:
            f.write(netplan_content)
        print(f"[INFO] Netplan configuration written to {config_path}")
        run_command("netplan apply")
    except Exception as e:
        print(f"[ERROR] Failed to write Netplan configuration: {e}")

def set_hostname(new_hostname):
    """Set the system hostname and update /etc/hosts accordingly."""
    run_command(f"hostnamectl set-hostname {new_hostname}")
    try:
        with open("/etc/hosts", "r") as f:
            hosts_lines = f.readlines()
        updated_lines = []
        found = False
        for line in hosts_lines:
            if line.startswith("127.0.1.1"):
                updated_lines.append(f"127.0.1.1\t{new_hostname}\n")
                found = True
            else:
                updated_lines.append(line)
        if not found:
            updated_lines.append(f"127.0.1.1\t{new_hostname}\n")
        with open("/etc/hosts", "w") as f:
            f.writelines(updated_lines)
        print(f"[INFO] Hostname set to '{new_hostname}' and /etc/hosts updated.")
    except Exception as e:
        print(f"[ERROR] Failed to update /etc/hosts: {e}")

def main():
    parser = argparse.ArgumentParser(description="Initial VM setup: hostname and DHCP configuration.")
    parser.add_argument("--hostname", required=True, help="New hostname for this machine (e.g., unitvas-node2)")
    args = parser.parse_args()

    print("[*] Detecting primary network interface...")
    interface = detect_primary_interface()
    if not interface:
        print("[ERROR] No suitable network interface found.")
        sys.exit(1)

    print(f"[*] Using network interface: {interface}")
    set_hostname(args.hostname)
    configure_dhcp_netplan(interface)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️  This script must be run as root. Try: sudo python3 init_vm_config.py --hostname unitvas-nodeX")
        sys.exit(1)
    main()
