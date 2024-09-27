from oracledb import Connection

from utils.constants import CAR_EXT, CTR_EXT, DAT_EXT
from utils.functions.reject_and_save_error import reject_and_save_error


def validate_not_empty(connector: Connection, sizes, correlativo, data, files, logger):
    if sizes[CAR_EXT] == 0:
        reject_and_save_error(connector, correlativo, '044', 'Carátula', data, files, logger)
        raise ValueError(f'El archivo .CAR no puede estar vacio')
    if sizes[CTR_EXT] == 0:
       reject_and_save_error(connector, correlativo, '040', 'Control de datos', data, files, logger)
       raise ValueError(f'El archivo .CTR no puede estar vacio')
    if sizes[DAT_EXT] == 0:
        reject_and_save_error(connector, correlativo, '040', 'Archivo de datos', data, files, logger)
        raise ValueError(f'El archivo de datos no puede estar vacio')