#!/usr/bin/env python3
"""
Device Check Script for ComfyUI Universal AppImage
Shows whether GPU or CPU mode is actually being used
"""

import sys
import os

def check_device():
    """Check what device PyTorch is actually using"""
    
    print("\n" + "="*70)
    print("🔍 DEVICE CHECK - GPU vs CPU Mode")
    print("="*70)
    
    try:
        import torch
        
        # Basic PyTorch info
        print(f"\n✅ PyTorch Version: {torch.__version__}")
        print(f"✅ PyTorch Location: {torch.__file__}")
        
        # CUDA availability (works for both NVIDIA CUDA and AMD ROCm)
        cuda_available = torch.cuda.is_available()
        print(f"\n🔧 CUDA API Available: {cuda_available}")
        
        if cuda_available:
            # Get device info
            device_count = torch.cuda.device_count()
            current_device = torch.cuda.current_device()
            device_name = torch.cuda.get_device_name(current_device)
            device_props = torch.cuda.get_device_properties(current_device)
            
            print(f"\n✅ GPU MODE ENABLED")
            print(f"   Devices Found: {device_count}")
            print(f"   Current Device: {current_device}")
            print(f"   Device Name: {device_name}")
            print(f"   Total Memory: {device_props.total_memory / 1024**3:.2f} GB")
            
            # Try to detect if it's ROCm or CUDA
            if 'rocm' in torch.__version__.lower():
                print(f"   Backend: ROCm (AMD GPU)")
            elif 'cu' in torch.__version__.lower():
                print(f"   Backend: CUDA (NVIDIA GPU)")
            else:
                print(f"   Backend: Unknown")
                
            # Test tensor creation on GPU
            try:
                test_tensor = torch.randn(10, 10).cuda()
                print(f"\n✅ GPU Tensor Test: SUCCESS")
                print(f"   Tensor Device: {test_tensor.device}")
            except Exception as e:
                print(f"\n⚠️  GPU Tensor Test: FAILED - {e}")
                
        else:
            print(f"\n⚠️  CPU MODE - No GPU acceleration")
            print(f"   Reason: torch.cuda.is_available() returned False")
            
            # Check for common AMD GPU issues
            if 'rocm' in torch.__version__.lower():
                print(f"\n   🔍 Diagnosing AMD GPU issues...")
                
                # Check /dev/kfd access
                import os
                if os.path.exists('/dev/kfd'):
                    if os.access('/dev/kfd', os.R_OK | os.W_OK):
                        print(f"   ✅ /dev/kfd is accessible")
                    else:
                        print(f"   ❌ /dev/kfd exists but NOT accessible")
                        print(f"   ")
                        print(f"   🔧 FIX: Add your user to the 'render' group:")
                        print(f"      sudo usermod -a -G render $USER")
                        print(f"      Then log out and log back in")
                        print(f"   ")
                        return 1
                else:
                    print(f"   ❌ /dev/kfd not found - ROCm kernel driver missing")
                
                # Check if in render group
                import grp
                try:
                    render_gid = grp.getgrnam('render').gr_gid
                    user_groups = os.getgroups()
                    if render_gid in user_groups:
                        print(f"   ✅ User is in 'render' group")
                    else:
                        print(f"   ❌ User is NOT in 'render' group")
                        print(f"   ")
                        print(f"   🔧 FIX: Add your user to the 'render' group:")
                        print(f"      sudo usermod -a -G render $USER")
                        print(f"      Then log out and log back in")
                        print(f"   ")
                        return 1
                except KeyError:
                    print(f"   ⚠️  'render' group does not exist")
                
                print(f"\n   Other possible reasons:")
                print(f"   - GPU not compatible with ROCm 6.2")
                print(f"   - ROCm runtime environment issue")
            else:
                print(f"\n   Possible reasons:")
                print(f"   - No NVIDIA GPU detected")
                print(f"   - NVIDIA drivers not installed")
            
    except ImportError as e:
        print(f"\n❌ ERROR: Could not import PyTorch - {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "="*70 + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(check_device())
