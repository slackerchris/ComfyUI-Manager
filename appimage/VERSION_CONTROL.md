# Version Control Process

## Overview

This project uses semantic versioning (MAJOR.MINOR.PATCH) with proper change control.

**Current Version:** `2.5.0`

---

## Version Number Format

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─ Patch: Bug fixes, minor improvements (2.5.0 → 2.5.1)
  │     └─────── Minor: New features, backward compatible (2.5.0 → 2.6.0)
  └───────────── Major: Breaking changes (2.5.0 → 3.0.0)
```

---

## Single Source of Truth

**VERSION file** - The authoritative version number
- Location: `/appimage/VERSION`
- Format: Plain text, single line (e.g., `2.5.0`)
- Used by build scripts to generate AppImage filename

---

## Files That Contain Version

### 1. VERSION (Source of Truth)
```
2.5.0
```

### 2. comfyui_qt_manager.py
```python
app.setApplicationVersion("2.5.0")
self.setWindowTitle("ComfyUI Manager v2.5.0 Universal")
self.tray_icon.setToolTip("ComfyUI Manager v2.5.0 Universal...")
```

### 3. CHANGELOG.md
```markdown
## v2.5.0 (October 2, 2025) - UNIVERSAL RELEASE
```

### 4. Documentation Files
- README_v2.5.0_UNIVERSAL.md
- PRODUCTION_READY_v2.5.0.md
- BUILD_v2.5.0_SUMMARY.md
- etc.

---

## Bumping Version

### Automated Way (Recommended)

```bash
# Patch version (bug fixes)
./bump-version.sh patch    # 2.5.0 → 2.5.1

# Minor version (new features)
./bump-version.sh minor    # 2.5.0 → 2.6.0

# Major version (breaking changes)
./bump-version.sh major    # 2.5.0 → 3.0.0
```

This script will:
1. ✅ Update VERSION file
2. ✅ Update comfyui_qt_manager.py (all references)
3. ✅ Remind you to update CHANGELOG.md

### Manual Way

If you need to manually update:

1. **Update VERSION file:**
   ```bash
   echo "2.5.1" > VERSION
   ```

2. **Update comfyui_qt_manager.py:**
   ```python
   # Line ~1067
   app.setApplicationVersion("2.5.1")
   
   # Line ~234
   self.setWindowTitle("ComfyUI Manager v2.5.1 Universal")
   
   # Lines ~480, ~555, ~565 (tooltips)
   "ComfyUI Manager v2.5.1 Universal"
   ```

3. **Update CHANGELOG.md:**
   Add new section at top with date and changes

---

## Building

### Using Build Script (Recommended)

```bash
./build.sh
```

This will:
1. ✅ Read version from VERSION file
2. ✅ Verify version matches code
3. ✅ Build AppImage with correct filename
4. ✅ Generate SHA256 checksum
5. ✅ Remind you to update CHANGELOG

Output: `ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage`

### Manual Build

```bash
VERSION=$(cat VERSION)
ARCH=x86_64 ./build-tools/appimagetool ComfyUI.AppDir \
    "ComfyUI-Manager-Universal-v${VERSION}-x86_64.AppImage"
```

---

## Release Process

### 1. Before Release

- [ ] All features tested and working
- [ ] All bugs fixed
- [ ] Documentation updated

### 2. Version Bump

```bash
./bump-version.sh [major|minor|patch]
```

### 3. Update CHANGELOG

Add new version section:

```markdown
## vX.Y.Z (Date) - TITLE

### New Features
- Feature 1
- Feature 2

### Bug Fixes
- Fix 1
- Fix 2

### Technical Changes
- Change 1

### SHA256
```
[checksum]
```
```

### 4. Build

```bash
./build.sh
```

Copy the SHA256 from build output and paste into CHANGELOG.md

### 5. Test

```bash
./ComfyUI-Manager-Universal-vX.Y.Z-x86_64.AppImage --check-device
./ComfyUI-Manager-Universal-vX.Y.Z-x86_64.AppImage
```

Verify:
- Version shown in window title
- Version shown in tray tooltip
- All features work
- GPU/CPU detection works

### 6. Commit and Tag

```bash
git add VERSION ComfyUI.AppDir/comfyui_qt_manager.py CHANGELOG.md
git commit -m "Release v2.5.0"
git tag v2.5.0
git push origin main
git push origin v2.5.0
```

### 7. Create GitHub Release

1. Go to GitHub → Releases → Draft a new release
2. Choose tag: v2.5.0
3. Title: ComfyUI Manager v2.5.0 Universal
4. Description: Copy from CHANGELOG.md
5. Attach: ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage
6. Include SHA256 checksum in description
7. Publish release

---

## CHANGELOG Guidelines

### Format

```markdown
## vX.Y.Z (Date) - SHORT TITLE

**Status**: Brief status description

### Category 1 (e.g., New Features)

**Feature Name**
   - Implementation detail 1
   - Implementation detail 2
   - Result/outcome

### Category 2 (e.g., Bug Fixes)

**Bug Description**
   - What was broken
   - How it was fixed
   - Result

### SHA256

```
checksum_here
```

### Testing Results

- ✅ Tested configuration 1
- ✅ Tested configuration 2
```

### Categories

- **New Features**: New functionality added
- **Bug Fixes**: Bugs fixed
- **Technical Changes**: Internal improvements
- **Performance**: Speed/efficiency improvements
- **Breaking Changes**: Changes that break compatibility
- **Deprecations**: Features being phased out
- **Security**: Security-related fixes

---

## Version History Quick Reference

| Version | Date | Description | SHA256 |
|---------|------|-------------|--------|
| 2.5.0 | Oct 2, 2025 | Universal GPU + Production UX | `a42255eb...` |
| 2.4.2 | Oct 1, 2025 | CUDA auto-detection fix | `[hash]` |
| 2.4.1 | Oct 1, 2025 | Process detection fixes | `[hash]` |
| 2.4.0 | Oct 1, 2025 | All critical bugs fixed | `[hash]` |

---

## Troubleshooting

### Version mismatch between files

Run:
```bash
./bump-version.sh patch
```

This ensures all files are updated consistently.

### Build script doesn't find version

Check VERSION file exists:
```bash
cat VERSION
```

Should output single line with version number.

### Git tag already exists

Delete old tag:
```bash
git tag -d v2.5.0
git push origin :refs/tags/v2.5.0
```

Then create new tag.

---

## Best Practices

1. ✅ **Always use bump-version.sh** for version changes
2. ✅ **Always use build.sh** for building
3. ✅ **Update CHANGELOG** before releasing
4. ✅ **Test thoroughly** before tagging
5. ✅ **One version = one git tag**
6. ✅ **Include SHA256** in all documentation
7. ✅ **Never reuse version numbers**
8. ✅ **Keep VERSION file in git**

---

## Semantic Versioning Examples

### Patch (2.5.0 → 2.5.1)
- Fixed GPU detection bug
- Updated documentation
- Minor UI tweaks

### Minor (2.5.0 → 2.6.0)
- Added Intel Arc GPU support
- New diagnostic features
- Backward compatible

### Major (2.5.0 → 3.0.0)
- Complete UI redesign
- Changed configuration format
- Requires re-setup

---

**Remember:** Version control is not just about numbers—it's about clear communication with users about what changed and why they should update.
