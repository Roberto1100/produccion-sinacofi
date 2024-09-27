import os

def find_files_by_name(files_directory, file_name: str):
    files = []
    with os.scandir(files_directory) as current_directory:
        for entry in current_directory:
            if entry.is_file():
                base_name, extension = os.path.splitext(entry.name)
                if ((base_name == file_name and
                    (extension.lower() in ['.ctr', '.car', '.dat'] or not extension))
                    or 
                    (base_name.lower() == file_name.lower()+'.car' and
                    extension.lower() == '.ctr')
                    ):
                    files.append(entry.path)
    return (files)