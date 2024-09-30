from config.conector import DatabaseConnection
from generar_informes import generarInformes
from envio_correos import envioCorreos
from config.get_logger import get_logger
from validar_directorios import validate_directories




def main(connector, logger):
    fecha_periodo_mft, fecha_periodo_front = generarInformes(connector, logger)
    envioCorreos(fecha_periodo_mft, 'MFT', logger)
    envioCorreos(fecha_periodo_front, 'WEB', logger)
    
if __name__ == "__main__":
    try:
        validate_directories()
        logger = get_logger()
        try:
            connection = DatabaseConnection()
            connector = connection.get_connection()
            connector.autocommit = True
            main(connector, logger)
        except Exception as e:
            print(f'Error: {e}')
            logger.error(e)
    except Exception as e:
        print(f'Error: {e}')