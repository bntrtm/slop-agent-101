import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        wd_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(wd_path, directory))
        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'
        valid_target_dir = os.path.commonpath([wd_path, target_dir]) == wd_path
        if not valid_target_dir:
            return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'
        lines = []
        for path in os.listdir(target_dir):
            full_path = os.path.join(target_dir, path)
            size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            lines.append(f"- {path}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
