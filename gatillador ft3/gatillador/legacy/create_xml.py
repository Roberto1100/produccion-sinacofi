import datetime
from logging import Logger
import os
import xml.etree.ElementTree as ET

from ..constants import XML_DATA_LENGTH_LIMIT


def get_data_divided(content):
    if len(content) <= XML_DATA_LENGTH_LIMIT:
        return [content]
    content_divided = []
    while(len(content) > XML_DATA_LENGTH_LIMIT):
        content_divided.append(content[:XML_DATA_LENGTH_LIMIT])
        content = content[XML_DATA_LENGTH_LIMIT:]
    content_divided.append(content)
    return content_divided


def create_xml(file_name, encoded_files: dict, xml_directory, logger: Logger, data):
    root = ET.Element('inbound')
    root.set('xmlns', '#')

    option_element = ET.SubElement(root, 'opcion')
    option_element.text = '4'

    canal_element = ET.SubElement(root, 'flujo')
    canal_element.text = 'F3'

    usuario_element = ET.SubElement(root, 'usuario')
    usuario_element.text = data['usuario_casilla']

    current_date = datetime.datetime.now().strftime('%Y%m%d')
    fecha_element = ET.SubElement(root, 'fecha')
    fecha_element.text = current_date

    na_element = ET.SubElement(root, 'NA')
    na_element.text = data['cleaned_filename']

    td_element = ET.SubElement(root, 'TD')
    td_element.text = data['type_of_file']

    filler_element = ET.SubElement(root, 'filler')
    filler_element.text = ''

    for extension, encoded_file in encoded_files.items():
        if(extension.lower() not in ['car', 'ctr']):
            data_content = encoded_file
        elif(extension.lower() == 'car'):
            car_content = encoded_file
        else:
            ctr_content = encoded_file
    data_contents = get_data_divided(data_content)
    if len(data_contents) == 1:
        data_element = ET.SubElement(root, 'Datos')
        data_element.text = data_contents[0]
        for i in range(1, 6):
            data_element = ET.SubElement(root, f'Datos{i}')
            data_element.text = ''
    else:
        data_element = ET.SubElement(root, 'Datos')
        data_element.text = ''
        for i, data_content in enumerate(data_contents, start=1):
            if i > 6:
                break
            data_element = ET.SubElement(root, f'Datos{i}')
            data_element.text = data_content
        for j in range(i+1, 7):
            data_element = ET.SubElement(root, f'Datos{j}')
            data_element.text = ''
    
    control_datos_element = ET.SubElement(root, 'ControlDatos')
    control_datos_element.text = ctr_content

    caratula_element = ET.SubElement(root, 'Caratula')
    caratula_element.text = car_content
    
    control_caratula_element = ET.SubElement(root, 'ControlCaratula')
    control_caratula_element.text = ''

    tree = ET.ElementTree(root)
    directory_and_filename = os.path.join(xml_directory, file_name + '.xml')
    tree.write(directory_and_filename, xml_declaration=True, encoding='utf-8', )
    # Se crea la lista de archivos procesados
    files_names = [file_name + '.' + extension if extension.lower() in ['car', 'ctr'] else file_name for extension in encoded_files.keys()]
    logger.info(f'Archivos procesados: {files_names}')