from oracledb import Connection

from utils.functions.reject_and_save_error import reject_and_save_error
from utils.functions.set_movement import set_movement


def get_correlativo(connector: Connection, data, file_size, files, logger, cant_lineas):
    usuario_casilla = data['usuario_casilla']
    archivo_entrada = data['cleaned_filename']
    tipo_documento = data['type_of_file']
    cursor = connector.cursor()
    cursor.execute("SELECT CORRELATIVO_TRAZA.NEXTVAL FROM DUAL")
    correlativo_num = cursor.fetchone()[0]
    correlativo = str(correlativo_num).zfill(8)
    logger.info(f'Se consumió el correlativo "{correlativo}" para el documento "{archivo_entrada}"')
    flujo = 'MFT'
    cursor_result_cod_inst_y_casilla = connector.cursor()
    cursor.callproc(
        "PROC_OBTENER_COD_INST_Y_CASILLA",
        [
            usuario_casilla,
            cursor_result_cod_inst_y_casilla
        ]
    )
    select_result = cursor_result_cod_inst_y_casilla.fetchone()
    cursor_result_cod_inst_y_casilla.close()
    if select_result is None:
        cursor_result_cod_inst_y_casilla = connector.cursor()
        cursor.callproc(
            "PROC_OBTENER_COD_INST_Y_CASILLA",
            [
                'NE',
                cursor_result_cod_inst_y_casilla
            ]
        )
        select_result = cursor_result_cod_inst_y_casilla.fetchone()
        cursor_result_cod_inst_y_casilla.close()
    usuario_casilla = select_result[1]
    entidad_origen = select_result[0]
    cursor_result_t_doc = connector.cursor() 
    cursor.callproc(
        "PROC_OBTENER_T_DOC",
        [
            tipo_documento,
            cursor_result_t_doc
        ]
    )
    select_result = cursor_result_t_doc.fetchone()
    cursor_result_t_doc.close()  
    if select_result is None:
        cursor_result_t_doc = connector.cursor()
        cursor.callproc(
            "PROC_OBTENER_T_DOC",
            [
                '000',
                cursor_result_t_doc

            ]
        )
        select_result = cursor_result_t_doc.fetchone()
        cursor_result_t_doc.close()   
    tipo_documento = select_result[0]
    if usuario_casilla == 'NE':
        correlativo_inst = '00000000'
    else:
        cursor.execute(f"SELECT CORRELATIVO_ENTRADA_{entidad_origen}.NEXTVAL FROM DUAL")
        correlativo_inst_num = cursor.fetchone()[0]
        correlativo_inst = str(correlativo_inst_num).zfill(8)
    if tipo_documento == '000':
        version = 1
    else:
        cursor_result_version_max = connector.cursor()
        cursor.callproc(
            "PROC_OBTENER_VERSION_MAX_MSG",
            [
                tipo_documento,
                cursor_result_version_max
            ]
        )
        version = cursor_result_version_max.fetchone()[0]
        cursor_result_version_max.close()
    cursor.callfunc(
        "FUNC_INSERTAR_ENCABEZADO_TRAZA", 
        int,
        [
            correlativo, 
            flujo, 
            usuario_casilla, 
            entidad_origen, 
            archivo_entrada, 
            tipo_documento, 
            file_size, 
            correlativo_inst, 
            version,
            cant_lineas
        ]
    )    
    cursor.close()
    set_movement(connector, correlativo, '10')
    if usuario_casilla == "NE":
        reject_and_save_error(connector, correlativo, '007', f"Casilla no existe: {data['usuario_casilla']}", data, files, logger)
        raise ValueError(f"Casilla no existe: {data['usuario_casilla']}")
    if tipo_documento == "000":
        reject_and_save_error(connector, correlativo, '083', f"Documento no existe: {data['type_of_file']}", data, files, logger)
        raise ValueError(f"Documento no existe: {data['type_of_file']}")
    return correlativo