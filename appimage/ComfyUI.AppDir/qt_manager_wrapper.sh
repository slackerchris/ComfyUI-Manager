#!/bin/bash
# ComfyUI Manager Process Wrapper
# This script sets the process name before launching Python

# Set process name using exec -a (most visible method)
exec -a "ComfyUI-Manager" "$@"