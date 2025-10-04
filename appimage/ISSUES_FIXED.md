# Important Information - Two Issues Addressed

## Issue 1: GPU Not Working ⚠️

### The Problem
Your AMD GPU is detected but **not being used** because you're not in the `render` group.

### What I Did
✅ Added you to the render group with:
```bash
sudo usermod -a -G render $USER
```

### ⚠️ CRITICAL: You MUST Log Out and Back In
**The GPU will NOT work until you do this!**

The render group change requires a full logout/login to take effect. Just closing and reopening windows won't work.

**Steps:**
1. Save all your work
2. Log out of your Linux session (or reboot)
3. Log back in
4. Test GPU: `./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage --check-device`

**After logout/login, you should see:**
```
✅ GPU MODE ENABLED
Device Name: AMD Radeon RX 6700 XT
Total Memory: 11.98 GB
Backend: ROCm (AMD GPU)
```

---

## Issue 2: Network Access Not Visible in GUI ✅

### The Problem
The network access feature was only available via command line flag (`--listen-network`). It wasn't visible in the GUI.

### What I Did
✅ Added **Network Access Checkbox** to the Settings tab

### Where to Find It
1. Launch the AppImage (double-click or `./app.AppImage`)
2. Go to **⚙️ Settings tab**
3. Look for **Connection Settings** section
4. You'll see: **🌐 Enable Network Access (listen on 0.0.0.0)**

### How It Works

**Default (Secure):**
- Checkbox: ☐ Unchecked
- Host: `127.0.0.1`
- Status: 🔒 Localhost only (secure) - Green background
- Only accessible from same computer

**Network Access Enabled:**
- Checkbox: ☑ Checked
- Host: `0.0.0.0`
- Status: 🌐 Network access enabled - Yellow background
- Security warning popup appears
- Accessible from any device on your LAN

### Using Network Access

1. **Enable in GUI:**
   - Check the "Enable Network Access" box
   - Click "Save Settings"
   - Restart ComfyUI (Stop then Start)

2. **Access from other devices:**
   - Find your IP: Look at the network URL shown
   - On phone/tablet (same WiFi): `http://your-ip:8188`

3. **Security Warning:**
   - You'll see a popup warning about security
   - Only use on trusted networks (home/office)
   - Don't use on public WiFi

---

## Updated AppImage

**Filename:** `ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage`  
**Size:** 8.1 GB  
**SHA256:** `4831037b230445f6355eab967cb3e13bba244ca5f1f28293d1ebbdb154d01617`

---

## Testing Steps

### 1. Test GPU (AFTER logout/login)
```bash
./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage --check-device
```

**Expected:** Green "GPU MODE ENABLED" with AMD RX 6700 XT details

### 2. Test GUI Network Option
```bash
./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage
```

1. Go to ⚙️ Settings tab
2. See "Connection Settings" with network checkbox
3. Check the box
4. Click "Save Settings"
5. See yellow warning banner: "🌐 Network access enabled"

### 3. Test Network Access
With network enabled:
1. Start ComfyUI
2. Note the URL shown
3. On phone (same WiFi), open that URL
4. Should see ComfyUI interface

---

## Summary of Changes

### GUI Manager (comfyui_qt_manager.py)
- ✅ Added network access checkbox to Settings tab
- ✅ Added visual indicators (green/yellow backgrounds)
- ✅ Added security warning popup when enabled
- ✅ Auto-updates host field (127.0.0.1 vs 0.0.0.0)
- ✅ Saves network preference to settings
- ✅ Loads network preference on startup

### Command Line (Still Available)
- ✅ `--listen-network` flag still works
- ✅ `--network` and `--lan` aliases work
- ✅ Command line overrides GUI setting

### Documentation
- ✅ NETWORK_ACCESS.md - Full guide
- ✅ CHANGELOG.md updated
- ✅ Help text (`--help`) updated

---

## Why GPU Wasn't Working

**Technical Explanation:**
- ROCm (AMD GPU driver) requires access to `/dev/kfd` (kernel fusion driver)
- `/dev/kfd` is only accessible to users in the `render` group
- Without render group → ROCm can't access GPU → Falls back to CPU mode
- With render group → ROCm works → GPU acceleration enabled

This is a **Linux permission issue**, not an AppImage or ComfyUI issue.

**One-time fix:**
```bash
sudo usermod -a -G render $USER
# Then logout/login
```

---

## Next Steps

1. **Log out and log back in** (for GPU to work)
2. **Test GPU:**
   ```bash
   ./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage --check-device
   ```
3. **Launch GUI:**
   ```bash
   ./ComfyUI-Manager-Universal-v2.5.1-x86_64.AppImage
   ```
4. **Go to Settings tab** to see network option
5. **Optional:** Enable network access if you want to use from phone/tablet

---

## Support

If GPU still doesn't work after logout/login:
```bash
# Verify you're in render group
groups | grep render

# Should show: render

# Check /dev/kfd access
ls -la /dev/kfd

# Should show: crw-rw---- ... root render ... /dev/kfd
```

If network option doesn't appear:
- Make sure you're using the new v2.5.1 AppImage (SHA: 4831037...)
- Look in ⚙️ Settings tab → Connection Settings section

---

**Both issues are now fixed! 🎉**
- GPU: Will work after logout/login
- Network: Checkbox visible in Settings tab
