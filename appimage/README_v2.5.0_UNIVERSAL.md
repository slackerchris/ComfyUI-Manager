# ComfyUI Manager v2.5.0 - Universal GPU Support ✨

**Release Date**: October 1, 2025  
**Status**: ✅ UNIVERSAL - Works with NVIDIA, AMD, and CPU  
**File**: `ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage` (8.1 GB)  
**SHA256**: `6578583184729180218074cc7564c8101cb48661a0781cc18fe4a561c4cbd588`

---

## 🎯 What Makes This Universal?

This AppImage **automatically detects your GPU** and uses the appropriate acceleration:

- ✅ **NVIDIA GPU** → Uses CUDA acceleration (PyTorch 2.8.0+cu128)
- ✅ **AMD GPU** → Uses ROCm acceleration (PyTorch 2.5.1+rocm6.2)
- ✅ **No GPU / Intel** → Falls back to CPU mode
- ✅ **One file works for everyone** - no need to choose variants

---

## 🚀 Quick Start

```bash
# Download and run
chmod +x ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage
./ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage
```

The AppImage will:
1. Detect your GPU hardware automatically
2. Load the appropriate PyTorch backend (CUDA or ROCm)
3. Launch the Qt Manager GUI
4. You're ready to go!

---

## 🔍 How It Works

### Automatic GPU Detection

On startup, the AppImage:
1. Scans for NVIDIA GPU → Loads PyTorch with CUDA
2. If not found, scans for AMD GPU → Loads PyTorch with ROCm
3. If neither found → Uses CPU mode (CUDA backend works fine for CPU)

### Bundled Backends

The AppImage contains:
- **PyTorch CUDA 2.8.0** (1.7 GB) - For NVIDIA GPUs
- **PyTorch ROCm 2.5.1** (2.0 GB) - For AMD GPUs
- Both are dormant until startup detection selects one

### No Host Dependencies

Unlike other solutions, you **don't need to install**:
- ❌ CUDA toolkit (for NVIDIA)
- ❌ ROCm drivers (for AMD)
- ❌ Any Python packages

The AppImage only requires GPU **drivers** from your system:
- NVIDIA: Your existing NVIDIA driver
- AMD: Works with open-source AMDGPU driver (built into kernel)

---

## 📊 System Requirements

### For NVIDIA GPU Acceleration
- **GPU**: Any NVIDIA GPU with compute capability 5.0+
- **Driver**: NVIDIA proprietary driver (any recent version)
- **RAM**: 8 GB minimum, 16 GB recommended
- **VRAM**: 4 GB minimum, 8 GB+ recommended

### For AMD GPU Acceleration  
- **GPU**: RDNA 1/2/3 or CDNA (RX 5000+, RX 6000+, RX 7000+)
- **Driver**: AMDGPU driver (included in Linux kernel 5.0+)
- **RAM**: 8 GB minimum, 16 GB recommended
- **VRAM**: 8 GB minimum, 12 GB+ recommended

### For CPU Mode
- **CPU**: Multi-core x86_64 processor (4+ cores recommended)
- **RAM**: 16 GB minimum, 32 GB recommended
- **Note**: CPU mode is slow but works on any system

---

## 🎨 Features

### Qt Desktop Manager
- **Professional GUI** - Native desktop application
- **System Tray** - Runs in background
- **Process Control** - Start/Stop/Restart with one click
- **Real-time Monitoring** - CPU, Memory, GPU usage
- **Model Management** - Browse and organize models
- **Settings** - Auto-start, tray behavior, configuration

### Self-Contained
- **No Dependencies** - Everything bundled
- **Portable** - Run from anywhere
- **Isolated** - Doesn't interfere with system
- **Complete** - Ready to use out of the box

### Configuration Locations
- **Settings**: `~/.config/ComfyUI/`
- **Models**: `~/.local/share/ComfyUI/`
- **Output**: `~/.config/ComfyUI/output/`

---

## 🔧 Troubleshooting

### "AMD GPU detected but using CPU mode"

Check if ROCm backend loaded correctly:
```bash
./ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage 2>&1 | grep -i "rocm\|backend"
```

Should show: `✅ AMD GPU detected - using ROCm backend`

### "NVIDIA GPU not detected"

Verify your NVIDIA driver:
```bash
nvidia-smi
```

If this fails, install NVIDIA drivers:
```bash
ubuntu-drivers autoinstall
```

### Performance Issues

**CPU mode too slow?**
- Make sure GPU was detected (check startup messages)
- Verify you have appropriate drivers installed
- Close other applications to free RAM

**GPU mode but still slow?**
- Check VRAM usage (might need --lowvram flag)
- Update GPU drivers to latest version
- Some models require more VRAM than available

---

## 📝 What's New in v2.5.0

### Major Features
- ✅ **Universal GPU support** - Works with NVIDIA and AMD
- ✅ **Automatic backend selection** - No configuration needed
- ✅ **Dual PyTorch bundles** - CUDA and ROCm in one AppImage
- ✅ **Runtime detection** - Smart GPU detection on startup

### Technical Changes
- Added `pytorch_backend_selector.sh` for GPU detection
- Bundled PyTorch 2.8.0+cu128 (NVIDIA)
- Bundled PyTorch 2.5.1+rocm6.2 (AMD)
- Modified AppRun to dynamically set PYTHONPATH
- Increased AppImage size to 8.1 GB (was 4.3 GB)

### All Previous Fixes Preserved
- ✅ v2.4.2: CUDA auto-detection for systems without NVIDIA
- ✅ v2.4.1: Process detection, restart crash fixes
- ✅ v2.4.0: Subprocess blocking, dynamic Python, stdlib paths
- ✅ All stability improvements from earlier versions

---

## 📦 Download

**File**: ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage  
**Size**: 8.1 GB  
**SHA256**: `6578583184729180218074cc7564c8101cb48661a0781cc18fe4a561c4cbd588`

### Installation

```bash
# Make executable
chmod +x ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage

# Run
./ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage
```

---

## 🎯 Which AppImage Should I Use?

### Use v2.5.0 Universal (This One) If:
- ✅ You have an AMD GPU
- ✅ You want maximum compatibility  
- ✅ You don't mind 8.1 GB download
- ✅ You want the latest features

### Use v2.4.2 CUDA-Only If:
- ✅ You have an NVIDIA GPU
- ✅ You want smaller download (4.3 GB)
- ✅ You don't need AMD support

---

## 🏆 Success!

You now have a **truly universal** ComfyUI AppImage that works with any GPU. No more "it only works with NVIDIA" - this works with NVIDIA, AMD, Intel, or none at all.

**Enjoy your AI image generation! 🎨**

---

*For questions or issues, check the startup messages - they'll tell you which backend was detected and loaded.*
