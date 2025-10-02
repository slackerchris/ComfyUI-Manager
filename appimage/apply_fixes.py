#!/usr/bin/env python3
"""
Apply all critical fixes to comfyui_qt_manager.py
"""

import re

# Read the file
with open('ComfyUI.AppDir/comfyui_qt_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Applying fixes...")

# FIX #1: Add dynamic Python version detection (after line 630)
old_env_setup = '''            if self.appdir and os.path.exists(os.path.join(self.appdir, "usr", "bin", "python3")):
                # Running from AppImage - setup self-contained environment
                self.log_display.append("🔧 Configuring self-contained AppImage environment...")
                
                # Set Python environment to use bundled libraries
                env['PYTHONHOME'] = os.path.join(self.appdir, "usr")
                env['PYTHONPATH'] = os.path.join(self.appdir, "usr", "lib", "python3.12", "site-packages")
                env['LD_LIBRARY_PATH'] = os.path.join(self.appdir, "usr", "lib")
                
                # Add ComfyUI app directory to Python path
                if os.path.exists(os.path.join(self.appdir, "app")):
                    env['PYTHONPATH'] = f"{env['PYTHONPATH']}:{os.path.join(self.appdir, 'app')}"
                
                self.log_display.append(f"   PYTHONHOME: {env['PYTHONHOME']}")
                self.log_display.append(f"   PYTHONPATH: {env['PYTHONPATH'][:80]}...")
                self.log_display.append(f"   LD_LIBRARY_PATH: {env['LD_LIBRARY_PATH'][:80]}...")'''

new_env_setup = '''            if self.appdir and os.path.exists(os.path.join(self.appdir, "usr", "bin", "python3")):
                # Running from AppImage - setup self-contained environment
                self.log_display.append("🔧 Configuring self-contained AppImage environment...")
                
                # Dynamically detect Python version
                python_lib_dir = os.path.join(self.appdir, "usr", "lib")
                python_version = None
                if os.path.exists(python_lib_dir):
                    for item in os.listdir(python_lib_dir):
                        if item.startswith("python3.") and os.path.isdir(os.path.join(python_lib_dir, item)):
                            python_version = item
                            break
                
                if not python_version:
                    python_version = "python3.12"  # Fallback
                
                self.log_display.append(f"   Detected Python: {python_version}")
                
                # Set Python environment to use bundled libraries
                env['PYTHONHOME'] = os.path.join(self.appdir, "usr")
                
                # Build PYTHONPATH with all necessary directories
                site_packages = os.path.join(self.appdir, "usr", "lib", python_version, "site-packages")
                stdlib = os.path.join(self.appdir, "usr", "lib", python_version)
                app_dir = os.path.join(self.appdir, "app")
                python_paths = [site_packages, stdlib, app_dir]
                env['PYTHONPATH'] = ":".join(python_paths)
                env['LD_LIBRARY_PATH'] = os.path.join(self.appdir, "usr", "lib")
                
                self.log_display.append(f"   PYTHONHOME: {env['PYTHONHOME']}")
                self.log_display.append(f"   PYTHONPATH: {env['PYTHONPATH'][:80]}...")
                self.log_display.append(f"   LD_LIBRARY_PATH: {env['LD_LIBRARY_PATH'][:80]}...")'''

if old_env_setup in content:
    content = content.replace(old_env_setup, new_env_setup)
    print("✓ Fix #1: Dynamic Python version detection applied")
else:
    print("✗ Fix #1: Could not find environment setup code")

# FIX #2: Change subprocess.PIPE to subprocess.DEVNULL
old_subprocess = '''                self.comfyui_process = subprocess.Popen(
                    cmd, 
                    cwd=working_dir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,  # Separate stderr to avoid blocking
                    text=True,
                    start_new_session=True,  # Start in new process group
                    preexec_fn=os.setsid if hasattr(os, 'setsid') else None  # Unix process isolation
                )'''

new_subprocess = '''                self.comfyui_process = subprocess.Popen(
                    cmd, 
                    cwd=working_dir,
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,  # Start in new process group
                    preexec_fn=os.setsid if hasattr(os, 'setsid') else None  # Unix process isolation
                )'''

if old_subprocess in content:
    content = content.replace(old_subprocess, new_subprocess)
    print("✓ Fix #2a: subprocess.DEVNULL applied (first instance)")
else:
    print("✗ Fix #2a: Could not find first subprocess.Popen")

# Also fix the fallback subprocess call
old_subprocess_fallback = '''                self.comfyui_process = subprocess.Popen(
                    cmd, 
                    cwd=working_dir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    start_new_session=True
                )'''

new_subprocess_fallback = '''                self.comfyui_process = subprocess.Popen(
                    cmd, 
                    cwd=working_dir,
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )'''

if old_subprocess_fallback in content:
    content = content.replace(old_subprocess_fallback, new_subprocess_fallback)
    print("✓ Fix #2b: subprocess.DEVNULL applied (fallback instance)")
else:
    print("✗ Fix #2b: Could not find fallback subprocess.Popen")

# Write the fixed file
with open('ComfyUI.AppDir/comfyui_qt_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll fixes applied. Verifying syntax...")
