from oracledb import Connection

from utils.reject_and_save_error import reject_and_save_error


def validate_area(connector: Connection, t_doc, correlativo, casilla, file):
    cursor = connector.cursor()
    cursor_validar_area = connector.cursor()
    cursor.callproc("PROC_VALIDAR_AREA_DOC", [t_doc, casilla, cursor_validar_area])
    area = cursor_validar_area.fetchone()
    cursor_validar_area.close()
    cursor.close()
    if area is None:
        reject_and_save_error(connector, correlativo, '084', f"Familia de documento {t_doc} no contiene un area relacionada", file)
        raise ValueError(f"Familia de documento {t_doc} no contiene un area relacionada")
    return area[0]