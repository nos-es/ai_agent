import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        if os.path.isdir(directory) is not True:
            return f'Error: "{directory}" is not a directory'

        print(f"working_directory: {working_directory}")
        working_dir_abs = os.path.abspath(working_directory)
        print(f"working_dir_abs: {working_dir_abs}")

        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is not True:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return f'Success: "{directory}" is within the working directory'
    except Exception as ex:
        return f"Error: {ex}"
