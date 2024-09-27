import datetime
import os
import xml.etree.ElementTree as ET

from ..constants import CAR_CTR_EXT, CAR_EXT, DAT_EXT, XML_DATA_LINES_LIMIT


def get_data_divided(content):
    if content[-1] == '\n':
        content = content[:-1]
    lines = content.split('\n')  
    total_lines = len(lines)
    
    if total_lines <= XML_DATA_LINES_LIMIT:
        return [content + '\n']

    lines_per_part = total_lines // 6
    part1 = '\n'.join(lines[:lines_per_part])
    part2 = '\n'.join(lines[lines_per_part:lines_per_part*2])
    part3 = '\n'.join(lines[lines_per_part*2:lines_per_part*3])
    part4 = '\n'.join(lines[lines_per_part*3:lines_per_part*4])
    part5 = '\n'.join(lines[lines_per_part*4:lines_per_part*5])
    part6 = '\n'.join(lines[lines_per_part*5:]) + '\n'
    content_divided = [
        part1,
        part2,
        part3,
        part4,
        part5,
        part6
    ]
    return content_divided


def create_xml(file_name, file_contents: dict, xml_directory, data, correlativo):
    root = ET.Element('inbound')
    root.set('xmlns', '#')

    option_element = ET.SubElement(root, 'opcion')
    option_element.text = '4'

    canal_element = ET.SubElement(root, 'flujo')
    canal_element.text = 'MFT'

    usuario_element = ET.SubElement(root, 'usuario')
    usuario_element.text = data['usuario_casilla']

    na_element = ET.SubElement(root, 'NA')
    na_element.text = data['cleaned_filename']

    td_element = ET.SubElement(root, 'TD')
    td_element.text = data['type_of_file']

    filler_element = ET.SubElement(root, 'filler')
    filler_element.text = ''

    car_ctr_content = ''
    for extension, file_content in file_contents.items():
        if extension.lower() == DAT_EXT:
            datos_content = file_content
        elif(extension.lower() == CAR_EXT):
            car_content = file_content
        elif(extension.lower() == CAR_CTR_EXT):
            car_ctr_content = file_content
        else:
            ctr_content = file_content
    data_contents = get_data_divided(datos_content)
    if len(data_contents) == 1:
        data_element = ET.SubElement(root, 'Datos')
        data_element.text = data_contents[0]
        for i in range(1, 7):
            data_element = ET.SubElement(root, f'Datos{i}')
            data_element.text = ''
    else:
        data_element = ET.SubElement(root, 'Datos')
        data_element.text = ''
        for i, datos_content in enumerate(data_contents, start=1):
            data_element = ET.SubElement(root, f'Datos{i}')
            data_element.text = datos_content
    
    control_datos_element = ET.SubElement(root, 'ControlDatos')
    control_datos_element.text = ctr_content

    caratula_element = ET.SubElement(root, 'Caratula')
    caratula_element.text = car_content
    
    control_caratula_element = ET.SubElement(root, 'ControlCaratula')
    control_caratula_element.text = car_ctr_content

    tree = ET.ElementTree(root)
    directory_and_filename = os.path.join(xml_directory, f'{data['type_of_file']}_{correlativo}_{file_name}.xml')
    tree.write(directory_and_filename, xml_declaration=True, encoding='utf-8', )
    