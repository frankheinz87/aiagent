import os
from google.genai import types

def get_files_info(working_directory, directory = "."):
    #print(f"DEBUG: get_files_info called with working_directory='{working_directory}', directory='{directory}'")
    try:
        full_path = os.path.join(working_directory, directory)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        #print("DEBUG: About to check if path starts with working directory")
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        #print("DEBUG: About to check if directory exists")
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        #print("DEBUG: About to list directory contents")
        contents = os.listdir(full_path)
        collection = []
        #print(f"DEBUG: contents = {contents}")

        for item in sorted(contents):
            path = os.path.join(full_path, item)
            string = f" - {item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}"
            collection.append(string)
        #print("DEBUG: About to join results")
        result = "\n".join(collection)
        #print(f"DEBUG: Final result: {result}")
        #print("DEBUG: About to return result")
        return result
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

