"""
Chatbot using Azure OpenAI.

This module implements a conversational agent.
"""
import sys

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI


from src.config import settings


# imports
project_endpoint = settings.AZURE_PROJECT_ENDPOINT
deployment_name = settings.AZURE_DEPLOYMENT_NAME
base_url = project_endpoint.rstrip("/") + "/openai/v1"


credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential, "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=base_url,
    api_key=token_provider(),
)


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



def _process_response(response):
    """Process model response.

    Args:
        response: The OpenAI chat completion response object.

    Returns:
        str: The final bot response text.
    """
    return response.choices[0].message.content


def main():
    """Run the chatbot main loop."""
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
            max_tokens=500,
        )

        bot_response = _process_response(response)
        messages.append({"role": "assistant", "content": bot_response})

        print("Bot:", bot_response, "\n")


if __name__ == "__main__":
    main()

