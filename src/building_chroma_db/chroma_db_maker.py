import os
from pathlib import Path

from dotenv import load_dotenv
from firecrawl import Firecrawl
import chromadb

# fircrawl logic
# env_path = Path(__file__).resolve().parents[2] / ".env"
# load_dotenv(dotenv_path=env_path)

# firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

# firecrawl = Firecrawl(api_key=firecrawl_api_key)

client = chromadb.PersistentClient(path="./chromaDB")
collection = client.get_or_create_collection("pokemon_knowledge")

URLS = [
    "https://www.pokemon.com/us/pokedex/bulbasaur",
    "https://www.pokemon.com/us/pokedex/charmander",
]


def chunk_text(text, chunk_size=1200, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def main():
    for url in URLS:
        doc = firecrawl.scrape(url, formats=[""])
        markdown = doc.get("markdown", "")

        if not markdown.strip():
            continue

        chunks = chunk_text(markdown)

        ids = []
