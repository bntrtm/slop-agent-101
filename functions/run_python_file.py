import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        wd_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(wd_path, file_path))
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        valid_target_file = os.path.commonpath([wd_path, target_file]) == wd_path
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", os.path.abspath(target_file)]
        if args:
            command.extend(args)
        completedProcess = subprocess.run(
            command, cwd=wd_path, capture_output=True, text=True, timeout=30
        )

        lines = []
        if completedProcess.returncode != 0:
            lines.append(f"Process exited with code {completedProcess.returncode}")
        if completedProcess.stdout == "" and completedProcess.stderr == "":
            lines.append("No output produced")
        else:
            if completedProcess.stdout != "":
                lines.append(f"STDOUT: {completedProcess.stdout}")
            if completedProcess.stderr != "":
                lines.append(f"STDERR: {completedProcess.stderr}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"
