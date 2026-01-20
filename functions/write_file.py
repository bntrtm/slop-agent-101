import os


def write_file(working_directory, file_path, content):
    try:
        wd_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(wd_path, file_path))
        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        valid_target_file = os.path.commonpath([wd_path, target_file]) == wd_path
        if not valid_target_file:
            return f'Error: could not write to "{target_file}" as it is outside the permitted working directory'
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"
