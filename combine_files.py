import os
import shutil


def combine_files(path):
    """
    This function combine all the image and video files from the given directory (path var) to single directory inside path
    The function then deletes the empty directories
    :param path: the path to the google photos directory
    :return: None
    """
    # Define the directory name where you want to move your files
    target_directory_name = 'combined_files'
    target_directory_path = os.path.join(path, target_directory_name)

    # Define allowed extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.heic')
    video_extensions = ('.mp4', '.mov', '.wmv', '.flv', '.avi', '.mkv', '.webm')
    json_extension = '.json'

    # Create the target directory if it doesn't exist
    if not os.path.exists(target_directory_path):
        os.makedirs(target_directory_path)

    # Walk through the directory
    for dir_path, dir_names, filenames in os.walk(path):
        if dir_path == target_directory_path:
            # Skip the target directory
            continue

        for file in filenames:
            # Check if the file is a .jpg or .json file
            if file.lower().endswith(image_extensions + video_extensions + (json_extension,)):
                # Define the source and destination paths
                file_path = os.path.join(dir_path, file)
                destination = os.path.join(target_directory_path, file)

                # Move the file
                shutil.move(file_path, destination)
                print(f'Moved: {file_path} -> {destination}')

    # Walk through the directory again to remove empty directories
    for dir_path, dir_names, filenames in os.walk(path, topdown=False):
        if dir_path in (target_directory_path, path):
            # Skip the target directory and source directory
            continue
        # The directory is empty, remove it
        if not dir_names:
            if len(filenames) <= 1:
                if '.DS_Store' in filenames:
                    os.remove(os.path.join(dir_path, '.DS_Store'))
                elif len(filenames) == 1:
                    continue
                os.rmdir(dir_path)
                print(f'Removed empty directory: {dir_path}')
