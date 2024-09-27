import datetime
import logging
import os

from config.directories import LOGS_DIRECTORY


def get_logger():
    logs_directory = LOGS_DIRECTORY
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)
    
    current_date = datetime.datetime.now().strftime('%Y%m%d')
    log_file_path = f'{current_date}.log'
    log_file_path = os.path.join(logs_directory, log_file_path) 
    if not os.path.isfile(log_file_path):
        open(log_file_path, 'a').close()
    
    logger = logging.getLogger(log_file_path)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger