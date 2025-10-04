#!/bin/bash
# AMD GPU Setup Script for ComfyUI Universal AppImage
# This script checks and fixes common AMD GPU configuration issues

echo "======================================================================"
echo "🔧 AMD GPU Setup for ComfyUI Universal AppImage"
echo "======================================================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ ERROR: Do not run this script as root (don't use sudo)"
    echo "   The script will ask for your password when needed"
    exit 1
fi

# Check if AMD GPU is present
if ! lspci 2>/dev/null | grep -i 'vga.*amd' > /dev/null; then
    echo "⚠️  No AMD GPU detected"
    echo "   This script is only needed for AMD GPU users"
    echo ""
    lspci | grep -i vga
    echo ""
    exit 0
fi

echo "✅ AMD GPU detected:"
lspci | grep -i vga | grep -i amd
echo ""

# Check if /dev/kfd exists
if [ ! -c /dev/kfd ]; then
    echo "❌ /dev/kfd not found"
    echo "   ROCm kernel driver is not loaded"
    echo ""
    echo "   You may need to install ROCm or update your kernel:"
    echo "   sudo apt install rocm-hip-runtime"
    echo ""
    exit 1
fi

echo "✅ /dev/kfd exists (ROCm kernel driver present)"
echo ""

# Check if user can access /dev/kfd
if [ -r /dev/kfd ] && [ -w /dev/kfd ]; then
    echo "✅ You already have access to /dev/kfd"
    echo "   AMD GPU should work with ComfyUI"
    echo ""
    exit 0
fi

# User doesn't have access - need to add to render group
echo "⚠️  You don't have access to /dev/kfd"
echo "   Need to add your user to the 'render' group"
echo ""

# Check if render group exists
if ! getent group render > /dev/null; then
    echo "❌ 'render' group does not exist"
    echo "   Creating it..."
    sudo groupadd -r render || exit 1
    echo "✅ 'render' group created"
    echo ""
fi

# Check if already in render group
if groups | grep -q '\brender\b'; then
    echo "✅ You're already in the 'render' group"
    echo "   But the current session doesn't have it active yet"
    echo ""
    echo "🔄 Please log out and log back in to activate the group"
    echo "   Or run: newgrp render"
    echo ""
    exit 0
fi

# Add user to render group
echo "Adding user '$USER' to 'render' group..."
echo "(You may be prompted for your password)"
echo ""

sudo usermod -a -G render "$USER"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! User added to 'render' group"
    echo ""
    echo "📋 IMPORTANT: You must log out and log back in for this to take effect"
    echo ""
    echo "After logging back in, run this to verify:"
    echo "   ./ComfyUI-Manager-Universal-v2.5.0-x86_64.AppImage --check-device"
    echo ""
    echo "You should see '✅ GPU MODE ENABLED' with your AMD GPU name"
    echo ""
else
    echo ""
    echo "❌ Failed to add user to render group"
    echo "   Try manually: sudo usermod -a -G render $USER"
    echo ""
    exit 1
fi
