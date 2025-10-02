# ComfyUI AppImage Launch Behavior

## What Happens When You Double-Click the AppImage

### Expected Behavior (Default Launch - No Arguments)

When you double-click `ComfyUI-Manager-v2.4.0-x86_64.AppImage` or run `./ComfyUI-Manager-v2.4.0-x86_64.AppImage` with no arguments:

```
🚀 ComfyUI AppImage - Starting...
=================================
🎮 Launching GUI Management Interface
📋 Use this to start/stop/restart ComfyUI and manage models

🎨 Launching ComfyUI Qt Manager
🔧 Environment check:
   PYTHONPATH: /path/to/site-packages:/path/to/stdlib:/path/to/app
   PYTHONHOME: /path/to/usr
   APPDIR: /tmp/.mount_ComfyUIXXXXXX
   
🔧 Configuring Qt platform...
   XDG_SESSION_TYPE: x11 (or wayland)
   WAYLAND_DISPLAY: Not set (or wayland-0)
   ✅ Configured Qt for X11/Wayland platform
   
✅ System tray icon initialized with ComfyUI Manager branding
```

### What You'll See

1. **Qt Desktop Application Window Opens**
   - Window title: "ComfyUI Manager"
   - System tray icon appears with "ComfyUI Manager v2.4.0" tooltip
   - Taskbar shows "ComfyUI Manager" (NOT "python3")

2. **Application Layout**
   - **Control Tab** 🎮 (default)
     - Status: "🔴 Not Running"
     - Buttons: Start, Stop, Restart, Kill All
     - Web interface URL: http://127.0.0.1:8188
   
   - **Models Tab** 📁
     - Models directory browser
     - Model categories: checkpoints, vae, loras, embeddings, controlnet, etc.
   
   - **Logs Tab** 📋
     - Real-time log output
     - Shows startup messages, errors, process info
   
   - **Settings Tab** ⚙️
     - Auto-start ComfyUI on manager launch
     - Minimize to tray on close
     - Auto-open browser
     - Host/port configuration

3. **Initial State**
   - ComfyUI is NOT running (you need to click "▶ Start ComfyUI")
   - Status bar shows "Ready"
   - No processes detected

### Starting ComfyUI from the Manager

When you click **"▶ Start ComfyUI"**:

```
🚀 Preparing to start ComfyUI...
✅ Using bundled Python: /tmp/.mount_ComfyUIXXXXXX/usr/bin/python3
✅ Using bundled ComfyUI: /tmp/.mount_ComfyUIXXXXXX/app/main.py
📋 Command: /usr/bin/python3 /app/main.py --listen 127.0.0.1 --port 8188 [...]
🔧 Configuring self-contained AppImage environment...
   Detected Python: python3.12
   PYTHONHOME: /tmp/.mount_ComfyUIXXXXXX/usr
   PYTHONPATH: /site-packages:/stdlib:/app...
   LD_LIBRARY_PATH: /usr/lib...
✅ Environment configured, starting process...
✅ Started ComfyUI (PID: 12345)
✅ ComfyUI process running successfully
```

The manager window will show:
- Status: "🟢 Running"
- Processes: 1
- Memory: ~X MB (depending on models loaded)
- CPU: ~X%

### Alternative Launch Modes

#### Direct Web Mode (Skip Manager GUI)
```bash
./ComfyUI-Manager-v2.4.0-x86_64.AppImage --direct --auto-launch
```
- Skips the Qt manager
- Launches ComfyUI web interface directly
- Opens browser automatically

#### Manager Only Mode
```bash
./ComfyUI-Manager-v2.4.0-x86_64.AppImage --manager
```
- Explicitly launches the Qt manager (same as default)

#### Help
```bash
./ComfyUI-Manager-v2.4.0-x86_64.AppImage --help
```
- Shows all available command-line options

### System Tray Behavior

The system tray icon provides:
- **Tooltip**: "ComfyUI Manager v2.4.0 - Running/Stopped"
- **Right-click menu**:
  - Show Manager
  - Start ComfyUI
  - Stop ComfyUI
  - Quit
- **Double-click**: Shows/hides the manager window

### Window Close Behavior

By default (if "Minimize to tray" is enabled):
- Closing the window minimizes to system tray
- Manager keeps running in background
- ComfyUI process continues if started
- Double-click tray icon to restore window

If you want to fully quit:
- Right-click tray icon → "Quit"
- Or disable "Minimize to tray" in settings, then close window

### Auto-Start Feature

If enabled in Settings tab:
- When manager opens, ComfyUI automatically starts
- 1 second delay, then executes start sequence
- Useful for "launch and go" workflow

### Expected Process Behavior

When running:
```bash
ps aux | grep -i comfyui
```

You should see:
```
ComfyUI-Manager    (the Qt manager - PID X)
python3 main.py    (ComfyUI server - PID Y)
```

**NOT** "python3 comfyui_qt_manager.py" - should show as "ComfyUI-Manager"

### Exit Behavior

When you quit the manager:
1. Stops the ComfyUI process gracefully (terminate signal)
2. Stops process monitoring thread
3. Stops UI update timer
4. Saves settings
5. Exits with code 0

### Troubleshooting Expected vs Actual

If the manager doesn't launch:
- Check terminal output for Python/Qt errors
- Verify PySide6 is bundled: `./AppImage --appimage-extract` then check `squashfs-root/usr/lib/python3.12/site-packages/PySide6`

If ComfyUI fails to start:
- Check Logs tab for error messages
- Verify main.py exists: should be in AppImage at `/app/main.py`
- Check Python environment in logs

If you see "python3" instead of "ComfyUI Manager":
- WM_CLASS fix should handle this (v2.4.0)
- Check desktop file: `StartupWMClass=ComfyUI Manager`
- Check line 931: `app.setDesktopFileName("ComfyUI.desktop")`

### Performance Expectations

**Manager GUI**:
- Opens in < 2 seconds
- Memory: ~50-80 MB
- CPU: < 5% idle, < 10% when monitoring

**ComfyUI Process** (after clicking Start):
- Startup time: 3-10 seconds (depending on system)
- Memory: 500 MB - 8 GB (depending on models)
- CPU: Variable (depends on workload)

### Summary

**TL;DR**: Double-click AppImage → Qt Manager opens → Click "Start ComfyUI" → ComfyUI runs → Use web interface at http://127.0.0.1:8188

The manager is a **control panel** - it doesn't automatically start ComfyUI, it gives you control over starting/stopping/monitoring it.
