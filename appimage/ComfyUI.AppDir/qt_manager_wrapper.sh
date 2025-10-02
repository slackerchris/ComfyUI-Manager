#!/bin/bash
# ComfyUI Manager Process Wrapper
# This script preserves environment and sets the process name before launching Python

# Preserve all environment variables and set process name
exec -a "ComfyUI-Manager" env \
    "APPDIR=${APPDIR}" \
    "PYTHONPATH=${PYTHONPATH}" \
    "PYTHONHOME=${PYTHONHOME}" \
    "LD_LIBRARY_PATH=${LD_LIBRARY_PATH}" \
    "QT_PLUGIN_PATH=${QT_PLUGIN_PATH}" \
    "QT_QPA_PLATFORM_PLUGIN_PATH=${QT_QPA_PLATFORM_PLUGIN_PATH}" \
    "QML2_IMPORT_PATH=${QML2_IMPORT_PATH}" \
    "QT_WAYLAND_SHELL_INTEGRATION_PATH=${QT_WAYLAND_SHELL_INTEGRATION_PATH}" \
    "$@"