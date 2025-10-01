#!/usr/bin/env python3
"""
Minimal Qt test to isolate the bus error in AppImage environment
"""
import sys
import os

def test_qt_step_by_step():
    """Test Qt initialization step by step to find exact failure point"""
    print("🔍 Step-by-step Qt test starting...")
    print(f"Python: {sys.executable}")
    print(f"Working dir: {os.getcwd()}")
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
    print(f"PYTHONHOME: {os.environ.get('PYTHONHOME', 'Not set')}")
    
    try:
        print("1️⃣ Testing basic imports...")
        print("   ✅ sys already imported")
        
        print("2️⃣ Testing PySide6 import...")
        import PySide6
        print("   ✅ PySide6 imported")
        
        print("3️⃣ Testing QtCore import...")
        from PySide6 import QtCore
        print("   ✅ QtCore imported")
        
        print("4️⃣ Testing QCoreApplication import...")
        from PySide6.QtCore import QCoreApplication
        print("   ✅ QCoreApplication imported")
        
        print("5️⃣ Testing QApplication import...")
        from PySide6.QtWidgets import QApplication
        print("   ✅ QApplication imported")
        
        print("6️⃣ Testing QApplication creation (this might crash)...")
        # This is where the bus error likely occurs
        app = QCoreApplication(sys.argv)  # Try core first, safer
        print("   ✅ QCoreApplication created")
        
        print("7️⃣ Testing QApplication with widgets...")
        # Only try this if core app works
        app2 = QApplication(sys.argv)
        print("   ✅ QApplication created")
        
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Failed at step: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_qt_step_by_step()