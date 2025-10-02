#!/bin/bash
echo "================================================================================"
echo "FINAL VERIFICATION - All Critical Code Sections"
echo "================================================================================"
echo ""

echo "✓ CHECK 1: Dynamic Python Detection (lines 621-632)"
sed -n '621,632p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "for item in os.listdir" && echo "  ✅ PASS" || echo "  ❌ FAIL"

echo ""
echo "✓ CHECK 2: PYTHONPATH includes stdlib (line 641)"
sed -n '641p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "stdlib" && echo "  ✅ PASS" || echo "  ❌ FAIL"

echo ""
echo "✓ CHECK 3: subprocess.DEVNULL (line 666)"
sed -n '666p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "DEVNULL" && echo "  ✅ PASS" || echo "  ❌ FAIL"

echo ""
echo "✓ CHECK 4: subprocess.DEVNULL fallback (line 676)"
sed -n '676p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "DEVNULL" && echo "  ✅ PASS" || echo "  ❌ FAIL"

echo ""
echo "✓ CHECK 5: No communicate() in check_startup_success"
sed -n '695,710p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "communicate()" && echo "  ❌ FAIL" || echo "  ✅ PASS"

echo ""
echo "✓ CHECK 6: No subprocess.PIPE anywhere"
grep -q "subprocess.PIPE" ComfyUI.AppDir/comfyui_qt_manager.py && echo "  ❌ FAIL" || echo "  ✅ PASS"

echo ""
echo "✓ CHECK 7: Python syntax valid"
python3 -m py_compile ComfyUI.AppDir/comfyui_qt_manager.py 2>&1 && echo "  ✅ PASS" || echo "  ❌ FAIL"

echo ""
echo "================================================================================"
echo "FINAL VERDICT:"
echo "================================================================================"

# All checks
if sed -n '621,632p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "for item in os.listdir" && \
   sed -n '641p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "stdlib" && \
   sed -n '666p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "DEVNULL" && \
   sed -n '676p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "DEVNULL" && \
   ! sed -n '695,710p' ComfyUI.AppDir/comfyui_qt_manager.py | grep -q "communicate()" && \
   ! grep -q "subprocess.PIPE" ComfyUI.AppDir/comfyui_qt_manager.py && \
   python3 -m py_compile ComfyUI.AppDir/comfyui_qt_manager.py 2>&1 > /dev/null; then
    echo "✅ ALL CRITICAL CHECKS PASSED - READY TO BUILD v2.4.0"
else
    echo "❌ SOME CHECKS FAILED - DO NOT BUILD"
fi
echo ""
