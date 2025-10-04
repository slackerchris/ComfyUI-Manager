#!/bin/bash
# PyTorch Backend Selector - Detects GPU and sets appropriate PYTHONPATH
# Part of ComfyUI Manager Universal GPU Support

# Get APPDIR from argument or detect from script location
if [ -n "$1" ]; then
    APPDIR="$1"
else
    # Fallback: detect from script location
    APPDIR="$(dirname "$(readlink -f "${0}")")"
fi

# Send status messages to stderr so they don't interfere with path output
echo "🔍 Detecting GPU hardware..." >&2

# Detect GPU type
if lspci 2>/dev/null | grep -i 'vga.*nvidia' > /dev/null; then
    echo "✅ NVIDIA GPU detected - using CUDA backend" >&2
    PYTORCH_BACKEND="cuda"
elif lspci 2>/dev/null | grep -i 'vga.*amd' > /dev/null; then
    echo "✅ AMD GPU detected - using ROCm backend" >&2
    PYTORCH_BACKEND="rocm"
    
    # Check if user has access to /dev/kfd (ROCm kernel driver)
    if [ -c /dev/kfd ]; then
        if [ ! -r /dev/kfd ] || [ ! -w /dev/kfd ]; then
            echo "" >&2
            echo "⚠️  WARNING: AMD GPU detected but /dev/kfd is not accessible" >&2
            echo "   ROCm requires access to /dev/kfd for GPU acceleration" >&2
            echo "" >&2
            echo "   To enable AMD GPU support, run:" >&2
            echo "   sudo usermod -a -G render \$USER" >&2
            echo "   Then log out and log back in." >&2
            echo "" >&2
            echo "   Without this, ComfyUI will run in slow CPU mode." >&2
            echo "   (This is a one-time setup, not an AppImage issue)" >&2
            echo "" >&2
        fi
    else
        echo "" >&2
        echo "⚠️  WARNING: AMD GPU detected but /dev/kfd not found" >&2
        echo "   ROCm kernel driver may not be installed" >&2
        echo "   GPU acceleration will not work" >&2
        echo "" >&2
    fi
else
    echo "ℹ️  No discrete GPU detected - using CPU-only backend (CUDA)" >&2
    PYTORCH_BACKEND="cuda"  # CUDA build works fine for CPU
fi

# Auto-detect Python version
PYTHON_VERSION=$(find "${APPDIR}/usr/lib" -maxdepth 1 -name "python*" -type d | head -1)
PYTHON_VERSION=$(basename "$PYTHON_VERSION" 2>/dev/null || echo "python3.12")

# Return the absolute backend directory path (to stdout only)
echo "${APPDIR}/usr/lib/${PYTHON_VERSION}/site-packages-${PYTORCH_BACKEND}"
