import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from config import LOOP_ITER_MAX


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
    if LOOP_ITER_MAX == 0:
        raise RuntimeError("INVALID LOOP ITERATION MAXIMUM: 0 (must be at least 1)")
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print("User prompt: " + args.user_prompt)
    for i in range(LOOP_ITER_MAX):
        try:
            resp = generate_content(client, messages, args.verbose)
            if resp:
                print("Response:")
                print(resp)
                return
        except Exception as e:
            print(f"Error while generating content: {e}")
    print(f"Error: reached maximum loop iterations ({LOOP_ITER_MAX})")
    sys.exit(1)


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
    if resp.candidates:
        for c in resp.candidates:
            if c.content:
                messages.append(c.content)
    if not resp.function_calls:
        return resp.text
    func_results = []
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
    messages.append(types.Content(role="user", parts=func_results))


if __name__ == "__main__":
    main()
