import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        is_inside = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not is_inside:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File "{file_path}" not found.'
        
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed = subprocess.run(
            ["python", target_file, *args],
            capture_output=True,
            text=True,
            cwd=working_dir_abs,
            timeout=30
        )

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()

        output_parts = []

        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")
        
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")

        if completed.returncode != 0:
            output_parts.append(f"Process exited with code {completed.returncode}")

        if not output_parts:
            return "No output produced"
        
        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments.",
            ),
        },
        required=["file_path"],
    ),
)

        
    

