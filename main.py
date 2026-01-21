import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    print("Hello from build-ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("MISSING ENV VARIABLE: 'GEMINI_API_KEY'")
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print("User prompt: " + args.user_prompt)
    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )
    if resp.usage_metadata is None:
        raise RuntimeError("Gemini API response is malformed")
    if verbose:
        print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
        print("Response tokens:", resp.usage_metadata.candidates_token_count)
    func_results = []
    if resp.function_calls is None:
        print("Response:")
        print(resp.text)
        return
    for call in resp.function_calls:
        func_result = call_function(call, True)
        if (
            not func_result.parts
            or not func_result.parts[0].function_response
            or not func_result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {func_result.name}")
        if verbose:
            print(f"-> {func_result.parts[0].function_response.response}")

        func_results.append(func_result.parts[0])


if __name__ == "__main__":
    main()
