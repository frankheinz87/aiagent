import os

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.exists(full_path) and not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)        

        with open(full_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"