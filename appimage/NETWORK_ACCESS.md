# ComfyUI Network Access Guide

## Default Behavior (Secure)

By default, ComfyUI is configured for **localhost-only access** (127.0.0.1):
- ✅ Only accessible from the same computer
- ✅ More secure (no network exposure)
- ✅ Good for personal use

**Default URL:** `http://127.0.0.1:8188`

---

## Enabling Network Access

To access ComfyUI from other devices on your **local network** (phones, tablets, other computers):

### Option 1: Command Line Flag (Recommended)

```bash
./ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage --listen-network --web
```

Or shorter:
```bash
./ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage --network --web
```

Or with alias:
```bash
./ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage --lan --web
```

### Option 2: Via GUI Manager

1. Launch the GUI manager (double-click AppImage)
2. In the command line arguments field, add: `--listen-network`
3. Click "Start ComfyUI"

---

## Finding Your Network IP Address

When you enable network access, the startup message will show:

```
🌐 Network Access: ENABLED
📱 Local:   http://127.0.0.1:8188
📱 Network: http://192.168.1.100:8188
⚠️  Security: Accessible from any device on your local network
```

You can also find your IP manually:

```bash
# Linux
hostname -I

# Or
ip addr show | grep inet

# Result example: 192.168.1.100
```

---

## Accessing from Other Devices

Once network access is enabled:

### From Another Computer on Same Network
1. Find your ComfyUI host IP (e.g., 192.168.1.100)
2. Open browser: `http://192.168.1.100:8188`

### From Phone/Tablet on Same WiFi
1. Connect to same WiFi network
2. Open browser: `http://192.168.1.100:8188`
3. Use the web interface just like on desktop

### From Another Room
- Same WiFi network required
- IP address stays the same on your local network
- Works with any device (Windows, Mac, Linux, Android, iOS)

---

## Port Configuration

Default port is **8188**. To change:

```bash
./app.AppImage --listen-network --port 8080 --web
```

Then access via: `http://your-ip:8080`

---

## Firewall Configuration

If you can't connect from other devices, check your firewall:

### Ubuntu/Debian
```bash
# Allow port 8188
sudo ufw allow 8188/tcp

# Check status
sudo ufw status
```

### Fedora/RHEL
```bash
# Allow port 8188
sudo firewall-cmd --add-port=8188/tcp --permanent
sudo firewall-cmd --reload

# Check
sudo firewall-cmd --list-ports
```

### Check if Port is Open
```bash
# From another computer on same network
telnet your-ip 8188

# Or
nc -zv your-ip 8188
```

---

## Security Considerations

### ⚠️ Important Security Notes

When you enable network access (`--listen-network`):

1. **Local Network Only**
   - Only accessible from devices on your LOCAL network (WiFi/LAN)
   - NOT accessible from the internet (unless you port-forward)

2. **No Authentication**
   - ComfyUI has NO built-in password protection
   - Anyone on your network can access it
   - Anyone can generate images/videos using your GPU

3. **Trust Your Network**
   - Only enable on trusted home/office networks
   - Do NOT enable on public WiFi (cafes, airports, etc.)
   - Do NOT port-forward to the internet

### 🔒 Best Practices

**For Home Use:**
```bash
# Safe: Your home network
./app.AppImage --listen-network --web
```

**For Travel/Public WiFi:**
```bash
# Safe: Localhost only (default)
./app.AppImage --web
```

**For Multi-User Environments:**
- Consider using a reverse proxy with authentication (nginx, Apache)
- Use VPN for remote access instead of port forwarding
- Monitor who's on your network

---

## Common Scenarios

### Scenario 1: Desktop + Tablet
**Goal:** Control ComfyUI from tablet while desktop runs it

```bash
# On desktop
./app.AppImage --listen-network --web

# On tablet browser
http://192.168.1.100:8188
```

### Scenario 2: Multiple Workstations
**Goal:** Access one powerful GPU machine from multiple computers

```bash
# On GPU machine
./app.AppImage --listen-network --web

# From any other computer on network
http://gpu-machine-ip:8188
```

### Scenario 3: Remote Access via VPN
**Goal:** Access from outside home network securely

1. Set up VPN (Tailscale, WireGuard, etc.)
2. Run with network access:
   ```bash
   ./app.AppImage --listen-network --web
   ```
3. Connect via VPN first, then access via local IP

### Scenario 4: Reverse Proxy with Authentication
**Goal:** Add password protection

Example nginx config:
```nginx
server {
    listen 80;
    server_name comfyui.local;
    
    auth_basic "ComfyUI Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    
    location / {
        proxy_pass http://127.0.0.1:8188;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Troubleshooting

### Can't Connect from Other Devices

**Check 1: Network Access Enabled**
```bash
# Should show 0.0.0.0, not 127.0.0.1
./app.AppImage --listen-network --web
```

**Check 2: Same Network**
```bash
# From other device, ping the host
ping 192.168.1.100
```

**Check 3: Firewall**
```bash
# Allow port
sudo ufw allow 8188/tcp
```

**Check 4: ComfyUI Running**
```bash
# Check if port is listening
ss -tlnp | grep 8188
# Or
netstat -tlnp | grep 8188
```

### Connection Refused

- ComfyUI not started yet (wait for "Starting server" message)
- Wrong IP address (use `hostname -I` to verify)
- Firewall blocking (check firewall settings)

### Timeout

- Not on same network (check WiFi SSID matches)
- Router isolation enabled (check router "AP Isolation" setting)
- VPN interfering (disable VPN on connecting device)

### Slow Performance

- Network bandwidth limited
- Generating large images/videos (normal behavior)
- WiFi signal weak (move closer or use ethernet)

---

## Quick Reference

| Command | Access Type | Security |
|---------|-------------|----------|
| `./app.AppImage` | Localhost only | 🔒 Secure |
| `./app.AppImage --listen-network` | Local network | ⚠️ Trusted network only |
| `./app.AppImage --listen 0.0.0.0` | Local network | ⚠️ Trusted network only |

**Default (Secure):**
```bash
./app.AppImage --web
# Access: http://127.0.0.1:8188
```

**Network Access:**
```bash
./app.AppImage --listen-network --web
# Access from any device: http://your-ip:8188
```

---

## Related Documentation

- **PRODUCTION_READY_v2.5.0.md** - Full feature list
- **GPU_CPU_MODE_CHECK.md** - GPU detection and diagnostics
- **VERSION_CONTROL.md** - Version management
- **CHANGELOG.md** - All changes and updates

---

**Last Updated:** v2.5.0 (October 2, 2025)
