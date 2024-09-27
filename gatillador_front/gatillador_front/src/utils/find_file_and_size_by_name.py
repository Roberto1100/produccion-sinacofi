import os

def find_file_and_size_by_name(files_directory, file_name: str):
    with os.scandir(files_directory) as current_directory:
        for entry in current_directory:
            if entry.is_file() and file_name == entry.name:
                with open(entry, 'rb') as content:
                    cantidad_lineas = len(content.readlines())
                return(entry.path, os.path.getsize(entry.path), cantidad_lineas)
    raise ValueError(f"Archivo {file_name} no encontrado.")