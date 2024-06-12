# Flight Software for the PyCubed Board (Argus-1)

The repository contains the current flight software stack for the **PyCubed Board** within Argus-1. Argus-1 is a technology demonstration mission with the goal of (not exhaustive):
- Demonstrating Visual Attitude and Orbit Determination (A&OD) on a low-cost satellite (Independance from any GPS or ground involvement in the A&OD process)
- Collecting a dataset of images of the Earth to further efforts in CubeSat visual applications.
- Demonstrating efficient on-orbit ML/GPU Payload processing 

## Moving files to the board

```bash
chmod +x setup.sh && ./setup.sh
```

Building and moving to the flight software code to the Argus board can be automated using the build.py and move_to_board.py script. It automatically updates all changes (including adding and deleting files).

```bash
./build_move_board.sh
```
or 

```bash
python build.py
python move_to_board.py -s <source_folder_path> -d <destination_folder_path>
```


