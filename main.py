import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main() -> None:
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

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(0, 20):
        try:
            result = generate_content(client, messages, args.verbose)
            if result:
                print(f"result: {result}")
            print(result)
        except Exception as ex:
            print(f"Something went wrong when calling gemini: {ex}")
    print("Maximum of 20 function calls reached")
    sys.exit(1)


def generate_content(client: genai.Client, messages: list[types.Content], verbose: bool) -> str | None:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]),
        contents=messages)


    if response.usage_metadata is not None and verbose:
        print(f"Prompt tokens: {
              response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")

    candidates = response.candidates

    if candidates is not None:
        for candidate in candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)

        if function_call_result.parts[0].function_response is None:
            raise Exception(
                f"Error: FunctionResponseObject was None for the function{function_call}")

        if function_call_result.parts[0].function_response.response is None:
            raise Exception(
                f"Error: response Property of FunctionResponseObject was None for the function{function_call}")

        if verbose:
            print(
                f"-> {function_call_result.parts[0].function_response.response}")

        function_responses.append(function_call_result.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()
