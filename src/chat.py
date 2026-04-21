"""
Pokémon TCG chatbot using Azure OpenAI with tool use capabilities.

This module implements a conversational agent that can answer questions
about Pokémon TCG cards, sets, and related information by calling
external API tools.
"""
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

from tcg_api import get_card_info, get_sets, get_most_recent_set

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

project_endpoint = os.getenv("AZURE_PROJECT_ENDPOINT")
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

if not project_endpoint or not deployment_name:
    raise RuntimeError(
        "Missing AZURE_PROJECT_ENDPOINT or AZURE_DEPLOYMENT_NAME "
        "environment variable. Put them in .env or export them in "
        "your shell."
    )

base_url = project_endpoint.rstrip("/") + "/openai/v1"

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential, "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=base_url,
    api_key=token_provider(),
)


def _get_tools():
    """Define tool functions available to the chat model.

    Returns:
        list: List of tool definitions in OpenAI format.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "get_card_info",
                "description": (
                    "Get detailed information about a specific "
                    "Pokémon TCG card by name"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "card_name": {
                            "type": "string",
                            "description": (
                                "The exact name of the Pokémon card "
                                "(e.g., 'Pikachu')"
                            ),
                        }
                    },
                    "required": ["card_name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_sets",
                "description": (
                    "Get a list of all Pokémon TCG expansion sets "
                    "with release dates"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_most_recent_set",
                "description": "Get the most recent Pokémon TCG expansion set",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
    ]

def get_next_user_input():
    """Get the next user input from stdin or interactive prompt.

    Handles both interactive mode (TTY) and piped input streams.

    Returns:
        str or None: The user input string, or None if EOF is reached.
    """
    if sys.stdin.isatty():
        try:
            return input("You: ")
        except EOFError:
            return None
    line = sys.stdin.readline()
    if not line:
        return None
    return line.rstrip("\n")


def _execute_tool_call(function_name, arguments):
    """Execute a tool function and return the result.

    Args:
        function_name (str): Name of the tool function to execute.
        arguments (dict): Arguments to pass to the tool function.

    Returns:
        str: JSON-formatted result from the tool or error message.
    """
    if function_name == "get_card_info":
        return get_card_info(arguments["card_name"])
    elif function_name == "get_sets":
        return get_sets()
    elif function_name == "get_most_recent_set":
        return get_most_recent_set()
    else:
        return "Unknown tool"


def _process_response(response, messages, tools):
    """Process model response and handle tool calls if present.

    Args:
        response: The OpenAI chat completion response object.
        messages (list): Conversation message history.
        tools (list): Available tool definitions.

    Returns:
        str: The final bot response text.
    """
    # Check for tool calls
    if (hasattr(response.choices[0].message, "tool_calls") and
            response.choices[0].message.tool_calls):
        tool_calls = response.choices[0].message.tool_calls
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": tool_calls,
        })

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            result = _execute_tool_call(function_name, arguments)

            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id,
            })

        # Get final response after tool use
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=500,
        )

    return response.choices[0].message.content


def main():
    """Run the Pokémon TCG chatbot main loop."""
    tools = _get_tools()
    messages = []

    while True:
        user_input = get_next_user_input()
        if user_input is None:
            break

        if not user_input.strip():
            continue

        if user_input.lower() in ["quit", "exit"]:
            break

        if not sys.stdin.isatty():
            print("You:", user_input)

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            tools=tools,
            max_tokens=500,
        )

        bot_response = _process_response(response, messages, tools)
        messages.append({"role": "assistant", "content": bot_response})

        print("Bot:", bot_response, "\n")


if __name__ == "__main__":
    main()

