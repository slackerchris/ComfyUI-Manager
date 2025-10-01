#!/usr/bin/env python3
"""
Simple Qt test to isolate PySide6 issues in AppImage environment
"""
import sys
import os

print("🔍 Qt Test Starting...")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

try:
    print("📦 Testing PySide6 import...")
    from PySide6.QtWidgets import QApplication
    print("✅ PySide6.QtWidgets imported successfully")
    
    print("🎯 Testing QApplication creation...")
    app = QApplication(sys.argv)
    print("✅ QApplication created successfully")
    
    print("🧪 Testing basic widget...")
    from PySide6.QtWidgets import QLabel
    label = QLabel("Test")
    print("✅ QLabel created successfully")
    
    print("🎉 Qt test completed successfully!")
    app.quit()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Qt error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)