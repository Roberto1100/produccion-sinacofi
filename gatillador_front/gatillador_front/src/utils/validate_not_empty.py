from oracledb import Connection

from utils.reject_and_save_error import reject_and_save_error


def validate_not_empty(connector: Connection, size, correlativo, file):
    if size == 0:
        reject_and_save_error(connector, correlativo, '040', 'Archivo de datos', file)
        raise ValueError(f'El archivo de datos no puede estar vacio')