import os
from config import MAX_FILE_SIZE
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        is_inside = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not is_inside:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r", encoding="utf-8") as f:
            data = f.read()

        if len(data) > MAX_FILE_SIZE:
            truncated = data[:MAX_FILE_SIZE]
            truncated += f'\n[...File "{file_path}" truncated at {MAX_FILE_SIZE} characters]'
            return truncated

        return data

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)