import sys

from config.conector import DatabaseConnection
from config.directories import FILES_DIRECTORY
from config.get_logger import get_logger
from utils.replace_line_breaks import read_file_lines
from utils.find_file_and_size_by_name import find_file_and_size_by_name
from utils.get_correlativo_and_t_doc import get_correlativo_and_t_doc
from utils.get_data_from_file_name import get_data_from_file_name
from utils.rename_and_move_processed_files import rename_and_move_processed_files
from utils.set_movement import set_movement
from utils.validate_correct_flow import validate_correct_flow
from utils.validate_directories import validate_directories
from utils.validate_not_deleted import validate_not_deleted
from utils.validate_area import validate_area
from utils.validar_gestion_usuarios import validate_gestion_usuarios

def main(file_name, logger, connector):
    file, size, cant_lineas = find_file_and_size_by_name(FILES_DIRECTORY, file_name)
    data = get_data_from_file_name(file_name)    
    correlativo, t_doc = get_correlativo_and_t_doc(connector, data, file, logger, size, cant_lineas)
    
    logger.info(f"{data['cleaned_filename']}: Tipo de documento {t_doc}")
    logger.info(f"{data['cleaned_filename']}: Validando que documento no está eliminado de la base de datos.")
    validate_not_deleted(connector, t_doc, correlativo, file)
    logger.info(f"{data['cleaned_filename']}: Validando flujo correcto.")
    validate_correct_flow(connector, t_doc, correlativo, file)
    
    logger.info(f"{data['cleaned_filename']}: Validando que exista área relacionada al documento.")
    area_id = validate_area(connector, t_doc, correlativo, data['usuario_casilla'], file)
    logger.info(f"{data['cleaned_filename']}: Validando que área contenga usuarios.")
    validate_gestion_usuarios(connector, area_id, correlativo, file, data['usuario_casilla'])
    file_content = read_file_lines(file, connector, correlativo)
    logger.info(f"{data['cleaned_filename']}: Renombrando archivo.")
    rename_and_move_processed_files(file, correlativo, False, t_doc, file_content)
    logger.info(f"{data['cleaned_filename']}: Archivo procesado correctamente.")
    set_movement(connector, correlativo, '20')

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("""Mal uso de script.
            Uso: python trigger_front.py <nombre_archivo>""")
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
            logger.error(f"F1 {e}")
    except Exception as e:
        print(f'Error: {e}')