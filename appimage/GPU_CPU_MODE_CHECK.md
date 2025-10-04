# GPU vs CPU Mode - Quick Check Guide

## How to Check Your Device Status

Run this command to see if you're using GPU or CPU mode:

```bash
./ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage --check-device
```

## What You'll See

### ✅ GPU Mode (Working)
```
======================================================================
🔍 DEVICE CHECK - GPU vs CPU Mode
======================================================================

✅ PyTorch Version: 2.8.0+cu128
✅ PyTorch Location: /tmp/.mount_ComfyU.../site-packages-cuda/torch/__init__.py

🔧 CUDA API Available: True

✅ GPU MODE ENABLED
   Devices Found: 1
   Current Device: 0
   Device Name: NVIDIA GeForce RTX 3090
   Total Memory: 24.00 GB
   Backend: CUDA (NVIDIA GPU)

✅ GPU Tensor Test: SUCCESS
   Tensor Device: cuda:0

======================================================================
```

### ⚠️ CPU Mode (Fallback)
```
======================================================================
🔍 DEVICE CHECK - GPU vs CPU Mode
======================================================================

✅ PyTorch Version: 2.5.1+rocm6.2
✅ PyTorch Location: /tmp/.mount_ComfyU.../site-packages-rocm/torch/__init__.py

🔧 CUDA API Available: False

⚠️  CPU MODE - No GPU acceleration
   Reason: torch.cuda.is_available() returned False

   Possible reasons:
   - ROCm drivers not properly installed
   - GPU not compatible with ROCm 6.2
   - Missing ROCm runtime environment

======================================================================
```

## Checking During Runtime

You can also check the device mode via ComfyUI's API while it's running:

```bash
curl -s http://127.0.0.1:8188/system_stats | python3 -m json.tool | grep -A10 "devices"
```

**GPU Mode Output:**
```json
"devices": [
    {
        "name": "cuda:0",
        "type": "cuda",
        "index": 0,
        "vram_total": 25757220864,
        "vram_free": 23456789012
    }
]
```

**CPU Mode Output:**
```json
"devices": [
    {
        "name": "cpu",
        "type": "cpu",
        "index": null,
        "vram_total": 33515728896,
        "vram_free": 17624158208
    }
]
```

## Understanding CPU vs GPU Mode

### Performance Impact

| Mode | Image Generation Speed | Model Loading | Memory Usage |
|------|----------------------|---------------|--------------|
| **GPU (CUDA)** | 🚀 Fast (2-10s) | Fast | VRAM |
| **GPU (ROCm)** | 🚀 Fast (2-10s) | Fast | VRAM |
| **CPU** | 🐌 Slow (30-120s) | Slow | RAM |

### Why CPU Mode Happens

**On Systems with NVIDIA GPUs:**
- ✅ Should automatically use GPU mode
- ⚠️ If CPU mode: Install NVIDIA drivers (`ubuntu-drivers autoinstall`)

**On Systems with AMD GPUs:**
- ⚠️ **Currently may default to CPU mode** due to ROCm compatibility
- Reason: ROCm PyTorch 2.5.1 may not detect older AMD GPUs
- ROCm 6.2 officially supports RDNA2 (RX 6000) and newer
- Some RDNA1 (RX 5000) GPUs work with workarounds

**On Systems without discrete GPU:**
- ✅ Expected behavior - will use CPU mode
- Works fine but slower

## AMD GPU ROCm Status (Current Known Issue)

### Current Behavior
The universal AppImage includes ROCm PyTorch 2.5.1+rocm6.2, but it may not activate GPU acceleration on all AMD GPUs.

**Working:**
- ROCm backend loads correctly ✅
- PyTorch 2.5.1+rocm6.2 available ✅
- All dependencies present ✅

**Not Working:**
- `torch.cuda.is_available()` returns False ⚠️
- Falls back to CPU mode ⚠️

### Why This Happens

1. **GPU Compatibility**: ROCm 6.2 officially supports:
   - RDNA3 (RX 7000 series) - Full support
   - RDNA2 (RX 6000 series) - Full support
   - RDNA1 (RX 5000 series) - Limited support
   - GCN (older) - No support

2. **Runtime Dependencies**: ROCm needs:
   - ROCm runtime libraries on host system
   - Proper GPU firmware
   - Kernel HSA (Heterogeneous System Architecture) support

3. **Version Mismatch**: PyTorch ROCm 2.5.1 built for ROCm 6.2 may expect specific host ROCm version

### Workarounds

**Option 1: Install ROCm on Host System**
```bash
# Install ROCm runtime (Ubuntu/Debian)
sudo apt install rocm-hip-runtime

# Test GPU detection
rocm-smi
```

**Option 2: Use CUDA Backend with CPU Mode**
The AppImage will still work in CPU mode - just slower.

**Option 3: Use Native ROCm Installation**
Install ComfyUI natively with system PyTorch ROCm for best AMD GPU support.

## Future Improvements

We're working on:
1. **ROCm Runtime Bundling** - Include necessary ROCm libraries in AppImage
2. **Better GPU Detection** - Improved AMD GPU detection and configuration
3. **Fallback Strategies** - Try multiple ROCm versions
4. **Clear Warnings** - Better user feedback when GPU not available

## Getting Help

If you're experiencing CPU mode when you expect GPU mode:

1. **Check your setup:**
   ```bash
   ./ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage --check-device
   ```

2. **For NVIDIA users:** Install NVIDIA drivers
   ```bash
   sudo ubuntu-drivers autoinstall
   sudo reboot
   ```

3. **For AMD users:** Install ROCm runtime
   ```bash
   # Check if ROCm is available
   rocm-smi
   
   # If not, install
   sudo apt install rocm-hip-runtime
   ```

4. **Report issues** with output from `--check-device`

---

**Bottom Line:** The universal AppImage will work in CPU mode if GPU acceleration isn't available. It's slower but functional. NVIDIA users should get GPU acceleration automatically. AMD users may need additional ROCm setup on their system.
