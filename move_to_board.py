import os
import shutil
import filecmp
import argparse

ARGUS_PATH = "D:\\"

def copy_folder(source_folder, destination_folder, show_identical_files=True):
    # In destination path creat SD folder
    sd_folder = os.path.join(destination_folder, "SD")
    if not os.path.exists(sd_folder):
        os.makedirs(sd_folder)
    
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source_folder)
            destination_path = os.path.join(destination_folder, relative_path)

            if not os.path.exists(os.path.dirname(destination_path)):
                os.makedirs(os.path.dirname(destination_path))

            if not os.path.exists(destination_path):
                shutil.copy2(source_path, destination_path)
                print(f"Copied {source_path} to {destination_path}")
            else:
                if filecmp.cmp(source_path, destination_path):
                    if show_identical_files:
                        print(f"File {source_path} already exists and is identical.")
                else:
                    shutil.copy2(source_path, destination_path)
                    print(f"Overwrote {destination_path} with {source_path}")

    # Delete files in destination folder that are not in the new copy
    for root, dirs, files in os.walk(destination_folder):
        for file in files:
            destination_path = os.path.join(root, file)
            relative_path = os.path.relpath(destination_path, destination_folder)
            source_path = os.path.join(source_folder, relative_path)

            # if not os.path.exists(source_path):
                # os.remove(destination_path)
                # print(f"Deleted {destination_path}")


if __name__ == "__main__":

    # Parses command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--source_folder",
        type=str,
        default="flight-software/build",
        help="Source folder path",
    )
    parser.add_argument(
        "-d",
        "--destination_folder",
        type=str,
        default=ARGUS_PATH,
        help="Destination folder path",
    )
    args = parser.parse_args()

    source_folder = args.source_folder
    destination_folder = args.destination_folder

    """source_folder = "flight-software"
    destination_folder = '/media/ibrahima/PYCUBED'"""

    copy_folder(source_folder, destination_folder, show_identical_files=True)
