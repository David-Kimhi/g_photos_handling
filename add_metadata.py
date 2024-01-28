import piexif
import json
import os


def add_metadata_to_media(file_path):
    """
    This function add the missing metadata to the image file from the json file
    (google gives it the same name with different extension)
    In case of success the function deletes the json file
    :param file_path: (str) full path to the image or video file
    :return: tuple - exit code (int), exit message (str)
    """
    # Derive the JSON file path from the media file path
    ext_name = os.path.splitext(file_path)[1]

    # if the file is json or not video or image
    if not ext_name or ext_name == '.json':
        return -2, 'not an image or video file'

    json_file = file_path + '.json'

    # Check if the JSON file exists
    if not os.path.exists(json_file):
        return -1, f"JSON file does not exist"

    # Load metadata from JSON file
    with open(json_file, 'r') as file:
        metadata = json.load(file)

    # Load EXIF data from the media file
    try:
        exif_dict = piexif.load(file_path)
    except:
        return -1, f"Could not load EXIF data from file. This file may not support EXIF data."

    # Assign values from json to the piexif data
    for tag, value in metadata.items():
        # Check if the tag is a standard tag in piexif.ImageIFD
        if hasattr(piexif.ImageIFD, tag):
            exif_tag = getattr(piexif.ImageIFD, tag)
        else:
            continue

        exif_dict['0th'][exif_tag] = value

    try:
        # Convert EXIF dictionary to bytes
        exif_bytes = piexif.dump(exif_dict)
    except Exception as e:
        return -1, str(e)

    # Insert the new EXIF data into the image
    try:
        piexif.insert(exif_bytes, file_path)
    except Exception as e:
        return -1, f"Could not insert metadata into file. This file may not support EXIF data."

    os.remove(json_file)
    return 0, ''
