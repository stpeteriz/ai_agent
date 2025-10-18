import os
from config import MAX_FILE_SIZE   
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)   


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    absolute_target_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)

    if not absolute_target_path.startswith(absolute_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory' 
    if not os.path.isfile(absolute_target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        # Open the file for reading
        with open(absolute_target_path, "r", encoding="utf-8") as f:
            # Read exactly up to the maximum character limit
            file_content_string = f.read(MAX_FILE_SIZE)
            
            # Check for truncation: 
            # If the length of the content read is the max size, 
            # try reading just one more character. If it's not empty, the file was truncated.
            is_truncated = False
            if len(file_content_string) == MAX_FILE_SIZE:
                # Attempt to read the next character
                if f.read(1): 
                    is_truncated = True

            # If truncated, append the required message
            if is_truncated:
                truncation_message = (
                    f'[...File "{file_path}" truncated at {MAX_FILE_SIZE} characters]'
                )
                file_content_string += '\n' + truncation_message

            return file_content_string


    except Exception as e:
        return (f"Error: {e}")