#!/bin/bash
echo "==================================================================="
echo "METADATA & NON-FUNCTIONAL ISSUES CHECK"
echo "==================================================================="
echo ""

echo "[1] Checking for TODO/FIXME/HACK comments:"
grep -n "TODO\|FIXME\|HACK\|XXX" ComfyUI.AppDir/comfyui_qt_manager.py || echo "  ✓ None found"

echo ""
echo "[2] Checking for debug print statements:"
grep -n "^[[:space:]]*print(" ComfyUI.AppDir/comfyui_qt_manager.py | head -10

echo ""
echo "[3] Checking for hardcoded paths (home/chris):"
grep -n "/home/chris" ComfyUI.AppDir/comfyui_qt_manager.py || echo "  ✓ None found"

echo ""
echo "[4] Checking for inconsistent quotes:"
# Not critical but shows attention to detail
echo "  (Skipping - Python allows both)"

echo ""
echo "[5] Checking for unused imports:"
echo "  (Would need AST analysis - skipping)"

echo ""
echo "[6] Checking docstring consistency:"
grep -n '""".*"""' ComfyUI.AppDir/comfyui_qt_manager.py | head -5

echo ""
echo "[7] Checking for old issue references:"
grep -n "issue\|bug\|broken" ComfyUI.AppDir/comfyui_qt_manager.py || echo "  ✓ None found"

echo ""
echo "==================================================================="
