"""
ChromaDB Search Tool for Foundry Agent

This module defines a tool for searching the ChromaDB knowledge base
and provides the implementation function.
"""
import chromadb


# Tool definition in OpenAI function calling format
CHROMA_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_pokemon_knowledge",
        "description": (
            "Search the Pokemon Trading Card Game knowledge base for information. "
            "Use this tool when you need to find specific information about Pokemon TCG "
            "expansions, sets, cards, or game mechanics that may not be in your training data."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant information in the knowledge base"
                },
                "n_results": {
                    "type": "integer",
                    "description": "Number of results to return (default: 3, max: 10)",
                    "default": 3
                }
            },
            "required": ["query"]
        }
    }
}


def search_pokemon_knowledge(query: str, n_results: int = 3) -> dict:
    """
    Search the ChromaDB knowledge base for Pokemon TCG information.
    
    Args:
        query: The search query string
        n_results: Number of results to return (default: 3, max: 10)
    
    Returns:
        dict: Search results with documents, metadata, and distances
    """
    if n_results > 10:
        n_results = 10
    if n_results < 1:
        n_results = 1
        
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="web_knowledge")
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    # Format results for the agent
    formatted_results = []
    if results and results['documents'] and results['documents'][0]:
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i] if results['metadatas'] else {}
            distance = results['distances'][0][i] if results['distances'] else None
            
            formatted_results.append({
                "content": doc,
                "source": metadata.get("url", "unknown"),
                "title": metadata.get("title", ""),
                "relevance_score": f"{1 - distance:.3f}" if distance is not None else "N/A"
            })
    
    return {
        "query": query,
        "results_found": len(formatted_results),
        "results": formatted_results
    }


# Tool registry mapping function names to implementations
TOOL_FUNCTIONS = {
    "search_pokemon_knowledge": search_pokemon_knowledge
}


def execute_tool(tool_name: str, arguments: dict) -> dict:
    """
    Execute a tool by name with the given arguments.
    
    Args:
        tool_name: Name of the tool to execute
        arguments: Dictionary of arguments to pass to the tool
    
    Returns:
        dict: Result from the tool execution
    """
    if tool_name not in TOOL_FUNCTIONS:
        return {"error": f"Unknown tool: {tool_name}"}
    
    try:
        return TOOL_FUNCTIONS[tool_name](**arguments)
    except Exception as e:
        return {"error": f"Tool execution failed: {str(e)}"}


if __name__ == "__main__":
    # Test the tool
    result = search_pokemon_knowledge("What are the expansion sets of the Mega Evolution era?")
    print("Search Results:")
    print(f"Query: {result['query']}")
    print(f"Results found: {result['results_found']}\n")
    
    for i, res in enumerate(result['results'], 1):
        print(f"Result {i}:")
        print(f"  Title: {res['title']}")
        print(f"  Source: {res['source']}")
        print(f"  Relevance: {res['relevance_score']}")
        print(f"  Content: {res['content'][:200]}...")
        print()
