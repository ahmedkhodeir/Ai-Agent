import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import call_function

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


# ---------- Helpers ----------

def extract_function_calls(content: types.Content):
    """
    Safely extract function calls from Content.parts.
    In google-genai, function calls live inside parts as function_call.
    """
    calls = []
    for part in content.parts or []:
        if hasattr(part, "function_call") and part.function_call:
            calls.append(part.function_call)
    return calls


# ---------- Setup ----------

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ],
)


# ---------- Main ----------

def main():
    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Conversation history (the agent's memory)
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    max_iterations = 20

    for _ in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
                ),
            )

            # 1) Add model responses to conversation
            for candidate in response.candidates or []:
                messages.append(candidate.content)

            # 2) Collect function calls safely from parts
            function_calls = []
            for candidate in response.candidates or []:
                function_calls.extend(extract_function_calls(candidate.content))

            # 3) If no function calls and there is text -> final answer
            if not function_calls and response.text:
                print("Final response:")
                print(response.text)
                return

            # 4) Execute requested functions
            tool_parts = []
            for call in function_calls:
                tool_content = call_function(call, verbose=args.verbose)

                if (
                    not tool_content.parts
                    or not hasattr(tool_content.parts[0], "function_response")
                ):
                    raise RuntimeError("Invalid tool response format")

                tool_parts.append(tool_content.parts[0])

                if args.verbose:
                    print(f"-> {tool_content.parts[0].function_response.response}")

            # 5) Feed tool results back to the model as the next user message
            messages.append(
                types.Content(
                    role="user",
                    parts=tool_parts
                )
            )

        except Exception as e:
            print("Agent error:", e)
            sys.exit(1)

    print("Agent stopped: maximum iterations reached.")


if __name__ == "__main__":
    main()
