import hashlib
from datetime import datetime, timezone

import chromadb
import requests
from bs4 import BeautifulSoup


def chunk_text(text, chunk_size=1200, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += max(1, chunk_size - overlap)
    return chunks


def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""
    text = " ".join(soup.get_text(separator=" ").split())
    return title, text


def ingest_url_to_chroma(
    url,
    collection_name="web_knowledge",
    chroma_path="./chroma_db",
    source_name="web"
):
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection(name=collection_name)

    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "MyAppBot/1.0"}
    )
    response.raise_for_status()

    title, text = extract_text_from_html(response.text)
    chunks = chunk_text(text)

    scraped_at = datetime.now(timezone.utc).isoformat()
    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        chunk_id = hashlib.md5(f"{url}:{i}:{chunk}".encode("utf-8")).hexdigest()
        ids.append(chunk_id)
        documents.append(chunk)
        metadatas.append({
            "url": url,
            "title": title,
            "source": source_name,
            "chunk_index": i,
            "scraped_at": scraped_at
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return {
        "url": url,
        "title": title,
        "chunks_ingested": len(chunks),
        "collection": collection_name
    }


if __name__ == "__main__":
    result = ingest_url_to_chroma("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_Trading_Card_Game_expansions")
    print(result)