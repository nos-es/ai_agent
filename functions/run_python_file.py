import os
import subprocess


def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

        if os.path.isfile(target_file) is not True:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path.endswith(".py") is not True:
            return f'Error: "{file_path}" is not a Python file'

        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_file]) == working_dir_abs

        if valid_target_dir is not True:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        command = ["python", target_file]

        if args is not None and len(args) != 0:
            command.extend(args)

        completed_proc = subprocess.run(
            args=command, text=True, timeout=30, cwd=working_dir_abs, capture_output=True)
        return_code = completed_proc.returncode

        output = ""
        if return_code != 0:
            output += f"Process exited with code {return_code}" + "\n"

        std_out = completed_proc.stdout
        std_err = completed_proc.stderr

        if std_out == "" and std_err == "":
            output += "No output produced" + "\n"

        output += f"STDOUT: {std_out}" + "\n" + f"STDERR: {std_err}"

        return output

    except Exception as exp:
        return f"Error: executing Python file: {exp}"
