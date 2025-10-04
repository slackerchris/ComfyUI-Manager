#!/usr/bin/env python3
"""
ComfyUI Model Folders Configuration
====================================

Single Source of Truth for ALL ComfyUI model folder types.

This module defines the complete list of model folders that ComfyUI supports.
All components (AppRun, Qt Manager, YAML generation) use this single list
to ensure perfect synchronization.

Usage in Python:
    from model_folders import MODEL_FOLDERS
    for folder in MODEL_FOLDERS:
        # use it

Usage in Bash:
    FOLDERS=$(python3 model_folders.py --bash)
    mkdir -p "$BASE_DIR"/{$FOLDERS}

Adding a new model type:
    1. Add one line to MODEL_FOLDERS list below
    2. Done. All components automatically updated.

Version: 2.5.8
"""

# Complete list of ComfyUI model folder types
# Organized by category for clarity
MODEL_FOLDERS = [
    # Core Model Types
    'checkpoints',      # Main SD/SDXL checkpoint models
    'configs',          # Model configuration files
    'vae',              # VAE models for encoding/decoding
    'vae_approx',       # Approximate VAE for faster preview
    'loras',            # LoRA (Low-Rank Adaptation) models
    
    # Text & Vision Encoders
    'text_encoders',    # Text encoding models
    'clip',             # CLIP models for text-image understanding
    'clip_vision',      # CLIP vision encoders
    
    # Diffusion Models
    'diffusion_models', # Diffusion model components
    'unet',             # U-Net architectures
    'diffusers',        # HuggingFace diffusers format
    
    # ControlNet & Adapters
    'controlnet',       # ControlNet models for guided generation
    't2i_adapter',      # Text-to-Image adapters (T2I-Adapter)
    
    # Embeddings & Style
    'embeddings',       # Textual inversion embeddings
    'style_models',     # Style transfer models
    'hypernetworks',    # Hypernetwork models
    
    # Upscaling & Enhancement
    'upscale_models',   # Image upscaling models (ESRGAN, etc)
    
    # Video & Animation
    'animatediff',      # AnimateDiff models for video generation
    'video_models',     # Video generation models (SVD, etc)
    
    # Special Model Types
    'gligen',           # GLIGEN grounded text-to-image
    'photomaker',       # PhotoMaker customization models
    'classifiers',      # Classification models
    'model_patches',    # Model patches and modifications
    'audio_encoders',   # Audio encoding models
]


def get_folders_bash():
    """Return comma-separated list for bash brace expansion."""
    return ','.join(MODEL_FOLDERS)


def get_folders_yaml():
    """Return YAML-formatted entries for extra_model_paths.yaml."""
    lines = []
    for folder in MODEL_FOLDERS:
        lines.append(f"    {folder}: {folder}")
    return '\n'.join(lines)


def validate():
    """Validate the model folders list."""
    if len(MODEL_FOLDERS) != len(set(MODEL_FOLDERS)):
        duplicates = [f for f in MODEL_FOLDERS if MODEL_FOLDERS.count(f) > 1]
        raise ValueError(f"Duplicate folders found: {set(duplicates)}")
    
    for folder in MODEL_FOLDERS:
        if not folder.replace('_', '').replace('-', '').isalnum():
            raise ValueError(f"Invalid folder name: {folder}")
    
    return True


if __name__ == '__main__':
    import sys
    
    # Command-line interface for different output formats
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == '--bash':
            # For bash brace expansion: mkdir -p $DIR/{folder1,folder2,...}
            print(get_folders_bash())
        
        elif cmd == '--yaml':
            # For YAML generation in extra_model_paths.yaml
            print(get_folders_yaml())
        
        elif cmd == '--count':
            # Return count for validation
            print(len(MODEL_FOLDERS))
        
        elif cmd == '--validate':
            # Validate the list
            try:
                validate()
                print(f"✅ Valid: {len(MODEL_FOLDERS)} unique folders")
            except ValueError as e:
                print(f"❌ Invalid: {e}")
                sys.exit(1)
        
        elif cmd == '--list':
            # List all folders one per line
            for folder in MODEL_FOLDERS:
                print(folder)
        
        else:
            print(f"Unknown command: {cmd}", file=sys.stderr)
            print("Usage: model_folders.py [--bash|--yaml|--count|--validate|--list]", file=sys.stderr)
            sys.exit(1)
    
    else:
        # Default: print list for human reading
        print(f"ComfyUI Model Folders (v2.5.8)")
        print(f"{'='*50}")
        for i, folder in enumerate(MODEL_FOLDERS, 1):
            print(f"{i:2d}. {folder}")
        print(f"{'='*50}")
        print(f"Total: {len(MODEL_FOLDERS)} folders")
