# imports
import sys
import os
import shutil
from tqdm import tqdm
from add_metadata import *
from combine_files import *


if __name__ == "__main__":

    # check arguments
    if len(sys.argv) <= 1:
        print("Please provide directory")
        exit()

    # first argument as the path to google photos dir
    path = sys.argv[1]

    # combine all files to single directory inside path
    combine_files(path=path)

    # prepare metadata execution details
    success_list = []
    failed_list = []
    failed_dict = dict()

    # path to new directory
    combine_files_dir = os.path.join(path, 'combined_files')

    # add metadata for each file
    for file in tqdm(os.listdir(combine_files_dir), desc='Json processing'):
        return_code, return_message = add_metadata_to_media(os.path.join(combine_files_dir, file))

        # organize the results and print them
        if return_code == -1:
            failed_list.append({'file': file, 'message': return_message})
            if return_message in failed_dict:
                failed_dict[return_message] += 1
            else:
                failed_dict[return_message] = 1
        if return_code == 0:
            success_list.append(file)

    print(f"Number of success cases: {len(success_list)}\nNumber of fail cases: {len(failed_list)}\nFailed dict: {failed_dict}")