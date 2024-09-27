import os

from config.db_config import ORA_CONFIG_DIRECTORY
from config.directories import FILES_DIRECTORY, LOGS_DIRECTORY, VALIDATED_FILES_DIRECTORY

def validate_directories():
    if(not FILES_DIRECTORY or not os.path.exists(FILES_DIRECTORY)):
        raise ValueError('FILES_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar directories.py')
    if(not LOGS_DIRECTORY or not os.path.exists(LOGS_DIRECTORY)):
        raise ValueError('LOGS_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar directories.py')
    if(not ORA_CONFIG_DIRECTORY or not os.path.exists(ORA_CONFIG_DIRECTORY)):
        raise ValueError('ORA_CONFIG_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar db_config.py')
    if(not VALIDATED_FILES_DIRECTORY or not os.path.exists(VALIDATED_FILES_DIRECTORY)):
        raise ValueError('VALIDATED_FILES_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar directories.py')
