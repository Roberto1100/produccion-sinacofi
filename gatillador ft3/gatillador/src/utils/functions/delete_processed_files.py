from logging import Logger
import os

def delete_processed_files(files, logger: Logger):
    for file in files:
        file_name = os.path.basename(file)
        # Se crea la lista de archivos procesados
        logger.info(f'Archivos procesados: {file_name}')
        os.remove(file)