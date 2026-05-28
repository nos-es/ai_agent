import os
MAX_CHARS = 1000


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

        if os.path.isfile(target_file) is not True:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_file]) == working_dir_abs

        if valid_target_dir is not True:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        with open(target_file, "r") as f:
            file_content: str = f.read(MAX_CHARS)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content

    except Exception as exp:
        return f"Error: {exp}"
