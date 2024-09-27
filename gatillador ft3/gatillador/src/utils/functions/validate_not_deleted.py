from oracledb import Connection

from utils.functions.reject_and_save_error import reject_and_save_error


def validate_not_deleted(connector: Connection, data, correlativo, files, logger):
    t_doc = data['type_of_file']
    cursor = connector.cursor()
    cursor_not_deleted = connector.cursor()    
    cursor.callproc(
        "PROC_OBTENER_FECHA_ELIMINADO",
        [
            t_doc,
            cursor_not_deleted 
        ]
    )
    result = cursor_not_deleted.fetchone()[0]
    cursor_not_deleted.close()
    cursor.close()
    if result is not None:
        reject_and_save_error(connector, correlativo, '087', f"Tipo de documento está eliminado: {t_doc}", data, files, logger)
        raise ValueError(f"Tipo de documento está eliminado: {t_doc}")
    