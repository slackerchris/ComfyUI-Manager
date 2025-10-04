#!/bin/bash
# Build script for ComfyUI Manager AppImage with proper version control

set -e  # Exit on error

# Get version from VERSION file
VERSION=$(cat VERSION 2>/dev/null || echo "unknown")
echo "📦 Building ComfyUI Manager v${VERSION}"

# Set variables
APPDIR="ComfyUI.AppDir"
OUTPUT_NAME="ComfyUI-Manager-Universal-v${VERSION}-x86_64.AppImage"
APPIMAGETOOL="./build-tools/appimagetool"

# Check if AppDir exists
if [ ! -d "$APPDIR" ]; then
    echo "❌ Error: $APPDIR not found"
    exit 1
fi

# Check if appimagetool exists
if [ ! -x "$APPIMAGETOOL" ]; then
    echo "❌ Error: appimagetool not found or not executable"
    exit 1
fi

# Verify version is set in comfyui_qt_manager.py
echo "🔍 Verifying version in code..."
if ! grep -q "setApplicationVersion(\"${VERSION}\")" "$APPDIR/comfyui_qt_manager.py"; then
    echo "⚠️  Warning: Version ${VERSION} not found in comfyui_qt_manager.py"
    echo "   You may need to update the code."
fi

# Remove old AppImage if exists
if [ -f "$OUTPUT_NAME" ]; then
    echo "🗑️  Removing old $OUTPUT_NAME"
    rm -f "$OUTPUT_NAME"
fi

# Build AppImage
echo "🔨 Building AppImage..."
ARCH=x86_64 "$APPIMAGETOOL" "$APPDIR" "$OUTPUT_NAME"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📊 File info:"
    ls -lh "$OUTPUT_NAME"
    echo ""
    echo "🔐 SHA256:"
    sha256sum "$OUTPUT_NAME"
    echo ""
    echo "📝 Don't forget to:"
    echo "   1. Update CHANGELOG.md with this SHA256"
    echo "   2. Test with: ./$OUTPUT_NAME --check-device"
    echo "   3. Commit and tag: git tag v${VERSION}"
else
    echo "❌ Build failed!"
    exit 1
fi
