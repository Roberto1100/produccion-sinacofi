import os

from utils.constants import FILES_DIRECTORY, LOGS_DIRECTORY, RES_DIRECTORY, XML_FILES_DIRECTORY

def validate_directories():
    if(not XML_FILES_DIRECTORY or not os.path.exists(XML_FILES_DIRECTORY)):
        raise ValueError('XML_FILES_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar constants.py')
    if(not FILES_DIRECTORY or not os.path.exists(FILES_DIRECTORY)):
        raise ValueError('FILES_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar constants.py')
    if(not LOGS_DIRECTORY or not os.path.exists(LOGS_DIRECTORY)):
        raise ValueError('LOGS_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar constants.py')
    if(not RES_DIRECTORY or not os.path.exists(RES_DIRECTORY)):
        raise ValueError('RES_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar constants.py')