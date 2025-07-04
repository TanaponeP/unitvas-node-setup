# 🔧 init_vm_config.py

Automated post-clone initialization script for Linux VMs.

This script is designed for infrastructure teams or DevOps workflows where virtual machines (VMs) are cloned frequently and need fast, reliable initialization — such as in the **Unitvas project** or private cloud deployments.

---

## 📋 Features

- ✅ Automatically detects the primary network interface
- ✅ Configures network with DHCP using Netplan
- ✅ Sets a custom hostname passed as an argument
- ✅ Updates `/etc/hosts` safely
- ✅ Minimal dependencies, runs on most Ubuntu systems

---

## 🚀 Use Case

Ideal for:

- Post-clone VM setup in QA/staging/production
- Auto-provisioned infrastructure (manual or scripted)
- Container-like behavior for VMs with dynamic identity

---

## 🛠 Requirements

- Python 3.6+
- Ubuntu/Debian-based system (Netplan-compatible)
- Must be run as `root` or with `sudo`

---

## 🧪 Usage

```bash
sudo python3 init_vm_config.py --hostname unitvas-node1
```

### Example Output
```
[*] Detecting primary network interface...
[*] Using network interface: ens33
[INFO] Hostname set to 'unitvas-node1' and /etc/hosts updated.
[INFO] Netplan configuration written to /etc/netplan/99-dhcp-config.yaml
```

---

## 📁 File Overview

| File                 | Description                                       |
|----------------------|---------------------------------------------------|
| `init_vm_config.py`   | Main script for network and hostname configuration |
| `setup_tailscale.py` | Companion script for resetting and joining Tailscale |
| `README.md`           | This documentation file                          |
| `LICENSE`             | License file (MIT License)                       |
| `.gitignore`          | Git ignore rules for Python and system files     |

---

## 🌐 Tailscale Integration

For cloned VMs that need to join a private Tailscale network securely and automatically, use the companion script `setup_tailscale.py`.

This script:

- Resets any previous Tailscale identity (`/var/lib/tailscale`)
- Re-authenticates using your own auth key (`tskey-xxxx...`)
- Sets a custom Tailscale hostname

### Example usage:
```bash
sudo python3 setup_tailscale.py --authkey tskey-abc123... --hostname unitvas-node2
```

> Ensure Tailscale is already installed on the VM.  
> You can generate an auth key from your Tailscale admin console under **Settings → Keys**.

---

## 🔒 Notes & Safety

- This script writes to:
  - `/etc/netplan/99-dhcp-config.yaml`
  - `/etc/hosts`
- Always review and test on a non-critical VM before large-scale deployment

---

## 👨‍💻 Author

Developed by **TOM**  
Part of the infrastructure automation in the Unitvas project

---

## 📄 License

MIT License. See `LICENSE` file for details.
