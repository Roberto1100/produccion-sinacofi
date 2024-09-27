from oracledb import Connection

def insert_documento_entrada(connector: Connection, correlativo, file, tipo_archivo:str, nombre_archivo:str):
    cursor = connector.cursor()
    if nombre_archivo[0].isupper():
        tipo_archivo = tipo_archivo.upper()
    cursor.callfunc(
        "FUNC_INSERTAR_ARCHIVO_ENTRADA", 
        int,
        [
            correlativo, 
            file,
            tipo_archivo,
            nombre_archivo
        ]
    )    
    cursor.close()