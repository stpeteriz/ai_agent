import os
from google.genai import types



def get_files_info(working_directory, directory="."):
    results = []
    # 1. Join paths
    full_path = os.path.join(working_directory, directory)
    
    # 2. Convert to absolute paths for reliable checking and use
    absolute_target_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)

    if not absolute_target_path.startswith(absolute_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(absolute_target_path):
        return f'Error: "{directory}" is not a directory'
    contents = os.listdir(absolute_target_path)
    for item in contents:
        full_item_path = os.path.join(absolute_target_path, item)
        get_size = 0
        try:
            directory_status = os.path.isdir(full_item_path)
            get_size = os.path.getsize(full_item_path)
            results.append(f"- {item}: file_size={get_size} bytes, is_dir={directory_status}")
        except Exception as e:
            results.append(f"Error: {e}")
            continue
    return '\n'.join(results)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)   
    
        
        
       
    