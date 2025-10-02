# ComfyUI Manager v2.4.2 - AppImage Release Notes

**Release Date**: October 1, 2025  
**Status**: ✅ STABLE - CUDA Auto-Detection Fixed

## What's New in v2.4.2

### Critical Fix: CUDA Auto-Detection

**Problem Solved**: ComfyUI was crashing on systems without NVIDIA drivers because it tried to initialize CUDA before checking if it was available.

**Solution**: Modified ComfyUI's `model_management.py` to properly check `torch.cuda.is_available()` before attempting to access CUDA devices. Now automatically falls back to CPU mode when CUDA isn't available.

### How It Works

The fix ensures proper device detection:

```python
# Before (crashed on non-NVIDIA systems):
return torch.device(torch.cuda.current_device())  # ❌ Crashes if no NVIDIA driver

# After (auto-detects and falls back):
if torch.cuda.is_available():
    return torch.device(torch.cuda.current_device())  # ✅ Uses GPU if available
else:
    cpu_state = CPUState.CPU
    return torch.device("cpu")  # ✅ Falls back to CPU automatically
```

### Benefits

- ✅ **Works on ANY Linux system** - NVIDIA GPU, AMD GPU, Intel, or CPU-only
- ✅ **Auto-detects** - No manual configuration needed
- ✅ **No forced modes** - Uses GPU when available, CPU when not
- ✅ **No crashes** - Graceful fallback instead of RuntimeError

## System Requirements

### Minimum (CPU Mode)
- **OS**: Any modern Linux distribution (x86_64)
- **RAM**: 8 GB minimum, 16 GB recommended
- **CPU**: Multi-core processor (4+ cores recommended)
- **Storage**: ~5 GB for AppImage + space for models

### Recommended (GPU Mode)
- **GPU**: NVIDIA GPU with CUDA support
- **VRAM**: 6 GB minimum, 12 GB+ recommended
- **Driver**: NVIDIA proprietary driver (not nouveau)
- **CUDA**: Automatically provided in AppImage

### What's Included

- ✅ Python 3.12.3 (self-contained)
- ✅ PyTorch 2.8.0 with CUDA 12.8 support
- ✅ PySide6/Qt6 for GUI
- ✅ All ComfyUI dependencies
- ✅ No host Python required
- ✅ Works with any Python version on host (or none at all)

## Installation

```bash
# 1. Download the AppImage
wget https://your-domain.com/ComfyUI-Manager-v2.4.2-x86_64.AppImage

# 2. Make it executable
chmod +x ComfyUI-Manager-v2.4.2-x86_64.AppImage

# 3. Run it
./ComfyUI-Manager-v2.4.2-x86_64.AppImage
```

## Features

### Qt Manager GUI
- **Start/Stop/Restart** ComfyUI server
- **System tray integration** - runs in background
- **Process monitoring** - real-time status updates
- **Model management** - browse and organize models
- **Settings persistence** - remembers your preferences
- **Browser integration** - open web UI with one click

### Self-Contained
- No dependencies on host system
- Bundled Python interpreter
- All libraries included
- Works on any Linux distro

### Configuration Locations

User data is stored in standard Linux locations:
- **Configuration**: `~/.config/ComfyUI/`
- **Models**: `~/.local/share/ComfyUI/`
- **Output**: `~/.config/ComfyUI/output/`

## Usage

### First Launch

1. Launch the AppImage
2. Manager will automatically detect your system (GPU or CPU)
3. Click "▶ Start" to launch ComfyUI
4. Click "Open in Browser" to access the web interface
5. Start creating!

### GPU vs CPU Mode

**The AppImage automatically detects your system:**

- **If you have NVIDIA GPU + driver**: Uses GPU acceleration 🚀
- **If you don't have NVIDIA**: Falls back to CPU mode 🖥️
- **No configuration needed** - it just works!

### Performance Notes

- **GPU Mode**: Fast, recommended for large models
- **CPU Mode**: Slower but works on any system
- **RAM Requirements**: CPU mode uses more RAM than GPU mode

## Troubleshooting

### AppImage Won't Start

```bash
# Check if you can extract it
./ComfyUI-Manager-v2.4.2-x86_64.AppImage --appimage-extract
cd squashfs-root
./AppRun
```

### ComfyUI Not Starting

Check the log display in the manager for errors. Common issues:
- Port 8188 already in use
- Insufficient RAM
- Permissions on config directory

### Slow Performance

If using CPU mode and it's too slow:
- Consider getting an NVIDIA GPU
- Close other applications to free RAM
- Use smaller models

## Version History

### v2.4.2 (Current)
- ✅ Fixed CUDA auto-detection for non-NVIDIA systems
- ✅ Automatic GPU/CPU fallback

### v2.4.1
- ✅ Fixed false positive process detection
- ✅ Fixed restart crash
- ✅ Removed hardcoded development paths

### v2.4.0
- ✅ Fixed subprocess blocking
- ✅ Dynamic Python detection
- ✅ Python stdlib in PYTHONPATH
- ✅ Fixed startup check hang
- ✅ Process name displays correctly

## Contributing

Found a bug? Have a feature request?

1. Check the log display for error messages
2. Test if the issue reproduces
3. Report with details about your system

## License

ComfyUI: GPL-3.0  
Qt Manager: Same as ComfyUI  
Dependencies: Various (see bundled licenses)

## Credits

- **ComfyUI**: comfyanonymous and contributors
- **PyTorch**: Facebook AI Research
- **PySide6**: The Qt Company
- **AppImage**: Simon Peter and contributors

---

**Download**: ComfyUI-Manager-v2.4.2-x86_64.AppImage (4.3 GB)  
**SHA256**: [to be added after final build]

**Questions?** Check the logs first, they usually tell you what went wrong!
