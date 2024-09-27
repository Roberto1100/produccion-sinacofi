from oracledb import Connection

from utils.get_t_doc_from_header import get_t_doc_from_header
from utils.reject_and_save_error import reject_and_save_error
from utils.set_movement import set_movement
from utils.validate_not_empty import validate_not_empty


def get_correlativo_and_t_doc(connector: Connection, data, file, logger, file_size, cant_lineas):
    usuario_casilla = data['usuario_casilla']
    archivo_entrada = data['cleaned_filename']
    EncodeError = False
    EmptyError = False
    cursor = connector.cursor()
    cursor.execute("SELECT CORRELATIVO_TRAZA.NEXTVAL FROM DUAL")
    correlativo_num = cursor.fetchone()[0]
    correlativo = str(correlativo_num).zfill(8)
    logger.info(f'{archivo_entrada}: Se consumio el correlativo "{correlativo}"')
    # TODO: Obtener flujo desde bbdd
    flujo = 'FL1'
    cursor_result_cod_inst_y_casilla = connector.cursor()
    cursor.callproc(
        "PROC_OBTENER_COD_INST_Y_CASILLA_F1",
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
            "PROC_OBTENER_COD_INST_Y_CASILLA_F1",
            [
                'NE',
                cursor_result_cod_inst_y_casilla
            ]
        )
        select_result = cursor_result_cod_inst_y_casilla.fetchone()
        cursor_result_cod_inst_y_casilla.close()
    else:
        logger.info(f"{archivo_entrada}: Entidad de origen {select_result[0]}")
    usuario_casilla = select_result[1]
    entidad_origen = select_result[0]
    
    try:
        t_doc_header = get_t_doc_from_header(file, connector)
    except Exception:
        EncodeError = True     
        t_doc_header = '000'
    
    cursor_result_t_doc = connector.cursor() 
    cursor.callproc(
        "PROC_OBTENER_T_DOC",
        [
            t_doc_header,
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
    t_doc = select_result[0]
    if usuario_casilla == 'NE':
        correlativo_inst = '00000000'
    else:
        cursor.execute(f"SELECT CORRELATIVO_ENTRADA_{entidad_origen}.NEXTVAL FROM DUAL")
        correlativo_inst_num = cursor.fetchone()[0]
        correlativo_inst = str(correlativo_inst_num).zfill(8)
    if t_doc == '000':
        version = 1
    else:
        cursor_result_version_max = connector.cursor()
        cursor.callproc(
            "PROC_OBTENER_VERSION_MAX_MSG",
            [
                t_doc,
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
            t_doc, 
            file_size, 
            correlativo_inst, 
            version,
            cant_lineas
        ]
    )    
    cursor.close()
    set_movement(connector, correlativo, '10')
    logger.info(f"{data['cleaned_filename']}: Validando que archivo no se encuentre vacío.")
    validate_not_empty(connector, file_size, correlativo, file)
    if t_doc_header is None:
        reject_and_save_error(connector, correlativo, '089', f"Archivo de datos", file)
        raise ValueError(f"Linea de header vacia")
    if usuario_casilla == "NE":
        reject_and_save_error(connector, correlativo, '007', f"Casilla no existe: {data['usuario_casilla']}", file)
        raise ValueError(f"Casilla no existe: {data['usuario_casilla']}")
    if t_doc == "000" and EncodeError == True:
        reject_and_save_error(connector, correlativo, '092', f"Error de codificación", file)
        raise ValueError(f"{archivo_entrada}: Error de codificación")
    elif t_doc == "000":
        reject_and_save_error(connector, correlativo, '083', f"Documento no existe: {t_doc_header}", file)
        raise ValueError(f"Documento no existe: {t_doc_header}")
    return (correlativo, t_doc)