"""
Chatbot with ChromaDB tool integration for Foundry Agent.

This module implements a conversational agent with tool calling support.
"""
import json
import sys

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

from src.config import settings
from src.tools.chroma_tool import CHROMA_SEARCH_TOOL, execute_tool

project_endpoint = settings.AZURE_PROJECT_ENDPOINT
deployment_name = settings.AZURE_DEPLOYMENT_NAME
base_url = project_endpoint.rstrip("/") + "/openai/v1"

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential,
    "https://ai.azure.com/.default",
)

client = OpenAI(
    base_url=base_url,
    api_key=token_provider(),
)


def get_next_user_input():
    """Get the next user input from stdin or interactive prompt."""
    if sys.stdin.isatty():
        try:
            return input("You: ")
        except EOFError:
            return None

    line = sys.stdin.readline()
    if not line:
        return None
    return line.rstrip("\n")


def process_tool_calls(tool_calls):
    """Process tool calls from the model response."""
    tool_messages = []

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(f"[Tool] Calling {function_name} with: {arguments}")
        result = execute_tool(function_name, arguments)

        tool_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result),
        })

        print(f"[Tool] Result: {result['results_found']} results found\n")

    return tool_messages


def run_agent_turn(client, deployment_name, messages, tools, max_steps=5):
    for _ in range(max_steps):
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=1000,
        )

        choice = response.choices[0]
        message = choice.message

        print("[DEBUG] finish_reason:", choice.finish_reason)
        print("[DEBUG] content:", repr(message.content))
        print("[DEBUG] tool_calls:", message.tool_calls)

        if message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in message.tool_calls
                ],
            })

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"[Tool] Calling {function_name} with: {arguments}")
                result = execute_tool(function_name, arguments)
                print(f"[Tool] Raw result: {json.dumps(result, indent=2)}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })

            continue

        final_text = (message.content or "").strip()
        if final_text:
            messages.append({"role": "assistant", "content": final_text})
            return final_text

        return "I queried the tools, but the model returned an empty response."

    return "I could not finish the request within the allowed tool-call steps."


def main():
    """Run the chatbot main loop with tool support."""
    messages = []
    tools = [CHROMA_SEARCH_TOOL]

    print("Pokemon TCG Chatbot with Knowledge Base Search")
    print("Type 'quit' or 'exit' to end the conversation.\n")

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

        bot_response = run_agent_turn(
            client=client,
            deployment_name=deployment_name,
            messages=messages,
            tools=tools,
        )

        print("Bot:", bot_response, "\n")


if __name__ == "__main__":
    main()