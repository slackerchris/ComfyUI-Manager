#!/usr/bin/env python3
"""
Complete code review for comfyui_qt_manager.py
"""
import re

with open('ComfyUI.AppDir/comfyui_qt_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=" * 80)
print("COMPREHENSIVE CODE REVIEW - comfyui_qt_manager.py")
print("=" * 80)

issues = []

# Check 1: subprocess.PIPE usage (should be DEVNULL)
print("\n[1] Checking for subprocess.PIPE (should be DEVNULL)...")
for i, line in enumerate(lines, 1):
    if 'subprocess.PIPE' in line:
        issues.append(f"Line {i}: Found subprocess.PIPE - should be DEVNULL")
        print(f"  ❌ Line {i}: {line.strip()}")
if not any('subprocess.PIPE' in line for line in lines):
    print("  ✅ No subprocess.PIPE found (good)")

# Check 2: communicate() calls
print("\n[2] Checking for communicate() calls...")
for i, line in enumerate(lines, 1):
    if 'communicate()' in line:
        issues.append(f"Line {i}: Found communicate() call")
        print(f"  ❌ Line {i}: {line.strip()}")
if not any('communicate()' in line for line in lines):
    print("  ✅ No communicate() calls found (good)")

# Check 3: Hardcoded python3.12 in PYTHONPATH
print("\n[3] Checking for hardcoded python3.12...")
pythonpath_hardcoded = False
for i, line in enumerate(lines, 1):
    if 'python3.12' in line and 'PYTHONPATH' in line:
        issues.append(f"Line {i}: Hardcoded python3.12 in PYTHONPATH")
        print(f"  ❌ Line {i}: {line.strip()}")
        pythonpath_hardcoded = True
if not pythonpath_hardcoded:
    print("  ✅ No hardcoded python3.12 in PYTHONPATH (good)")

# Check 4: Dynamic Python version detection
print("\n[4] Checking for dynamic Python version detection...")
has_dynamic_detection = False
for i, line in enumerate(lines, 1):
    if 'python_version = None' in line or 'for item in os.listdir(python_lib_dir)' in line:
        has_dynamic_detection = True
        print(f"  ✅ Line {i}: Found dynamic detection code")
        break
if not has_dynamic_detection:
    issues.append("Missing dynamic Python version detection")
    print("  ❌ No dynamic Python version detection found")

# Check 5: PYTHONPATH includes stdlib
print("\n[5] Checking if PYTHONPATH includes stdlib...")
has_stdlib = False
for i, line in enumerate(lines, 1):
    if 'stdlib' in line and ('site_packages' in lines[i-2:i+2] if i > 2 else False):
        has_stdlib = True
        print(f"  ✅ Line {i}: Found stdlib in PYTHONPATH setup")
        break
if not has_stdlib:
    issues.append("PYTHONPATH may not include stdlib")
    print("  ❌ stdlib may not be in PYTHONPATH")

# Check 6: text=True with DEVNULL (incompatible)
print("\n[6] Checking for text=True with DEVNULL (incompatible)...")
for i, line in enumerate(lines, 1):
    if 'text=True' in line:
        # Check nearby lines for DEVNULL
        context = ''.join(lines[max(0,i-5):min(len(lines),i+5)])
        if 'DEVNULL' in context:
            issues.append(f"Line {i}: text=True with DEVNULL (unnecessary)")
            print(f"  ⚠️  Line {i}: {line.strip()}")
if not any('text=True' in line for line in lines):
    print("  ✅ No text=True found (good for DEVNULL)")

# Check 7: Exception handling for subprocess
print("\n[7] Checking subprocess exception handling...")
has_preexec_fallback = False
for i, line in enumerate(lines, 1):
    if 'except Exception as preexec_error' in line:
        has_preexec_fallback = True
        print(f"  ✅ Line {i}: Found preexec_fn fallback exception handling")
if not has_preexec_fallback:
    print("  ⚠️  No preexec_fn fallback found")

# Check 8: Process monitoring thread
print("\n[8] Checking ProcessMonitor thread safety...")
has_stop_method = False
for i, line in enumerate(lines, 1):
    if 'def stop(self):' in line and i < 100:  # Should be in ProcessMonitor class
        has_stop_method = True
        print(f"  ✅ Line {i}: ProcessMonitor has stop() method")
if not has_stop_method:
    issues.append("ProcessMonitor missing stop() method")
    print("  ❌ ProcessMonitor missing stop() method")

# Check 9: Memory leaks - check for proper cleanup
print("\n[9] Checking for proper cleanup in quit_application...")
has_monitor_cleanup = False
for i, line in enumerate(lines, 1):
    if 'process_monitor.stop()' in line:
        has_monitor_cleanup = True
        print(f"  ✅ Line {i}: ProcessMonitor cleanup found")
if not has_monitor_cleanup:
    issues.append("ProcessMonitor may not be properly cleaned up")
    print("  ❌ ProcessMonitor cleanup not found")

# Check 10: Qt platform setup
print("\n[10] Checking Qt platform setup...")
has_qt_setup = False
for i, line in enumerate(lines, 1):
    if 'setup_qt_platform()' in line and i < 50:
        has_qt_setup = True
        print(f"  ✅ Line {i}: Qt platform setup called before imports")
if not has_qt_setup:
    issues.append("Qt platform setup not called")
    print("  ❌ Qt platform setup not called")

# Summary
print("\n" + "=" * 80)
print("REVIEW SUMMARY")
print("=" * 80)
if issues:
    print(f"\n❌ FOUND {len(issues)} ISSUE(S):\n")
    for issue in issues:
        print(f"  • {issue}")
    print("\n⚠️  FILE NEEDS FIXES BEFORE BUILDING")
else:
    print("\n✅ ALL CHECKS PASSED - FILE IS READY FOR BUILD")

print("\n" + "=" * 80)
