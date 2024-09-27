from oracledb import Connection

from utils.functions.reject_and_save_error import reject_and_save_error

def validate_movement(connector: Connection, data, correlativo, files, logger):
    cursor = connector.cursor()
    cursor_result = connector.cursor()
    filename = data['cleaned_filename']    
    cursor.callproc(
        "PROC_VALIDAR_MOVIMIENTO", 
        [
            filename,
            correlativo,
            cursor_result
        ]
    )
    cursor.close()
    already_sent = cursor_result.fetchone()
    cursor_result.close()
    if already_sent is not None:
        reject_and_save_error(connector, correlativo, '039', f'Archivo ya procesado: {filename}', data, files, logger)
        raise FileExistsError(f"Ya existe un envio con el mismo nombre de archivo: {filename}" )