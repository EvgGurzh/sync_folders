import os
import time
import shutil
import logging
import argparse
import filecmp
from datetime import datetime


def synchronizing_folders(source_path, destination_path, logs_path, interval):
    """
    One way synchronization from source to destination
        :param source_path: Source folder path
        :type source_path: string
        :param destination_path: Destination folder path, will be created if not exists
        :type destination_path: string
        :param logs_path: Path to folder to store logs, will be created if not exists
        :type logs_path: string
        :param interval: Synchronization interval in seconds
        :type interval: int
        :return: None
    """
    # stripping last separator if there is the case
    if source_path[-1] == os.sep:
        source_path = source_path[:-1]
    if destination_path[-1] == os.sep:
        destination_path = destination_path[:-1]
    if logs_path[-1] == os.sep:
        logs_path = logs_path[:-1]
    # configuring logging
    log_file = f"{logs_path}{os.sep}{datetime.now().strftime('%Y_%m_%d-%H_%M_%S_%f')}"
    if not os.path.exists(logs_path):
        print(f"Logs directory {logs_path} doesn't exist, creating..")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler(log_file), logging.StreamHandler()])
    # checking paths input
    if not os.path.exists(source_path):
        logging.error(f"Source directory {source_path} doesn't exist!")
        exit()
    if not os.path.exists(destination_path):
        logging.info(f"Destination directory {destination_path} doesn't exist, creating..")
        os.makedirs(os.path.dirname(destination_path + os.sep), exist_ok=True)
    # starting sync
    logging.info(f"Starting synchronization with interval of {interval} seconds")
    while True:
        start_time = time.time()
        for current_folder, current_sub_folders, current_files in os.walk(source_path):
            # handling folders
            destination_sub_folders = next(os.walk(current_folder.replace(source_path, destination_path)))[1]
            folders_to_remove = set(destination_sub_folders) - set(current_sub_folders)
            folders_to_create = set(current_sub_folders) - set(destination_sub_folders)
            for folder in folders_to_remove:
                destination_folder_path = f"{current_folder}{os.sep}{folder}".replace(source_path, destination_path)
                logging.info(f"Removing folder {destination_folder_path}")
                shutil.rmtree(destination_folder_path)
            for folder in folders_to_create:
                destination_folder_path = f"{current_folder}{os.sep}{folder}".replace(source_path, destination_path)
                logging.info(f"Creating folder {destination_folder_path}")
                os.mkdir(destination_folder_path)
            # handling files
            destination_files = next(os.walk(current_folder.replace(source_path, destination_path)))[2]
            files_to_remove = set(destination_files) - set(current_files)
            for file in files_to_remove:
                destination_file_path = f"{current_folder}{os.sep}{file}".replace(source_path, destination_path)
                logging.info(f"Removing file {destination_file_path}")
                os.remove(destination_file_path)
            for file in current_files:
                source_file_path = f"{current_folder}{os.sep}{file}"
                destination_file_path = source_file_path.replace(source_path, destination_path)
                if os.path.isfile(destination_file_path) and filecmp.cmp(source_file_path, destination_file_path):
                    continue
                logging.info(f"Copying file {source_file_path}")
                shutil.copy2(source_file_path, destination_file_path)
        # handling sleep according to the passed time
        if (time.time() - start_time) // interval >= 1:
            time.sleep(interval)
        else:
            time.sleep(interval - ((time.time() - start_time) % interval))


if __name__ == "__main__":
    # parsing arguments
    parser = argparse.ArgumentParser(description='Sync script')
    parser.add_argument('-s', dest="source", type=str)
    parser.add_argument('-d', dest="destination", type=str)
    parser.add_argument('-l', dest="logs", type=str)
    parser.add_argument('-i', dest="interval", type=int)
    args = parser.parse_args()
    # run synchronization
    synchronizing_folders(args.source, args.destination, args.logs, args.interval)
