#!/bin/bash
# Version bump script for ComfyUI Manager AppImage
# Usage: ./bump-version.sh [major|minor|patch]

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 [major|minor|patch]"
    echo "Example: $0 patch  # 2.5.0 -> 2.5.1"
    exit 1
fi

BUMP_TYPE=$1

# Read current version
if [ ! -f VERSION ]; then
    echo "❌ VERSION file not found"
    exit 1
fi

CURRENT_VERSION=$(cat VERSION)
echo "📌 Current version: $CURRENT_VERSION"

# Parse version
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Bump version based on type
case $BUMP_TYPE in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "❌ Invalid bump type: $BUMP_TYPE"
        echo "   Must be: major, minor, or patch"
        exit 1
        ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
echo "🆕 New version: $NEW_VERSION"

# Confirm
read -p "Update version to $NEW_VERSION? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

# Update VERSION file
echo "$NEW_VERSION" > VERSION
echo "✅ Updated VERSION file"

# Update comfyui_qt_manager.py
if [ -f "ComfyUI.AppDir/comfyui_qt_manager.py" ]; then
    echo "🔧 Updating comfyui_qt_manager.py..."
    
    # Update setApplicationVersion
    sed -i "s/setApplicationVersion(\".*\")/setApplicationVersion(\"$NEW_VERSION\")/" ComfyUI.AppDir/comfyui_qt_manager.py
    
    # Update window title
    sed -i "s/ComfyUI Manager v[0-9.]*Universal/ComfyUI Manager v${NEW_VERSION} Universal/" ComfyUI.AppDir/comfyui_qt_manager.py
    
    # Update tooltips
    sed -i "s/ComfyUI Manager v[0-9.]* Universal/ComfyUI Manager v${NEW_VERSION} Universal/g" ComfyUI.AppDir/comfyui_qt_manager.py
    
    echo "✅ Updated comfyui_qt_manager.py"
else
    echo "⚠️  Warning: ComfyUI.AppDir/comfyui_qt_manager.py not found"
fi

# Remind to update CHANGELOG
echo ""
echo "📝 Next steps:"
echo "   1. Update CHANGELOG.md with v$NEW_VERSION entry"
echo "   2. Run: ./build.sh"
echo "   3. Test the AppImage"
echo "   4. Commit: git add VERSION ComfyUI.AppDir/comfyui_qt_manager.py CHANGELOG.md"
echo "   5. Commit: git commit -m \"Bump version to v$NEW_VERSION\""
echo "   6. Tag: git tag v$NEW_VERSION"
echo "   7. Push: git push && git push --tags"
