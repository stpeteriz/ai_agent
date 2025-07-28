import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    
    # Generate content
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    # Print the response 
    print(response.text)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        

if __name__ == "__main__":
    main()