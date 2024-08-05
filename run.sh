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

if [[ -z $2 ]];
then
    export fake_time="n"
elif [ "$2" == "faketime" ];
then
    export fake_time="y"
fi

if [[ -z $1 ]];
then
    python3 build_tools/build.py && python3 build_tools/move_to_board.py
elif [ "$1" == "emulate" ];
then
    python3 build_tools/build-emulator.py
    cd build/ && python3 main.py
    cd -
elif [ "$1" == "simulate" ];
then
    export sim="y"
    python3 build_tools/build-emulator.py
    cd build/ && python3 main.py
    cd -
fi