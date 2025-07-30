import os



def get_files_info(working_directory, directory="."):
    if os.path.abspath(target_path).startswith(os.path.abspath(working_directory)):
        pass
        # do something if it's alright?
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    