import os

def get_files_info(working_directory, directory = "."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        contents = os.listdir(full_path)
        collection = []

        for item in sorted(contents):
            path = os.path.join(full_path, item)
            string = f" - {item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}"
            collection.append(string)

        result = "\n".join(collection)
        return result
    except Exception as e:
        return f"Error: {e}"