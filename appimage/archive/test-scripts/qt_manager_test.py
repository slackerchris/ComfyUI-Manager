#!/usr/bin/env python3
"""
Test that matches our Qt Manager's initialization pattern
"""
import sys
import os

def test_qt_manager_pattern():
    """Test the exact pattern our Qt Manager uses"""
    print("🔍 Testing Qt Manager initialization pattern...")
    
    try:
        # Exact imports from our Qt manager
        from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon
        from PySide6.QtCore import QTimer, Qt
        from PySide6.QtGui import QIcon, QAction
        print("✅ All Qt imports successful")
        
        # Test QApplication creation (the most likely crash point)
        print("🎯 Creating QApplication...")
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        # Test system tray (another potential crash point)
        print("🎯 Testing system tray availability...")
        if QSystemTrayIcon.isSystemTrayAvailable():
            print("✅ System tray available")
            
            # Test creating system tray icon
            print("🎯 Creating system tray icon...")
            tray = QSystemTrayIcon()
            print("✅ System tray icon created")
        else:
            print("⚠️ System tray not available")
        
        # Test main window creation
        print("🎯 Creating main window...")
        window = QMainWindow()
        print("✅ Main window created")
        
        # Test setting window properties
        print("🎯 Setting window properties...")
        window.setWindowTitle("ComfyUI Manager Test")
        window.resize(800, 600)
        print("✅ Window properties set")
        
        print("🎉 All Qt Manager patterns work!")
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_qt_manager_pattern()