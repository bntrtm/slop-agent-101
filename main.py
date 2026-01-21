import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    print("Hello from build-ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("MISSING ENV VARIABLE: 'GEMINI_API_KEY'")
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )
    if resp.usage_metadata is None:
        raise RuntimeError("API RESPONSE FAILED")
    if args.verbose:
        print("Prompt tokens: " + str(resp.usage_metadata.prompt_token_count))
        print("Response tokens: " + str(resp.usage_metadata.candidates_token_count))
        print("User prompt: " + resp.text)
    else:
        if resp.function_calls is not None:
            for call in resp.function_calls:
                print(f"Calling function: {call.name}({call.args})")
        else:
            print(resp.text)


if __name__ == "__main__":
    main()
