# ComfyUI Manager - Professional AppImage Distribution

![Version](https://img.shields.io/badge/version-v2.0.5-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20AppImage-green.svg)
![ComfyUI](https://img.shields.io/badge/ComfyUI-v0.3.61-orange.svg)
![Qt](https://img.shields.io/badge/Qt-PySide6-red.svg)

**A professional, self-contained AppImage distribution of ComfyUI with enhanced desktop management capabilities.**

## 🚀 Quick Start

```bash
# Download and run the AppImage
wget https://github.com/slackerchris/ComfyUI-Manager/releases/latest/download/ComfyUI-Manager-v2.0.5-x86_64.AppImage
chmod +x ComfyUI-Manager-v2.0.5-x86_64.AppImage
./ComfyUI-Manager-v2.0.5-x86_64.AppImage
```

## ✨ Features

- **🎮 Professional Qt Desktop Manager** - Native GUI for ComfyUI management
- **📦 Complete Self-Contained AppImage** - 4.3GB executable with full Python ML environment
- **🔄 Automatic Platform Detection** - Wayland/X11 compatibility with Qt crash prevention
- **🎯 Multiple Launch Modes** - GUI manager, direct web interface, or auto-launch browser
- **🛠️ Professional Development Workflow** - Git branching, semantic versioning, comprehensive testing

## 🏗️ Current Status

- ✅ **Core ComfyUI**: Fully functional (v0.3.61)
- ✅ **Web Interface**: Working (http://127.0.0.1:8188)
- ✅ **AppImage Distribution**: Production ready
- ✅ **Qt Manager**: Platform compatibility fixed (v2.0.5)
- ✅ **Professional Workflow**: Clean main branch established

## 📋 Launch Options

```bash
./ComfyUI-Manager-v2.0.5-x86_64.AppImage                # Default (try Qt manager, fallback to direct)
./ComfyUI-Manager-v2.0.5-x86_64.AppImage --direct       # Skip manager, web interface only
./ComfyUI-Manager-v2.0.5-x86_64.AppImage --manager      # Force Qt manager attempt
./ComfyUI-Manager-v2.0.5-x86_64.AppImage --auto-launch  # Auto-open browser
```

## 🔧 Technical Architecture

- **Base**: ComfyUI 0.3.61 with Python 3.12.3
- **ML Stack**: PyTorch 2.8.0+cu128 (CUDA 12.8)
- **Desktop**: PySide6 Qt Manager with Wayland/X11 auto-detection
- **Distribution**: AppImage format for universal Linux compatibility
- **Storage**: User data in `~/.config/ComfyUI/`

## 🎯 Project Evolution

This project evolved from a simple request: *"I would like help setting up an appimage for linux for ComfyUI"* into a comprehensive professional desktop application.

### Development Journey
1. **Phase 1**: Basic AppImage setup with ComfyUI integration
2. **Phase 2**: Professional Qt desktop manager development  
3. **Phase 3**: Git workflow implementation with proper branching
4. **Phase 4**: Qt compatibility debugging and platform detection
5. **Phase 5**: Production release with professional housekeeping

## 🏷️ Version History

- **v2.0.5** - Qt platform detection fix (current main branch)
- **v2.0.4** - Environment setup improvements  
- **v2.0.3** - Comprehensive debugging additions
- **v2.0.2** - Qt manager crash fixes
- **v2.0.1** - Initial hotfix release
- **v2.0.0** - First Qt manager implementation

## 🤝 Contributing

This is a stable main branch. Development happens in feature branches:
- `clean-appimage-release` - Current development branch
- `hotfix-*` - Emergency fixes
- `feature-*` - New features

## 📄 License

This project maintains the same license as the original ComfyUI project.

---

**Built with professional development practices** | **Production ready** | **Community driven**