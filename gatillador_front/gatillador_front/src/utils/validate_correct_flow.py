from oracledb import Connection

from utils.reject_and_save_error import reject_and_save_error


def validate_correct_flow(connector: Connection, t_doc, correlativo, file):
    cursor = connector.cursor()
    cursor_FLG_FL1 = connector.cursor()    
    cursor.callproc(
        "PROC_OBTENER_FLG_FL1",
        [
            t_doc,
            cursor_FLG_FL1
        ]
    )
    result = cursor_FLG_FL1.fetchone()[0]
    cursor_FLG_FL1.close()
    cursor.close()
    if result is None or result.lower() == 'n':
        reject_and_save_error(connector, correlativo, '086', f"Documento no está habilitado para WEB: {t_doc}", file)
        raise ValueError(f"Documento no está habilitado para WEB: {t_doc}")
