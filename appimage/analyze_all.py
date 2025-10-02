#!/usr/bin/env python3
"""
Line-by-line comprehensive analysis of comfyui_qt_manager.py
"""
import ast
import sys

print("=" * 80)
print("COMPREHENSIVE LINE-BY-LINE CODE ANALYSIS")
print("=" * 80)

try:
    with open('ComfyUI.AppDir/comfyui_qt_manager.py', 'r', encoding='utf-8') as f:
        code = f.read()
        
    # Parse the AST
    tree = ast.parse(code)
    
    issues = []
    warnings = []
    
    print("\n[ANALYZING FUNCTIONS AND METHODS]\n")
    
    for node in ast.walk(tree):
        # Check all function definitions
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            line_no = node.lineno
            
            # Check for subprocess.Popen calls
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Attribute):
                        if (isinstance(child.func.value, ast.Name) and 
                            child.func.value.id == 'subprocess' and 
                            child.func.attr == 'Popen'):
                            
                            # Check the arguments
                            has_pipe = False
                            has_devnull = False
                            has_text = False
                            
                            for keyword in child.keywords:
                                if keyword.arg in ['stdout', 'stderr']:
                                    if isinstance(keyword.value, ast.Attribute):
                                        if (isinstance(keyword.value.value, ast.Name) and
                                            keyword.value.value.id == 'subprocess'):
                                            if keyword.value.attr == 'PIPE':
                                                has_pipe = True
                                            elif keyword.value.attr == 'DEVNULL':
                                                has_devnull = True
                                elif keyword.arg == 'text':
                                    if isinstance(keyword.value, ast.Constant):
                                        if keyword.value.value is True:
                                            has_text = True
                            
                            if has_pipe:
                                issues.append(f"  ❌ Line {child.lineno}: {func_name}() - subprocess.PIPE detected")
                            elif has_devnull:
                                print(f"  ✅ Line {child.lineno}: {func_name}() - subprocess.DEVNULL (correct)")
                                if has_text:
                                    warnings.append(f"  ⚠️  Line {child.lineno}: {func_name}() - text=True unnecessary with DEVNULL")
                
                # Check for communicate() calls
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Attribute):
                        if child.func.attr == 'communicate':
                            issues.append(f"  ❌ Line {child.lineno}: {func_name}() - communicate() call detected")
                
                # Check for QTimer.singleShot
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Attribute):
                        if (isinstance(child.func.value, ast.Name) and
                            child.func.value.id == 'QTimer' and
                            child.func.attr == 'singleShot'):
                            print(f"  📍 Line {child.lineno}: {func_name}() - QTimer.singleShot found")
    
    print("\n" + "=" * 80)
    print("ISSUES FOUND")
    print("=" * 80)
    
    if issues:
        print("\n❌ CRITICAL ISSUES:")
        for issue in issues:
            print(issue)
    else:
        print("\n✅ No critical issues found")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(warning)
    else:
        print("\n✅ No warnings")
    
    print("\n" + "=" * 80)
    
    # Check for potential race conditions or logic errors
    print("\n[CHECKING FOR COMMON PATTERNS]\n")
    
    with open('ComfyUI.AppDir/comfyui_qt_manager.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Pattern checks
    print("Pattern Analysis:")
    print(f"  • Total lines: {len(lines)}")
    print(f"  • subprocess.Popen calls: {code.count('subprocess.Popen')}")
    print(f"  • subprocess.DEVNULL: {code.count('subprocess.DEVNULL')}")
    print(f"  • subprocess.PIPE: {code.count('subprocess.PIPE')}")
    print(f"  • .communicate(): {code.count('.communicate()')}")
    print(f"  • QTimer.singleShot: {code.count('QTimer.singleShot')}")
    print(f"  • try/except blocks: {code.count('try:')}")
    
    if issues or warnings:
        print("\n⚠️  CODE NEEDS REVIEW")
        sys.exit(1)
    else:
        print("\n✅ ALL CHECKS PASSED")
        sys.exit(0)
        
except SyntaxError as e:
    print(f"\n❌ SYNTAX ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ANALYSIS ERROR: {e}")
    sys.exit(1)
