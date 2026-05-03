import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv

# Loads the .env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# Set variables from .env
chroma_path = os.getenv("CHROMA_PATH")
collection_name = os.getenv("CHROMA_COLLECTION")


# Builds the db
if __name__ == "__main__":
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection(name=collection_name)