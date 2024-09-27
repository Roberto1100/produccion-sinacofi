from datetime import datetime
from oracledb import Connection

from utils.rename_and_move_processed_files import rename_and_move_processed_files
from utils.set_movement import set_movement



def reject_and_save_error(connector: Connection, correlativo, codigo_error, detalle_error, file):
    cursor = connector.cursor()
    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d %H:%M:%S')
    cursor.callfunc("FUNC_CARGAERROR", str, [correlativo, codigo_error, detalle_error, formated_date])
    cursor.close()
    set_movement(connector, correlativo, '00')
    rename_and_move_processed_files(file, correlativo, error=True)
