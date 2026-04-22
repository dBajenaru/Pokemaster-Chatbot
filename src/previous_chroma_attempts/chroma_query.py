import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="web_knowledge")

results = collection.query(
    query_texts=["What are the expansion sets of the Mega Evolution era?"],
    n_results=3
)

print(results)