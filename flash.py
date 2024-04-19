import os
import shutil
import filecmp
import argparse

ARGUS_PATH = "D:\\"

def create_build(source_folder):
    
    build_folder = os.path.join(source_folder, "build")
    if os.path.exists(build_folder):
        shutil.rmtree(build_folder)
    
    os.makedirs(build_folder)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # Exclude files in build folder
            if os.path.relpath(root, source_folder).startswith("build"):
                continue

            if file.endswith(".py"):
                source_path = os.path.join(root, file)
                build_path = os.path.join(build_folder, os.path.relpath(source_path, source_folder))
                os.makedirs(os.path.dirname(build_path), exist_ok=True)
                shutil.copy2(source_path, build_path)
                print(f"Copied {source_path} to {build_path}")
                
                current_dir = os.getcwd()
                
                # Change directory to the build path folder
                os.chdir(os.path.dirname(build_path))
                
                # Extract file name
                file_name = os.path.basename(file)

                os.system(f"./mpy-cross {file_name}")

                # Delete file
                # os.remove(file)

                os.chdir(current_dir)

    return build_folder

def copy_folder(build_folder, destination_folder, show_identical_files=True):
    for root, dirs, files in os.walk(build_folder):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, build_folder)
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
            source_path = os.path.join(build_folder, relative_path)

            if not os.path.exists(source_path):
                os.remove(destination_path)
                print(f"Deleted {destination_path}")


if __name__ == "__main__":

    # Parses command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--source_folder",
        type=str,
        default="flight-software",
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

    print(source_folder)
    build_folder = create_build(source_folder)

    # copy_folder(build_folder, destination_folder, show_identical_files=True)
