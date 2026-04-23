import os
from pathlib import Path

from dotenv import load_dotenv
from firecrawl import Firecrawl


env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

app = Firecrawl(api_key=firecrawl_api_key)

search_result = app.search("firecrawl", limit=5)

print(search_result)
