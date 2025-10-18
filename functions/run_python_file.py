import os
import subprocess 
from google.genai import types



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory, optionally passing arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    absolute_target_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)

    if not absolute_target_path.startswith(absolute_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_target_path):
        return f'Error: File "{file_path}" not found.'
    
    if not absolute_target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'


    try:
        command = ['python', absolute_target_path] + args
        completed_process = subprocess.run(command, capture_output=True, text=True, cwd=absolute_working_dir, timeout=30)

        output_parts = []
          # 1. Add STDOUT and STDERR if present
        if completed_process.stdout:
            # Add the STDOUT prefix and the content
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")
        
        if completed_process.stderr:
            # Add the STDERR prefix and the content
            output_parts.append(f"STDERR:\n{completed_process.stderr}")
            
        # 2. Check for non-zero exit code
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}.")
        
        # 3. Check for no output produced
        if completed_process.returncode == 0 and not completed_process.stdout and not completed_process.stderr:
            output_parts.append("No output produced.")

        # 4. Join parts together
        return "\n".join(output_parts)
    
    
    except subprocess.TimeoutExpired as e:
        # Handle timeout separately as it's a specific subprocess error
        return f"Error: Execution timed out after 30 seconds."
    
    except Exception as e:
        return f"Error: executing Python file: {e}"