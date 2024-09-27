import os


def get_data_from_file_name(filename: str):
    try:
        usuario_casilla, cleaned_filename = filename.split('_', 1)
    except Exception:
        raise SyntaxError(f'Fallo al obtener el nombre de usuario: Nombre de archivo no contiene el prefijo "_"')
    usuario_casilla = usuario_casilla.lower()
    cleaned_filename = cleaned_filename
    return {'usuario_casilla': usuario_casilla, 'cleaned_filename': cleaned_filename}
