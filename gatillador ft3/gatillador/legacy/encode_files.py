import base64
import os

def encode_files(files):
    encoded_files = {}
    for file in files:
        with open(file, 'rb') as binaryFile:
            file_name = os.path.basename(file)
            extension = file_name.split('.')[-1]
            content = binaryFile.read()
            encoded_file = base64.b64encode(content).decode('utf-8')
            encoded_files[extension] = encoded_file
    return encoded_files