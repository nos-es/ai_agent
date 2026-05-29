import os
from google.genai import types
MAX_CHARS = 1000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file from which the content will be read, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


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
                file_content += f'[...File "{
                    file_path}" truncated at {MAX_CHARS} characters]'

        return file_content

    except Exception as exp:
        return f"Error: {exp}"
