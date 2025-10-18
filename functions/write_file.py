import os
from google.genai import types



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file with the specified content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)




def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    absolute_target_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)

    if not absolute_target_path.startswith(absolute_working_dir):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory' 
       # 2. Directory Creation: Ensure parent directories exist
    try:
        # Get the directory part of the target path
        target_dir = os.path.dirname(absolute_target_path)
        
        # Create directories recursively. exist_ok=True prevents an error if the directory exists.
        os.makedirs(target_dir, exist_ok=True)

    except Exception as e:
        return f"Error: {e}"

    # 3. File Writing (Next Step)
    try:
        with open(absolute_target_path, "w", encoding="utf-8") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"