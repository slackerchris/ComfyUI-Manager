#!/usr/bin/env python3
"""
Test Qt Manager with Wayland platform
"""
import sys
import os

def test_wayland_platform():
    """Test Qt with Wayland platform"""
    print("🔍 Testing Qt with Wayland platform...")
    
    # Set Qt to use Wayland
    os.environ['QT_QPA_PLATFORM'] = 'wayland'
    
    try:
        from PySide6.QtWidgets import QApplication
        print("✅ PySide6 imported")
        
        print("🎯 Creating QApplication with Wayland...")
        app = QApplication([])
        print("✅ QApplication created with Wayland")
        
        print("🎉 Qt works with Wayland!")
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ Wayland failed: {e}")
        
        # Try auto-detection
        try:
            print("🎯 Trying auto-platform detection...")
            if 'QT_QPA_PLATFORM' in os.environ:
                del os.environ['QT_QPA_PLATFORM']
                
            app = QApplication([])
            print("✅ Auto-detection worked!")
            app.quit()
            return True
            
        except Exception as e2:
            print(f"❌ Auto-detection failed: {e2}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    test_wayland_platform()