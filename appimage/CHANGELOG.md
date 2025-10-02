# ComfyUI Manager AppImage - Changelog

## v2.4.2 (October 1, 2025) - STABLE RELEASE ✅

**Status**: CUDA auto-detection fixed for systems without NVIDIA drivers

### Critical Fix

**CUDA Auto-Detection for Non-NVIDIA Systems**
   - Fixed ComfyUI crash on systems without NVIDIA drivers
   - Modified `model_management.py` `get_torch_device()` to check `torch.cuda.is_available()` before calling `torch.cuda.current_device()`
   - Automatically falls back to CPU when CUDA is unavailable
   - No forced CPU mode - proper auto-detection as intended
   - File: `ComfyUI.AppDir/app/comfy/model_management.py` lines 187-198

### Testing

- ✅ Auto-detects GPU when available
- ✅ Auto-falls back to CPU when no NVIDIA driver found
- ✅ No crashes on non-NVIDIA systems
- ✅ Works on systems with NVIDIA GPUs
- ✅ Works on CPU-only systems

---

## v2.4.1 (October 1, 2025) - STABLE RELEASE

**Status**: Process detection and restart bugs fixed

### Critical Fixes

1. **False Positive Process Detection Fixed**
   - Manager was detecting itself as ComfyUI (both contained "comfyui" in cmdline)
   - Now checks for 'main.py' AND excludes 'comfyui_qt_manager.py'
   - Lines: 90, 784

2. **Restart Crash Fixed**
   - Blocking QMessageBox was interrupting restart sequence
   - Added `_restarting` flag to skip "stopped" dialog during restart
   - Proper cleanup of `self.comfyui_process` reference
   - Lines: 712-769

3. **Hardcoded Development Path Removed**
   - Removed `/home/chris/Documents/Git/Projects/ComfyUI/main.py` fallback
   - Now requires proper AppImage environment or fails with clear error
   - Works for any user downloading AppImage
   - Line: 584-591

---

## v2.4.0 (October 1, 2025) - STABLE RELEASE

**Status**: All critical bugs from v2.0.7-v2.3.0 resolved

### Critical Fixes

1. **Subprocess Blocking Fixed** 
   - Changed `subprocess.PIPE` → `subprocess.DEVNULL` in both Popen calls
   - Prevents 64KB buffer deadlock when ComfyUI output exceeds pipe capacity
   - Lines: 666-667, 678-679

2. **Dynamic Python Detection**
   - Automatically scans `usr/lib` for `python3.*` directories
   - No longer hardcoded to python3.12
   - Supports any Python 3.x version bundled in AppImage
   - Lines: 621-632

3. **Python Standard Library in PYTHONPATH**
   - Added stdlib directory to PYTHONPATH
   - Fixes import errors for standard library modules
   - PYTHONPATH order: site-packages → stdlib → app
   - Lines: 638-642

4. **Startup Check Fix**
   - Removed `communicate()` call that hung on DEVNULL descriptors
   - Now uses only `poll()` (non-blocking)
   - Prevents manager from freezing during startup checks
   - Lines: 696-711

5. **Process Name / Window Class Fix**
   - Added `app.setDesktopFileName("ComfyUI.desktop")`
   - Updated desktop file `StartupWMClass=ComfyUI Manager`
   - Taskbar and hover now show "ComfyUI Manager" instead of "python3"
   - Lines: 931 + ComfyUI.desktop line 11

### Version Consistency

- All tooltips updated to v2.4.0
- Application version string updated
- Changelog comment added documenting all fixes

### Testing

- ✅ Build successful (4.3 GB compressed from 8.1 GB)
- ✅ Launch test passed
- ✅ Environment configuration verified
- ✅ All 5 critical fixes verified in code review

---

## v2.3.0 (October 1, 2025) - UNSTABLE

**Issues**: Subprocess blocking still present, Python stdlib missing

### Changes
- Attempted fixes for subprocess handling
- Still using hardcoded python3.12

### Known Bugs
- ❌ Subprocess PIPE blocking on large output
- ❌ Missing Python stdlib in PYTHONPATH
- ❌ Process name shows "python3"

---

## v2.2.1 (October 1, 2025) - UNSTABLE

**Issues**: Multiple critical bugs

### Known Bugs
- ❌ Subprocess PIPE blocking
- ❌ Hardcoded Python 3.12
- ❌ communicate() hanging

---

## v2.2.0 (October 1, 2025) - UNSTABLE

**Issues**: Subprocess handling broken

---

## v2.1.6 through v2.1.1 (October 1, 2025) - DEVELOPMENT BUILDS

**Status**: Various intermediate fixes attempted

### Common Issues
- Subprocess blocking intermittent
- Python version detection incomplete
- Process naming issues

---

## v2.0.9, v2.0.8 (October 1, 2025) - TEST BUILDS

**Status**: Minimal builds for testing (365 MB)

### Notes
- Missing ComfyUI components
- Test builds only

---

## v2.0.7 (October 1, 2025) - INITIAL RELEASE

**Status**: First complete build, multiple bugs discovered

### Features
- Qt Manager GUI
- System tray integration
- Process monitoring
- Model management
- Settings persistence

### Known Bugs (Fixed in v2.4.0)
- ❌ Subprocess PIPE blocking
- ❌ Hardcoded Python 3.12
- ❌ Missing stdlib in PYTHONPATH
- ❌ communicate() hanging
- ❌ Process shows as "python3"

---

## Migration Guide

### From v2.3.0 or Earlier → v2.4.0

Simply replace the old AppImage with the new one. Settings are stored in:
- `~/.config/ComfyUI/` (configuration)
- `~/.local/share/ComfyUI/` (models)

No migration needed - all settings preserved.

---

## Recommendations

**Use v2.4.0** - All previous versions have critical bugs that are fixed in v2.4.0.

Previous versions may:
- Hang during startup
- Fail to start ComfyUI
- Show incorrect process names
- Have Python import errors

v2.4.0 resolves all of these issues.
