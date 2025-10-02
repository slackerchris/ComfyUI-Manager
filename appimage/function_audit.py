#!/usr/bin/env python3
"""
Function-by-function audit
"""
import ast

with open('ComfyUI.AppDir/comfyui_qt_manager.py', 'r', encoding='utf-8') as f:
    tree = ast.parse(f.read())

print("=" * 80)
print("FUNCTION-BY-FUNCTION AUDIT")
print("=" * 80)

classes = {}
functions = []

for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        classes[node.name] = node.lineno
    elif isinstance(node, ast.FunctionDef):
        if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
            functions.append((node.name, node.lineno))

print("\n[CLASSES]")
for name, line in classes.items():
    print(f"  • {name} (line {line})")

print("\n[TOP-LEVEL FUNCTIONS]")
for name, line in functions:
    print(f"  • {name}() (line {line})")

print("\n[KEY METHODS TO REVIEW]")
print("\n  ProcessMonitor class:")
print("    • run() - Background monitoring loop")
print("    • stop() - Cleanup")
print("    • get_comfyui_status() - Process detection")

print("\n  ComfyUIManager class:")
print("    • start_comfyui() - ⭐ CRITICAL - subprocess launch")
print("    • check_startup_success() - ⭐ CRITICAL - startup validation")
print("    • stop_comfyui() - Process termination")
print("    • restart_comfyui() - Restart logic")
print("    • quit_application() - Cleanup on exit")

print("\n" + "=" * 80)
print("CHECKING CRITICAL METHODS")
print("=" * 80)

with open('ComfyUI.AppDir/comfyui_qt_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find start_comfyui
print("\n✓ start_comfyui() analysis:")
in_start = False
start_line = 0
for i, line in enumerate(lines, 1):
    if 'def start_comfyui(self):' in line:
        in_start = True
        start_line = i
    elif in_start and line.strip().startswith('def ') and 'start_comfyui' not in line:
        print(f"    Lines {start_line}-{i-1} ({i-start_line} lines)")
        break

# Find check_startup_success
print("\n✓ check_startup_success() analysis:")
in_check = False
check_line = 0
for i, line in enumerate(lines, 1):
    if 'def check_startup_success(self):' in line:
        in_check = True
        check_line = i
    elif in_check and line.strip().startswith('def ') and 'check_startup' not in line:
        print(f"    Lines {check_line}-{i-1} ({i-check_line} lines)")
        break

print("\n" + "=" * 80)
