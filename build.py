import os
import subprocess
import shutil
import filecmp
import argparse
import platform

if platform.system() == "Windows":
    BOARD_PATH = "D:\\"
elif platform.system() == "Linux":
    username = subprocess.check_output("whoami", shell=True).decode().strip()
    BOARD_PATH = f"/media/{username}/ARGUS"
    if not os.path.exists(BOARD_PATH):
        BOARD_PATH = f"/media/{username}/PYCUBED"

MPY_CROSS_PATH = f"{os.getcwd()}/mpy-cross"


def check_directory_location(source_folder):
    if not os.path.exists(BOARD_PATH):
        raise FileNotFoundError(f"Destination folder {BOARD_PATH} not found")

    if not os.path.exists(MPY_CROSS_PATH):
        raise FileNotFoundError(f"MPY_CROSS_PATH folder {MPY_CROSS_PATH} not found")

    if not os.path.exists(f"./source_folder"):
        raise FileNotFoundError(f"Source folder {source_folder} not found")



def create_build(source_folder):
    build_folder = os.path.join(source_folder, "build/")
    if os.path.exists(build_folder):
        shutil.rmtree(build_folder)

    build_folder = os.path.join(build_folder, "lib/")

    os.makedirs(build_folder)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # Exclude files in build folder
            if os.path.relpath(root, source_folder).startswith("build/"):
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

                if file == "main.py":
                    # rename main.py to main_module.py
                    os.rename("main.py", "main_module.py")
                    file_name = "main_module.py"
                else:
                    # Extract file name
                    file_name = os.path.basename(file)

                relative_path = os.path.relpath(source_folder, build_path)

                os.system(f"{relative_path}/mpy-cross {file_name}")

                # Delete file python file once it has been compiled
                os.remove(file_name)

                os.chdir(current_dir)

        # Create main.py file with single import statement "import main_module"
        with open(os.path.join(build_folder, "main.py"), "w") as f:
            f.write("import main_module\n")

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
        required=False
    )
    parser.add_argument(
        "-d",
        "--destination_folder",
        type=str,
        default=BOARD_PATH,
        help="Destination folder path",
        required=False
    )
    args = parser.parse_args()

    source_folder = args.source_folder
    destination_folder = args.destination_folder

    build_folder = create_build(source_folder)



    
