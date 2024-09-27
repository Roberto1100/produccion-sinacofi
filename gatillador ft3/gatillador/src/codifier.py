import sys
from utils.conector import DatabaseConnection

from utils.functions.find_files_by_name import find_files_by_name
from utils.functions.create_xml import create_xml
from utils.functions.get_files_content import get_files_content
from utils.functions.get_data_from_file_name import get_data_from_file_name
from utils.functions.get_logger import get_logger
from utils.functions.delete_processed_files import delete_processed_files
from utils.functions.validate_correct_flow import validate_correct_flow
from utils.functions.validate_movement import validate_movement
from utils.functions.validate_directories import validate_directories
from utils.functions.validate_extensions_and_get_size import validate_extensions_and_get_size
from utils.functions.get_correlativo import get_correlativo
from utils.functions.set_movement import set_movement
from utils.functions.validate_not_deleted import validate_not_deleted
from utils.functions.validate_not_empty import validate_not_empty
from utils.constants import DAT_EXT, FILES_DIRECTORY, XML_FILES_DIRECTORY
from utils.functions.insert_documento_entrada import insert_documento_entrada
from utils.functions.reject_and_save_error import reject_and_save_error



def main(file_name, logger, connector):
    files = find_files_by_name(FILES_DIRECTORY, file_name)
    sizes, cant_lineas = validate_extensions_and_get_size(files, file_name)
    count_files = len(files)
    data = get_data_from_file_name(file_name, count_files)

    correlativo = get_correlativo(connector, data, sizes[DAT_EXT], files, logger, cant_lineas)
    logger.info(f'{data['cleaned_filename']}: Tipo de documento {data['type_of_file']}')
    logger.info(f'{data['cleaned_filename']}: Validando que documento no esta eliminado de la base de datos.')
    validate_not_deleted(connector, data, correlativo, files, logger)
    logger.info(f'{data['cleaned_filename']}: Validando que el flujo del documento sea correcto.')
    validate_correct_flow(connector, data, correlativo, files, logger)
    logger.info(f'{data['cleaned_filename']}: Validando que el archivo no este vacio.')
    validate_not_empty(connector, sizes, correlativo, data, files, logger)
    logger.info(f'{data['cleaned_filename']}: Validando que no haya sido procesado anteriormente.')
    validate_movement(connector, data, correlativo, files, logger)

    try:
        files_content = get_files_content(files)
    except Exception as e:
        reject_and_save_error(connector, correlativo, '092', f"Error de codificacion", data, files, logger)
        raise ValueError(f'{file_name}: Error de codificacion')

    
    insert_documento_entrada(connector, correlativo, files_content["car"],'car',data['cleaned_filename'])
    insert_documento_entrada(connector, correlativo, files_content["ctr"],'ctr',data['cleaned_filename'])
    logger.info(f'{data['cleaned_filename']}: Creando archivo XML...')
    create_xml(file_name, files_content, XML_FILES_DIRECTORY, data, correlativo)
    logger.info(f'{data['cleaned_filename']}: Eliminando archivos procesados.')
    delete_processed_files(files, logger)
    set_movement(connector, correlativo, '20')

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("""Mal uso de script.
            Uso: python codifier.py <nombre_archivo>""")
        validate_directories()
        file_name = sys.argv[1]
        logger = get_logger()
        try:
            connection = DatabaseConnection()
            connector = connection.get_connection()
            connector.autocommit = True
            main(file_name, logger, connector)
        except Exception as e:
            print(f'Error: {e}')
            logger.error(e)
    except Exception as e:
        print(f'Error: {e}')