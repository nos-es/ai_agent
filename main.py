import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true",
                    help="Enable verbose output")
args = parser.parse_args()
messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions]),
    contents=messages)


if response.usage_metadata is not None and args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if response.function_calls:
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose)
        if function_call_result.parts[0].function_response is None:
            raise Exception(
                f"Error: FunctionResponseObject was None for the function{function_call}")

        if function_call_result.parts[0].function_response.response is None:
            raise Exception(
                f"Error: response Property of FunctionResponseObject was None for the function{function_call}")
        if args.verbose:
            print(
                f"-> {function_call_result.parts[0].function_response.response}")


print(f"Response: {response.text}")
