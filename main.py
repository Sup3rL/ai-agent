import json
import sys

from prompt import system_prompt
import argparse
import os
from openai import OpenAI
from dotenv import load_dotenv
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY environment variable is not set.")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    # Ensure usage information is available
    if response.usage is None:
        raise RuntimeError("Response usage is None. Please check your API key and model availability.")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Model: {response.model}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)


    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if not result_message.get("content"):
                raise Exception(f"Empty result from {tool_call.function.name}")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
    else:
        print("Final response:")
        print(message.content)
        break

else:
    print("Error: reached maximum iterations without a final response.")
    sys.exit(1)
    