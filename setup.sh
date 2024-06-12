#!/bin/bash

# Detect the operating system
OS=$(uname -s)

# Set the correct mpy-cross executable based on the OS
if [ "$OS" == "Linux" ]; then
    MPY_EXEC="mpy-cross"
elif [ "$OS" == "Darwin" ]; then
    MPY_EXEC="mpy-cross-macos"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

# Make the correct mpy-cross executable
chmod +x $MPY_EXEC

echo "$MPY_EXEC is now executable"