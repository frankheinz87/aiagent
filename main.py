import os
import sys
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)



def main():
    if len(sys.argv) < 2:
        print("no prompt provided")
        exit(1)
    messages = [types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    try:
        counter = 20
        while counter > 0:
            #print(f"DEBUG: Starting loop iteration, counter = {counter}")
            counter -= 1
            response = client.models.generate_content(
                model = "gemini-2.0-flash-001", 
                contents = messages,
                config = types.GenerateContentConfig(tools = [available_functions], system_instruction = system_prompt))
            
            for candidate in response.candidates:
                messages.append(candidate.content)

                

            if response.function_calls:
                #print(f"DEBUG: Function ccalls found")
                for call in response.function_calls:
                    #print(f"DEBUG: About to call call_function with {call.name}")
                    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
                    result = call_function(call, verbose = verbose)
                    messages.append(result)
                    #print("DEBUG: call_function returned!")
                    if not result.parts[0].function_response.response.get("result"):
                        raise Exception("Function call failed: no function_response found")
                    else:
                        if verbose:
                            print(f"User prompt: {sys.argv[1]}")
                            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                            print(f"-> {result.parts[0].function_response.response}")
                    #print("DEBUG: Finished processing all function calls, continuing loop")
            elif response.text:
                #print("DEBUG: Found text response, breaking")
                print(response.text)
                break
            #print(f"DEBUG: End of loop iteration, going to next iteration")
            
    except Exception as e:
        return f"Error: executing generate content: {e}"

if __name__ == "__main__":
    main()
