import os

from utils.constants import CAR_CTR_EXT, CAR_EXT, CTR_EXT, DAT_EXT

def validate_extensions_and_get_size(files, file_name):
    sizes = {
        CAR_EXT: None,
        CTR_EXT: None,
        DAT_EXT: None,
        CAR_CTR_EXT: None,
    }
    if not files:
        raise FileNotFoundError(f'No se encontraron archivos con el nombre: "{file_name}"')
    for file in files:
        base_name = os.path.basename(file)
        extension = base_name.split('.')[1:]
        if len(extension) == 0:
            sizes[DAT_EXT] = os.path.getsize(file)
            with open(file, 'rb') as content:
                cantidad_lineas = len(content.readlines())
        elif len(extension) == 2 and extension[0].lower() == CAR_EXT and extension[1].lower() == CTR_EXT:
            sizes[CAR_CTR_EXT] = os.path.getsize(file)
        elif extension[0].lower() == CAR_EXT:
            sizes[CAR_EXT] = os.path.getsize(file)
        elif extension[0].lower() == CTR_EXT:
            sizes[CTR_EXT] = os.path.getsize(file)
        elif extension[0].lower() == DAT_EXT:
            sizes[DAT_EXT] = os.path.getsize(file)
            with open(file, 'rb') as content:
                cantidad_lineas = len(content.readlines())
    if sizes[DAT_EXT] is None:
        raise FileNotFoundError(f'No se encontro el archivo de datos: "{file_name}"')
    if sizes[CAR_EXT] is None:
        raise FileNotFoundError(f'No se encontro el archivo de caratula .CAR: "{file_name}"')
    if sizes[CTR_EXT] is None:
        raise FileNotFoundError(f'No se encontro el archivo de control .CTR: "{file_name}"')
    if len(files) == 4 and sizes[CAR_CTR_EXT] is None:
        raise FileNotFoundError(f'No se encontro el archivo de control de caratula .CAR.CTR: "{file_name}"')
    return sizes, cantidad_lineas