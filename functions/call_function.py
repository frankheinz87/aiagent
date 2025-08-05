import os
import subprocess
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file
from google.genai import types

def call_function(function_call_part, verbose = False):
    #print("DEBUG: call_function was called!")
    #print(f"DEBUG: function name = {function_call_part.name}")
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    #function map
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    #check if function call invalid
    if function_call_part.name not in function_map:
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                        )
                    ],
                )
    else:
        #get function from map
        actual_function = function_map[function_call_part.name]

        #add working directory to args
        args_with_directory = function_call_part.args.copy()
        args_with_directory["working_directory"] = "./calculator"

        #call function
        result = actual_function(**args_with_directory)
        return types.Content(
                role="tool",
                parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                        )
                    ],
                )
