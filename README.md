# Notes on Files and Folders
 - `chroma_db/` is the vector database that stores all my agent's knowledge on pokemon. Currently not tracked as to not expose collected data.
 - `src/` is the folder holding all the python code.
 - `src/building_chroma_db/` is the folder where I'm holding all my files used in buiding my db.
 - `src/previous_chroma_attempts` : previous attempts to build a chromadb; I'm starting from scratch in `src/building_chroma_db` to not confuse myself with that was previously built. `./chroma_ingestion` is pretty clear. `./chroma_query is for asking chroma questions`. `./chroma_tools` defines a search tool to get knowledge from chroma db.