import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        task=subprocess.run(["uv", "run", file_path] + args, cwd=working_directory, capture_output=True, timeout=30)

        if task.stdout == "" and task.stderr == "":
            return "No output produced"
        result = f"STDOUT: {task.stdout.decode('utf-8')}\nSTDERR: {task.stderr.decode('utf-8')}"
        if task.returncode != 0:
            return result + f"\nProcess exited with code {task.returncode}"
        return result

        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file at the specified file path, constrained to the working directory with optional arguments if provided.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file, relative from the working directory. If not provided, inform user.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional arguments for the call of the python file.",
            ),
        },
    ),
)