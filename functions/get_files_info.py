import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:

        working_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.isdir(target_dir) is not True:
            return f'Error: "{directory}" is not a directory'

        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is not True:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        items = os.listdir(target_dir)

        for item in items:
            item_path = os.path.join(target_dir, item)
            print(f"{item}: file_size={os.path.getsize(
                item_path)}, is_dir={os.path.isdir(item_path)}")

        return f'Success: "{directory}" is within the working directory'
    except Exception as ex:
        return f"Error: {ex}"
