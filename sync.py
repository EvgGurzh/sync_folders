import os
import time
import shutil
import logging
import argparse
import filecmp
from datetime import datetime


def synchronizing_folders(src_path, dest_path, logs_path, interval):
    """
    One way synchronization from source to destination
        :param src_path: Source folder path
        :type src_path: string
        :param dest_path: Destination folder path, will be created if not exists
        :type dest_path: string
        :param logs_path: Path to folder to store logs, will be created if not exists
        :type logs_path: string
        :param interval: Synchronisation interval in seconds, default is 30 seconds
        :type interval: int
        :return: None
    """
    # configuring logging
    log_file = f"{logs_path}{os.sep}{datetime.now().strftime('%Y_%m_%d-%H_%M_%S_%f')}"
    if not os.path.exists(logs_path):
        print(f"Logs directory {logs_path} doesn't exist, creating..")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler(log_file), logging.StreamHandler()])

    # checking paths input
    if not os.path.exists(src_path):
        logging.error(f"Source directory {src_path} doesn't exist!")
        exit()
    if not os.path.exists(dest_path):
        logging.info(f"Destination directory {dest_path} doesn't exist, creating..")
        os.makedirs(os.path.dirname(dest_path + os.sep), exist_ok=True)

    # starting sync
    logging.info(f"Starting synchronization with interval of {interval} seconds")
    while True:
        start_time = time.time()
        for current_folder, current_sub_folders, current_files in os.walk(src_path):
            # handling folders
            dest_sub_folders = next(os.walk(current_folder.replace(src_path, dest_path)))[1]
            folders_to_remove = set(dest_sub_folders) - set(current_sub_folders)
            folders_to_create = set(current_sub_folders) - set(dest_sub_folders)
            for folder in folders_to_remove:
                dest_folder = f"{current_folder}{os.sep}{folder}".replace(src_path, dest_path)
                logging.info(f"Removing folder {dest_folder}")
                shutil.rmtree(dest_folder)
            for folder in folders_to_create:
                dest_folder = f"{current_folder}{os.sep}{folder}".replace(src_path, dest_path)
                logging.info(f"Creating folder {dest_folder}")
                os.mkdir(dest_folder)
            # handling files
            dest_files = next(os.walk(current_folder.replace(src_path, dest_path)))[2]
            files_to_remove = set(dest_files) - set(current_files)
            for file in files_to_remove:
                dest_file = f"{current_folder}{os.sep}{file}".replace(src_path, dest_path)
                logging.info(f"Removing file {dest_file}")
                os.remove(dest_file)
            for file in current_files:
                src_file = f"{current_folder}{os.sep}{file}"
                dest_file = src_file.replace(src_path, dest_path)
                if os.path.isfile(dest_file) and filecmp.cmp(src_file, dest_file):
                    continue
                logging.info(f"Copying file {src_file}")
                shutil.copy2(src_file, dest_file)
        # handling sleep according to the passed time
        if (time.time() - start_time) // interval >= 1:
            time.sleep(interval)
        else:
            time.sleep(interval - ((time.time() - start_time) % interval))


if __name__ == "__main__":

    # parsing arguments
    parser = argparse.ArgumentParser(description='Sync script')
    parser.add_argument('-s', dest="src", type=str)
    parser.add_argument('-d', dest="dst", type=str)
    parser.add_argument('-i', dest="int", default=30, type=int)
    parser.add_argument('-l', dest="logs", type=str)
    args = parser.parse_args()

    # stripping last separator if there is the case
    if args.src[-1] == "\\" or "/" : args.src = args.src[:-1] 
    if args.dst[-1] == "\\" or "/" : args.dst = args.dst[:-1] 
    if args.logs[-1] == "\\" or "/" : args.logs = args.logs[:-1]

    synchronizing_folders(args.src, args.dst, args.logs, args.int)
