import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        wd_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(wd_path, file_path))
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        valid_target_file = os.path.commonpath([wd_path, target_file]) == wd_path
        if not valid_target_file:
            return f'Error: could not read "{file_path}" as it is outside the permitted working directory'
        f = open(target_file)
        content = f.read(MAX_CHARS)
        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"Error: {e}"
