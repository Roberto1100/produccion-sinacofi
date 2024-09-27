import os

from utils.constants import CAR_CTR_EXT, CAR_EXT, CTR_EXT, DAT_EXT

def get_files_content(files):
    encoded_files = {}
    for file in files:
        with open(file, 'rb') as binaryFile:
            file_name = os.path.basename(file)
            extension = file_name.split('.')[1:]
            if len(extension) == 0:
                encoded_files[DAT_EXT] = binaryFile.read().decode('utf-8')
            elif len(extension) == 2 and extension[0].lower() == CAR_EXT and extension[1].lower() == CTR_EXT:
                content = binaryFile.read().decode('utf-8')
                encoded_files[CAR_CTR_EXT] = content
            elif extension[0].lower() == CAR_EXT:
                content = binaryFile.read().decode('utf-8')
                encoded_files[CAR_EXT] = content
            elif extension[0].lower() == CTR_EXT:
                content = binaryFile.read().decode('utf-8')
                encoded_files[CTR_EXT] = content
            elif extension[0].lower() == DAT_EXT:
                content = binaryFile.read().decode('utf-8')
                encoded_files[DAT_EXT] = content
    return encoded_files