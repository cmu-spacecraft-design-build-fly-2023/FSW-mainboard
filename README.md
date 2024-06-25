# Flight Software for the PyCubed Board (Argus-1)

The repository contains the current flight software stack for the **PyCubed Board** within Argus-1. Argus-1 is a technology demonstration mission with the goal of (not exhaustive):
- Demonstrating Visual Attitude and Orbit Determination (A&OD) on a low-cost satellite (Independance from any GPS or ground involvement in the A&OD process)
- Collecting a dataset of images of the Earth to further efforts in CubeSat visual applications.
- Demonstrating efficient on-orbit ML/GPU Payload processing 

## Build and Execution

Building current files and moving them to the board can be handled by the run.sh script which can be run via:
```bash
./run.sh
```
This script first builds and compiles files to .mpy files and then transfers them to the mainboard you are connected to.

If you are not connected to a mainboard you should either run the simulator or emulator.

To run the emulator:
```bash
./run.sh emulate
```

To run the simulator:
```bash
./run.sh simulate
```


If you want to just do one of build or move to the baord then building and moving to the flight software code to the Argus board can be automated using the build.py and move_to_board.py scripts in the build_tools directory. It automatically updates all changes (including adding and deleting files).

To build:
```bash
python3 build_tools/build.py
```
or for emulation
```bash
python3 build_tools/build-emulator.py
```

To move to board:
```bash
python move_to_board.py -s <source_folder_path> -d <destination_folder_path>
```


