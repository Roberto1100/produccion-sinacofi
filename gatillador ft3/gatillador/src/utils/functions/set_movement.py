import datetime
from oracledb import Connection


def set_movement(connector: Connection, correlativo, estado):
    cursor = connector.cursor()
    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    cursor.callfunc("FUNC_CARGAMOVIMIENTO", str, [correlativo, None, None, None, estado, formatted_date])
    cursor.close()