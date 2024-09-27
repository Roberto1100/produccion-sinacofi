def get_data_from_file_name(filename: str, count_files: int):
    try:
        usuario_casilla, cleaned_filename = filename.split('_', 1)
    except Exception:
        raise SyntaxError(f'Fallo al obtener el nombre de usuario: Nombre de archivo no contiene el prefijo "_"')
    if count_files == 3:
        type_of_file = cleaned_filename[2:5]
    else:
        type_of_file = cleaned_filename[:3]
    usuario_casilla = usuario_casilla.lower()
    cleaned_filename = cleaned_filename
    type_of_file = type_of_file.upper()
    return {'usuario_casilla': usuario_casilla, 'cleaned_filename': cleaned_filename, 'type_of_file': type_of_file}
