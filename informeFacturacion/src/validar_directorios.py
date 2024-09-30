import os

from config.db_config import ORA_CONFIG_DIRECTORY
from config.directories import REPORTS_DIRECTORY, LOGS_DIRECTORY, BACKUPS_DIRECTORY

def validate_directories():
    if(not REPORTS_DIRECTORY or not os.path.exists(REPORTS_DIRECTORY)):
        raise ValueError('REPORTS_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar directories.py')
    if(not LOGS_DIRECTORY or not os.path.exists(LOGS_DIRECTORY)):
        raise ValueError('LOGS_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar directories.py')
    if(not ORA_CONFIG_DIRECTORY or not os.path.exists(ORA_CONFIG_DIRECTORY)):
        raise ValueError('ORA_CONFIG_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar db_config.py')
    if(not BACKUPS_DIRECTORY or not os.path.exists(BACKUPS_DIRECTORY)):
        raise ValueError('BACKUPS_DIRECTORY no está definido, contiene errores o el directorio no existe, por favor revisar directories.py')
