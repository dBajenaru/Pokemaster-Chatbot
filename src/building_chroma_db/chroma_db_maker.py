import chromadb

client = chromadb.PersistentClient(path="./chromaDB")

collection = client.get_or_create_collection("pokemon_knowledge")
