#!/usr/bin/env python3
"""
Test script to verify Qt Manager button functionality
"""
import sys
import os
import time

# Add the ComfyUI.AppDir to path so we can import the manager
sys.path.insert(0, '/home/chris/Documents/Git/Projects/ComfyUI/appimage/ComfyUI.AppDir')

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer
    from comfyui_qt_manager import ComfyUIManager
    
    def test_buttons():
        """Test the start/stop/restart buttons programmatically"""
        print("🧪 Testing Qt Manager buttons...")
        
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        
        # Create manager instance
        manager = ComfyUIManager()
        
        def test_start_button():
            print("🔴 Testing START button...")
            try:
                manager.start_comfyui()
                print("✅ START button test completed without crash")
            except Exception as e:
                print(f"❌ START button test failed: {e}")
        
        def test_stop_button():
            print("🟡 Testing STOP button...")
            try:
                manager.stop_comfyui()
                print("✅ STOP button test completed without crash")
            except Exception as e:
                print(f"❌ STOP button test failed: {e}")
        
        def test_restart_button():
            print("🟢 Testing RESTART button...")
            try:
                manager.restart_comfyui()
                print("✅ RESTART button test completed without crash")
            except Exception as e:
                print(f"❌ RESTART button test failed: {e}")
        
        def cleanup():
            print("🏁 Test completed - cleaning up...")
            try:
                manager.quit_application()
            except Exception as e:
                print(f"Cleanup error: {e}")
            finally:
                app.quit()
        
        # Schedule tests
        QTimer.singleShot(1000, test_start_button)
        QTimer.singleShot(3000, test_stop_button)  
        QTimer.singleShot(5000, test_restart_button)
        QTimer.singleShot(7000, cleanup)
        
        # Run the test
        sys.exit(app.exec())
    
    if __name__ == "__main__":
        test_buttons()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure PySide6 and psutil are installed")