from oracledb import Connection

from utils.functions.reject_and_save_error import reject_and_save_error


def validate_correct_flow(connector: Connection, data, correlativo, files, logger):
    t_doc = data['type_of_file']
    cursor = connector.cursor()
    cursor_FLG_MFT = connector.cursor()    
    cursor.callproc(
        "PROC_OBTENER_FLG_MFT",
        [
            t_doc,
            cursor_FLG_MFT
        ]
    )
    result = cursor_FLG_MFT.fetchone()[0]
    cursor_FLG_MFT.close()
    cursor.close()
    if result is None or result.lower() == 'n':
        reject_and_save_error(connector, correlativo, '086', f"Documento no está habilitado para MFT: {t_doc}", data, files, logger)
        raise ValueError(f"Documento no está habilitado para MFT: {t_doc}")
    