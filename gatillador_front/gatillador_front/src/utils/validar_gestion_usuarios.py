from oracledb import Connection

from utils.reject_and_save_error import reject_and_save_error


def validate_gestion_usuarios(connector: Connection, area_id, correlativo, file, casilla):
    cursor = connector.cursor()
    cursor_validar_gestion = connector.cursor()
    cursor.callproc("PROC_VALIDAR_GESTION_USUARIOS", [area_id, casilla, cursor_validar_gestion])
    conteo_usuarios = cursor_validar_gestion.fetchone()[0]
    cursor_validar_gestion.close()
    cursor.close()
    if conteo_usuarios == 0:
        reject_and_save_error(connector, correlativo, '090', f"Area {area_id} no contiene usuarios", file)
        raise ValueError(f"Area {area_id} no contiene usuarios")
    return conteo_usuarios