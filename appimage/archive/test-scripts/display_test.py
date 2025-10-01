#!/usr/bin/env python3
"""
Test Qt Manager with display environment matching AppRun context
"""
import sys
import os

def test_with_display_env():
    """Test Qt with the same environment that AppRun provides"""
    print("🔍 Testing Qt with AppRun-like environment...")
    print(f"DISPLAY: {os.environ.get('DISPLAY', 'Not set')}")
    print(f"XDG_SESSION_TYPE: {os.environ.get('XDG_SESSION_TYPE', 'Not set')}")
    print(f"WAYLAND_DISPLAY: {os.environ.get('WAYLAND_DISPLAY', 'Not set')}")
    
    # Set Qt platform options that might help
    os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Force X11
    os.environ['QT_X11_NO_MITSHM'] = '1'   # Disable shared memory (common AppImage fix)
    
    try:
        from PySide6.QtWidgets import QApplication
        print("✅ PySide6 imported")
        
        # Create app with explicit arguments
        print("🎯 Creating QApplication with platform settings...")
        app = QApplication([
            'comfyui_qt_manager',
            '-platform', 'xcb'
        ])
        print("✅ QApplication created with platform settings")
        
        # Test if we can actually show something
        from PySide6.QtWidgets import QLabel
        label = QLabel("Test")
        label.show()
        print("✅ Widget shown")
        
        print("🎉 Qt works with display settings!")
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_with_display_env()