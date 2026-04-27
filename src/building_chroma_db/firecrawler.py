import os
from pathlib import Path

from dotenv import load_dotenv
from firecrawl import Firecrawl
import chromadb


env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

firecrawl = Firecrawl(api_key=firecrawl_api_key)