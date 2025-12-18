import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # 1. absolute path to working directory
        working_dir_abs = os.path.abspath(working_directory)

        # 2. absolute normalized path to target dir
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # 3. check target_dir is inside working_dir only
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # 4. check it IS a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # 5. build directory listing
        lines = []
        for item in os.listdir(target_dir):
            full_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path)
            lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {str(e)}"

# -------- Function Declaration (Schema) --------

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory to list files from, relative to the working directory. Optional.",
            ),
        },
    ),
)