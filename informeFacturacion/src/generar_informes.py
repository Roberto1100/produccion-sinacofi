import os
import json
from datetime import datetime
from oracledb import Connection


from config.directories import REPORTS_DIRECTORY, BACKUPS_DIRECTORY

def generarInformes(connector: Connection, logger):
    cursor = connector.cursor()
    cursor_data_MFT = connector.cursor()
    cursor.callproc("PROC_GENERA_FACTURACION_MFT", [cursor_data_MFT])
    data_MFT = cursor_data_MFT.fetchall()
    cursor_data_MFT.close()
    cursor_data_front = connector.cursor()
    cursor.callproc("PROC_GENERA_FACTURACION_FRONT", [cursor_data_front])
    data_front = cursor_data_front.fetchall()
    cursor_data_front.close()
    cursor.close()

    informeMFT = ''
    informeFront = ''

    for registroMFT in data_MFT:
        jsondataMFT = json.loads(registroMFT[0])
        informeMFT += f'{jsondataMFT['TIDdeDestino']};{jsondataMFT['TipodeArchivo']};{jsondataMFT['TIDdeOrigen']};{jsondataMFT['CasilladeOrigen']};{jsondataMFT['CasilladeDestino']};{jsondataMFT['FechadeTransferencia']};{jsondataMFT['HoradeTransferencia']};{jsondataMFT['FechadeRecepcion']};{jsondataMFT['ArchivodeEntrada']};{jsondataMFT['TamañodeArchivo']};{jsondataMFT['ArchivoEntrada']}\n'

    for registroFront in data_front:
        jsondatafront = json.loads(registroFront[0])
        informeFront += f'{jsondatafront['TIDdeDestino']};{jsondatafront['TipodeArchivo']};{jsondatafront['TIDdeOrigen']};{jsondatafront['CasilladeOrigen']};{jsondatafront['CasilladeDestino']};{jsondatafront['FechadeTransferencia']};{jsondatafront['HoradeTransferencia']};{jsondatafront['FechadeRecepcion']};{jsondatafront['ArchivodeEntrada']};{jsondatafront['TamañodeArchivo']};{jsondatafront['ArchivoEntrada']}\n'


    fecha_str_MFT = jsondataMFT['FechadeRecepcion']
    fecha_obj_MFT = datetime.strptime(fecha_str_MFT, '%Y-%m-%d %H:%M:%S')
    fecha_str_front = jsondatafront['FechadeRecepcion']
    fecha_obj_front = datetime.strptime(fecha_str_front, '%Y-%m-%d %H:%M:%S')

    mes_MFT = fecha_obj_MFT.strftime('%m') 
    año_MFT = fecha_obj_MFT.strftime('%Y')
    mes_front = fecha_obj_front.strftime('%m') 
    año_front = fecha_obj_front.strftime('%Y')    

    file_name_mft = f'MFT-{mes_MFT}{año_MFT}.txt'
    file_name_front = f'WEB-{mes_front}{año_front}.txt'

    fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')

    file_name_backup_mft = f'{file_name_mft}-{fecha_actual}'
    file_name_backup_front = f'{file_name_front}-{fecha_actual}'

    file_path_mft = os.path.join(REPORTS_DIRECTORY, file_name_mft)
    file_path_front = os.path.join(REPORTS_DIRECTORY, file_name_front)
    file_path_backup_mft = os.path.join(BACKUPS_DIRECTORY, file_name_backup_mft)
    file_path_backup_front = os.path.join(BACKUPS_DIRECTORY, file_name_backup_front)

    with open(file_path_mft, 'w', encoding='utf-8') as file:
        file.write(informeMFT)
        print(f"Informe MFT guardado en: {file_path_mft}")
        logger.info(f"Informe MFT guardado en: {file_path_mft}")

    with open(file_path_front, 'w', encoding='utf-8') as file:
        file.write(informeFront)
        print(f"Informe WEB guardado en: {file_path_front}")
        logger.info(f"Informe WEB guardado en: {file_path_front}")

    with open(file_path_backup_mft, 'w', encoding='utf-8') as file:
        file.write(informeMFT)
        print(f"Informe MFT respaldado en: {BACKUPS_DIRECTORY}")
        logger.info(f"Informe MFT respaldado en: {BACKUPS_DIRECTORY}")

    with open(file_path_backup_front, 'w', encoding='utf-8') as file:
        file.write(informeFront)
        print(f"Informe WEB respaldado en: {BACKUPS_DIRECTORY}")
        logger.info(f"Informe WEB respaldado en: {BACKUPS_DIRECTORY}")
    
    return fecha_obj_MFT, fecha_obj_front




