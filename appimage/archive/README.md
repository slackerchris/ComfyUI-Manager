# ComfyUI Manager AppImage Archive

This directory contains archived versions of ComfyUI Manager AppImages that have been superseded or had issues.

## Archived Versions

### v2.0.5 (Original)
- **File**: `ComfyUI-Manager-v2.0.5-x86_64.AppImage`
- **Date**: Oct 1, 2025 00:02
- **Status**: ❌ Deprecated - Had system tray branding issues
- **Issues**: System tray showed "Python 3" instead of "ComfyUI Manager"

### v2.0.5-updated
- **File**: `ComfyUI-Manager-v2.0.5-x86_64-updated.AppImage`  
- **Date**: Oct 1, 2025 00:26
- **Status**: ❌ Deprecated - Partial system tray fix
- **Issues**: Process naming still showed "org.comfyui.python3"

### v2.0.6
- **File**: `ComfyUI-Manager-v2.0.6-x86_64.AppImage`
- **Date**: Oct 1, 2025 09:32  
- **Status**: ❌ Broken - Filesystem permission issues
- **Issues**: 
  - Load3D and Load3DAnimation nodes failed to load
  - Read-only filesystem errors
  - 2 ERROR messages during startup
  - Not production ready

## Current Production Version

### v2.0.7 (Production Ready) ✅
- **File**: `../ComfyUI-Manager-v2.0.7-x86_64.AppImage`
- **Date**: Oct 1, 2025 11:09
- **Status**: ✅ Production Ready
- **Fixes**: 
  - Fixed filesystem permission issues
  - All 494 nodes working (up from 492)
  - Zero startup errors
  - Proper system tray branding
  - Complete 3D model support

## Safe to Delete

These archived versions can be safely deleted to free up ~13GB of disk space if needed.
Each AppImage is ~4.3GB, so removing all archived versions would free up significant space.

## Cleanup Command

To remove all archived versions:
```bash
rm -rf /home/chris/Documents/Git/Projects/ComfyUI/appimage/archive/
```
