import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file,
    ]
)


def main():
    # Load environment variables first
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Create the client
    client = genai.Client(api_key=api_key)
    
    # Check for command line arguments
    if len(sys.argv) < 2:
        print("Please provide a prompt as a command line argument")
        sys.exit(1)
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

    # Get the user prompt from command line arguments
    user_prompt = sys.argv[1]
    if verbose:
        print(f"User prompt: {user_prompt}")
    # Create the messages list
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    MAX_ITERATIONS = 20
    system_prompt = system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Write or overwrite files
        - Execute Python files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

        If the user suggests to fix a file you have to authority to overwrite it.

        Make sure to handle errors gracefully and provide informative messages to the user.
        """

    config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
    )

    for i in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=config,
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            if response.function_calls:
                for function_call_part in response.function_calls:
                    if verbose:
                        if verbose:
                            print(f"- Calling function: {function_call_part.name}({function_call_part.args})")

                    function_call_result = call_function(function_call_part, verbose=verbose)
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                    messages.append(function_call_result)
            if response.text:
                print("Final response:")
                print(response.text)
                break

        except Exception as e:
            print(f"Error during iteration {i+1}: {e}")
            break
    else:
        print("Reached max iterations without a final response.")




        

if __name__ == "__main__":
    main()