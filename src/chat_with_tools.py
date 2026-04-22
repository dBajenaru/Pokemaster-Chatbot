"""
Chatbot with ChromaDB tool integration for Foundry Agent.

This module implements a conversational agent with tool calling support.
"""
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

from chroma_tool import CHROMA_SEARCH_TOOL, execute_tool


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
    """
    Process tool calls from the model response.
    
    Args:
        tool_calls: List of tool call objects from the model
    
    Returns:
        list: Tool call result messages to add to conversation
    """
    tool_messages = []
    
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"[Tool] Calling {function_name} with: {arguments}")
        
        # Execute the tool
        result = execute_tool(function_name, arguments)
        
        # Add tool response to messages
        tool_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })
        
        print(f"[Tool] Result: {result['results_found']} results found\n")
    
    return tool_messages


def main():
    """Run the chatbot main loop with tool support."""
    messages = []
    tools = [CHROMA_SEARCH_TOOL]  # Register available tools
    
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

        # Make API call with tools
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # Let the model decide when to use tools
            max_tokens=1000,
        )

        response_message = response.choices[0].message
        
        # Check if the model wants to call a tool
        if response_message.tool_calls:
            # Add assistant's tool call message to history
            messages.append({
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in response_message.tool_calls
                ]
            })
            
            # Process tool calls and get results
            tool_messages = process_tool_calls(response_message.tool_calls)
            messages.extend(tool_messages)
            
            # Get final response from model after tool execution
            response = client.chat.completions.create(
                model=deployment_name,
                messages=messages,
                tools=tools,
                max_tokens=1000,
            )
            
            response_message = response.choices[0].message
        
        # Add final assistant response to history
        bot_response = response_message.content
        messages.append({"role": "assistant", "content": bot_response})

        print("Bot:", bot_response, "\n")


if __name__ == "__main__":
    main()
