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

client = chromadb.PersistentClient(path=chroma_path)
collection = client.get_collection(name=collection_name)

def list_num_of_records():
    return collection.count()

results = collection.query(
    query_texts=["What are the expansion sets of the Mega Evolution era?"],
    n_results=3
)

print(list_num_of_records())
# print(results)