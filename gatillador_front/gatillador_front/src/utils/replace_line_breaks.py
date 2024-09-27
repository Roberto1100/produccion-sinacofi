from utils.reject_and_save_error import reject_and_save_error

def read_file_lines(archivo_entrada, connector, correlativo):
    try:
        with open(archivo_entrada, 'rb') as archivo_origen:
            contenido = archivo_origen.read().decode('utf-8')
            return contenido
    except Exception as e:
        reject_and_save_error(connector, correlativo, '092', f"{e}", archivo_entrada)
        raise ValueError(f"Error de codificación, {e}")