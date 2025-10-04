# ComfyUI Manager v2.5.1 - Release Notes

**Release Date:** October 2, 2025  
**Type:** Feature Update (Minor Version)  
**Status:** Production Ready ✅

---

## What's New in v2.5.1 🌐

### Network Access Option

ComfyUI can now be accessed from other devices on your local network!

#### Default Behavior (Secure)
- **Localhost only** (`127.0.0.1:8188`)
- Only accessible from the same computer
- Maximum security - no network exposure

#### New Network Mode
- Enable with `--listen-network`, `--network`, or `--lan` flag
- Listens on `0.0.0.0:8188` (all network interfaces)
- Access from phones, tablets, other computers on same WiFi/LAN
- Perfect for:
  - 📱 Controlling desktop from tablet/phone
  - 💻 Multi-workstation setups
  - 🖥️ Remote access to powerful GPU machine

---

## Quick Start

### Enable Network Access

```bash
# Launch with network access
./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage --listen-network --web
```

**Output shows:**
```
🌐 Network Access: ENABLED
📱 Local:   http://127.0.0.1:8188
📱 Network: http://192.168.1.100:8188
⚠️  Security: Accessible from any device on your local network
```

### Access from Other Devices

1. Start ComfyUI with `--listen-network`
2. Note the network IP address shown (e.g., `192.168.1.100`)
3. On your phone/tablet connected to same WiFi:
   - Open browser
   - Go to: `http://192.168.1.100:8188`
   - Use ComfyUI just like on desktop!

---

## Updated Help System

The `--help` command now includes network options:

```bash
./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage --help
```

Shows:
- Network Options section
- Security notes
- Usage examples
- Documentation references

---

## Security Considerations

### ⚠️ Important

When you enable `--listen-network`:
- ComfyUI is accessible to **anyone on your local network**
- There is **no password protection**
- Anyone can generate images/videos using your GPU

### Safe Usage

✅ **DO use on:**
- Home WiFi network
- Office trusted network
- Private LAN

❌ **DON'T use on:**
- Public WiFi (cafes, airports, hotels)
- Untrusted networks
- Open/guest networks

### Network vs Internet

- `--listen-network` = Local network only (WiFi/LAN)
- Still NOT accessible from the internet
- Your router provides natural firewall protection
- Don't port-forward unless you know what you're doing

---

## Documentation

### New Documentation
- **NETWORK_ACCESS.md** - Complete network setup guide
  - Detailed setup instructions
  - Firewall configuration
  - Security best practices
  - Troubleshooting
  - VPN and reverse proxy examples

### Existing Documentation
- **PRODUCTION_READY_v2.5.0.md** - v2.5.0 features
- **GPU_CPU_MODE_CHECK.md** - GPU diagnostics
- **VERSION_CONTROL.md** - Version management
- **CHANGELOG.md** - All changes

---

## Common Use Cases

### Use Case 1: Tablet Control
**Scenario:** You have a powerful desktop with GPU, but want to control ComfyUI comfortably from your couch with a tablet.

**Solution:**
```bash
# On desktop
./app.AppImage --listen-network --web

# On tablet (same WiFi)
# Open browser to: http://desktop-ip:8188
```

### Use Case 2: Multiple Workstations
**Scenario:** You have one machine with a powerful GPU, and want to use it from multiple computers in your office.

**Solution:**
```bash
# On GPU machine
./app.AppImage --listen-network --web

# From any workstation
# Browser: http://gpu-machine-ip:8188
```

### Use Case 3: Phone Monitoring
**Scenario:** Long video generation running, you want to check progress from your phone while away from desk.

**Solution:**
```bash
# Start with network access
./app.AppImage --listen-network --web

# Check from phone on same WiFi
# http://your-ip:8188
```

---

## Firewall Configuration

If you can't connect from other devices, you may need to allow the port:

### Ubuntu/Debian
```bash
sudo ufw allow 8188/tcp
sudo ufw status
```

### Fedora/RHEL
```bash
sudo firewall-cmd --add-port=8188/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

---

## Upgrading from v2.5.0

### What Changed
- Added `--listen-network` / `--network` / `--lan` flags
- Enhanced `--help` output with network options
- New NETWORK_ACCESS.md documentation
- Updated version control system

### What Didn't Change
- All v2.5.0 features preserved (Universal GPU, device status, AMD setup, etc.)
- Default behavior still localhost-only (secure)
- File size: Still ~8.1 GB
- CUDA and ROCm backends unchanged

### Migration
No migration needed! v2.5.1 is a drop-in replacement:
1. Download new AppImage
2. Optional: Delete old v2.5.0 AppImage
3. Use same commands as before
4. Add `--listen-network` only when needed

---

## All v2.5.x Features

### From v2.5.0 (Universal Release)
- ✅ Multi-backend (CUDA + ROCm) support
- ✅ Automatic GPU detection
- ✅ Works with NVIDIA, AMD, and CPU
- ✅ GUI device status display (Green/Orange/Blue)
- ✅ `--check-device` diagnostics
- ✅ `--amd-setup` automation
- ✅ Render group detection and warnings

### New in v2.5.1
- ✅ `--listen-network` for LAN access
- ✅ Network options in help system
- ✅ NETWORK_ACCESS.md guide
- ✅ Security warnings for network mode

---

## Technical Details

### Implementation
- Modified `AppRun` script to support `NETWORK_LISTEN` variable
- Default: `127.0.0.1` (localhost)
- With `--listen-network`: `0.0.0.0` (all interfaces)
- Displays appropriate URLs based on mode
- Shows local IP via `hostname -I`

### Flags
All three flags do the same thing:
- `--listen-network`
- `--network`
- `--lan`

Choose whichever you prefer!

---

## Download

**Filename:** `ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage`  
**Size:** 8.1 GB  
**SHA256:** `92f812f6ec57453cf8ae2b5869abb80aa261fa3eea274e36aadc18488eace6f3`

### Verify Download
```bash
sha256sum ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage
# Should match: 92f812f6ec57453cf8ae2b5869abb80aa261fa3eea274e36aadc18488eace6f3
```

---

## Support

### Documentation
- Read NETWORK_ACCESS.md for detailed setup
- Check CHANGELOG.md for all changes
- See VERSION_CONTROL.md for version management

### Common Issues
- **Can't connect:** Check firewall, same network, ComfyUI running
- **Slow performance:** Normal for large generations over WiFi
- **Security concerns:** Only use on trusted networks

---

## Next Steps

1. **Test default mode:**
   ```bash
   ./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage --web
   # Access: http://127.0.0.1:8188
   ```

2. **Test network mode:**
   ```bash
   ./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage --listen-network --web
   # Access from phone: http://your-ip:8188
   ```

3. **Check GPU status:**
   ```bash
   ./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage --check-device
   ```

4. **Read documentation:**
   - NETWORK_ACCESS.md for network setup
   - PRODUCTION_READY_v2.5.0.md for all features

---

**Enjoy remote control of your AI image/video generation! 🎨📱**
