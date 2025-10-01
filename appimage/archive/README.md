# AppImage Archive Structure

This directory contains archived files from the ComfyUI Manager development process.

## Structure

- `old-appimages/` - Previous AppImage builds (for rollback if needed)
- `test-scripts/` - Qt testing scripts used during debugging
- `logs/` - Build and test logs from development
- `build-tools/` - AppImage building tools (appimagetool, etc.)

## Current Production Version

The current production-ready AppImage is in the parent directory:
- `ComfyUI-Manager-v2.0.5-x86_64.AppImage` - Latest stable build

## Cleanup Notes

These archived files can be safely deleted after confirming v2.0.5 is stable.
They are kept temporarily for debugging purposes if issues arise.