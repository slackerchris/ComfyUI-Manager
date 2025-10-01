# ComfyUI Manager AppImage Build Instructions

This directory contains the source files and build tools for creating the ComfyUI Manager AppImage.

## 📋 Prerequisites

```bash
# Install required tools
sudo apt update
sudo apt install wget fuse libfuse2 python3-pip

# Download AppImageTool (if not in build-tools/)
cd build-tools/
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
mv appimagetool-x86_64.AppImage appimagetool
```

## 🏗️ Building the AppImage

### Method 1: Automated Build (Coming Soon)
```bash
# Full automated build script
./build-appimage.sh
```

### Method 2: Manual Build Process

1. **Prepare Base ComfyUI Environment**
```bash
# Clone ComfyUI to get base application
git clone https://github.com/comfyanonymous/ComfyUI.git temp-comfyui
```

2. **Set up Python Environment**
```bash
# Create Python environment with PyTorch + ComfyUI dependencies
# This step creates the large Python runtime (most of the 4.3GB)
python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
python3 -m pip install -r temp-comfyui/requirements.txt
python3 -m pip install PySide6 psutil
```

3. **Copy Application Files**
```bash
# Copy our Qt Manager and AppRun to ComfyUI.AppDir/
cp ComfyUI.AppDir/comfyui_qt_manager.py ComfyUI.AppDir/AppRun ComfyUI.AppDir/
cp ComfyUI.AppDir/*.desktop ComfyUI.AppDir/*.png ComfyUI.AppDir/*.svg ComfyUI.AppDir/
```

4. **Build AppImage**
```bash
# Use appimagetool to create the final AppImage
ARCH=x86_64 ./build-tools/appimagetool ComfyUI.AppDir ComfyUI-Manager-v2.0.5-x86_64.AppImage
```

## 📦 Result

- **Output**: `ComfyUI-Manager-v2.0.5-x86_64.AppImage` (~4.3GB)
- **Contains**: Complete Python 3.12.3 + PyTorch 2.8.0+cu128 + ComfyUI + Qt Manager
- **Self-Contained**: No external dependencies needed

## 🚀 Testing

```bash
# Test the built AppImage
./ComfyUI-Manager-v2.0.5-x86_64.AppImage --direct  # Test core ComfyUI
./ComfyUI-Manager-v2.0.5-x86_64.AppImage           # Test Qt Manager
```

## 📁 Directory Structure

- `ComfyUI.AppDir/` - AppImage source directory
- `build-tools/` - Build utilities (appimagetool, etc.)
- `archive/` - Historical builds and test files

## ⚠️ Notes

- Build requires ~8GB free space
- Build time: 10-30 minutes depending on hardware
- Final AppImage is 4.3GB (too large for GitHub releases)
- Consider cloud storage or torrent distribution for sharing

## 🐛 Troubleshooting

- **Qt Manager crashes**: Check platform detection in comfyui_qt_manager.py
- **Missing dependencies**: Ensure all Python packages are in site-packages
- **Large file size**: Normal - includes complete ML Python environment