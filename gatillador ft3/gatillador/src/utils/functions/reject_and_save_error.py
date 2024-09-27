from datetime import datetime
import os

from utils.constants import RES_DIRECTORY
from utils.functions.delete_processed_files import delete_processed_files
from utils.functions.set_movement import set_movement


def reject_and_save_error(connector, correlativo, codigo_error, detalle_error, data, files, logger):
    cursor = connector.cursor()
    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d %H:%M:%S')
    cursor.callfunc("FUNC_CARGAERROR", str, [correlativo, codigo_error, detalle_error, formated_date])
    cursor.close()
    user = data['usuario_casilla']
    set_movement(connector, correlativo, '00')
    filename = data['cleaned_filename']
    filepath = os.path.join(RES_DIRECTORY, f'{user}_{filename}.RES')
    res_content = f'''MENSAJE_RESULTADO
{filename.ljust(20, ' ')}NK
Detalles con los errores ver en sitio web
FIN_MENSAJE
'''
    with open(filepath, 'w') as f:
        f.write(res_content)
    delete_processed_files(files, logger)
