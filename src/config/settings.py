import os
from dotenv import load_dotenv
from .paths import ENV_PATH


load_dotenv(ENV_PATH)


def required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


AZURE_PROJECT_ENDPOINT = required("AZURE_PROJECT_ENDPOINT")
AZURE_DEPLOYMENT_NAME = required("AZURE_DEPLOYMENT_NAME")
MODEL_NAME = os.getenv("MODEL_NAME", "default-model")
