import os

from config.directories import VALIDATED_FILES_DIRECTORY

def rename_and_move_processed_files(
        file, 
        correlativo,
        error:bool, 
        t_doc=None, 
        file_content = None,
    ):
    # date_when_processed = datetime.datetime.now()
    # formatted_date = date_when_processed.strftime("%Y%m%d%H%M%S")
    file_name = os.path.basename(file)
    # processed_file_name = f'{file_name}.processed_{formatted_date}'
    # target = os.path.join(processed_files_directory, processed_file_name)
    os.remove(file)
    if not error:
        validated_file_name = f'{t_doc}_{correlativo}_{file_name}'
        final_file_name = os.path.join(VALIDATED_FILES_DIRECTORY, validated_file_name)
        
        with open(final_file_name, 'w') as final_file:
            final_file.write(file_content)
        