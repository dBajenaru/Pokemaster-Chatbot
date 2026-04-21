from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

project_endpoint = os.getenv("AZURE_PROJECT_ENDPOINT")
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

if not project_endpoint or not deployment_name:
    raise RuntimeError(
        "Missing AZURE_PROJECT_ENDPOINT or AZURE_DEPLOYMENT_NAME environment variable. "
        "Put them in .env or export them in your shell."
    )

base_url = project_endpoint.rstrip("/") + "/openai/v1"

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")

client = OpenAI(
    base_url=base_url,
    api_key=token_provider(),
)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        break

    response = client.responses.create(
        model=deployment_name,
        input=user_input,
        max_output_tokens=500,
    )

    print("Bot:", response.output_text)
