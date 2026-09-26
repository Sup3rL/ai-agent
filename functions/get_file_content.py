import config
import os


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # else:
        #     print(f'Success: "{file_path}" is within the working directory')

        with open(target_file_path, 'r') as file:
            content = file.read(config.MAX_CHARS)

            if file.read(1):
                content += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieves the content of a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file, relative to the working directory",
                },
            },
        },
    },
}