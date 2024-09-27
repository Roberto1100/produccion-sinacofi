import re
from oracledb import Connection

def get_t_doc_from_header(file, connector: Connection):
    
    cursor_result_t_docs = connector.cursor()
    cursor_t_docs = connector.cursor()
    cursor_t_docs.callproc("PROC_OBTENER_LISTA_TDOCS", [cursor_result_t_docs])
    t_docs = [row[0] for row in cursor_result_t_docs.fetchall()]
    cursor_result_t_docs.close()
    cursor_t_docs.close()
    
    
    cursor_result_positions = connector.cursor()
    cursor_positions = connector.cursor()
    cursor_positions.callproc("PROC_OBTENER_POSICIONES", [cursor_result_positions])
    positions = cursor_result_positions.fetchall()
    cursor_result_positions.close()
    cursor_positions.close()

    with open(file, "r") as archivo:
        linea = archivo.readline()
        if linea.startswith('\n'):
            return None
        for id, opcion, start_pos, end_pos in positions:
            start_pos -= 1  
            t_doc_candidate = linea[start_pos:end_pos]
            
            if t_doc_candidate in t_docs:
                return t_doc_candidate

    return '000'