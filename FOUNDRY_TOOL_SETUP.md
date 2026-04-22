# Adding ChromaDB Search Tool to Foundry Agent

This guide explains how to add the ChromaDB search tool to your Foundry agent.

## Method 1: Using Foundry SDK (Recommended)

If you're using the Foundry SDK, you can register the tool programmatically:

```python
from foundry_sdk import FoundryClient
from chroma_tool import CHROMA_SEARCH_TOOL, search_pokemon_knowledge

# Initialize Foundry client
foundry = FoundryClient()

# Get your agent
agent = foundry.agents.get("your-agent-id")

# Register the tool with your agent
agent.tools.register(
    name="search_pokemon_knowledge",
    definition=CHROMA_SEARCH_TOOL,
    implementation=search_pokemon_knowledge
)
```

## Method 2: Manual Tool Definition in Foundry UI

If the UI doesn't support tool creation, you need to use the Foundry API directly:

### Step 1: Get your Agent RID (Resource Identifier)

1. Navigate to your agent in Foundry
2. The RID is in the URL or agent settings

### Step 2: Use Foundry API to Add Tool

```python
import requests
import os
from chroma_tool import CHROMA_SEARCH_TOOL

# Your Foundry configuration
FOUNDRY_URL = "https://your-foundry-instance.palantirfoundry.com"
AGENT_RID = "ri.your.agent.rid"
TOKEN = os.getenv("FOUNDRY_TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Add tool to agent
response = requests.post(
    f"{FOUNDRY_URL}/api/v1/agents/{AGENT_RID}/tools",
    headers=headers,
    json=CHROMA_SEARCH_TOOL
)

print(response.json())
```

## Method 3: Using OpenAI SDK with Tool Definition

Since Foundry agents often use OpenAI-compatible APIs, you can use the tool definition directly:

```python
from openai import OpenAI
from chroma_tool import CHROMA_SEARCH_TOOL, execute_tool
import json

client = OpenAI(
    base_url="your-foundry-endpoint",
    api_key="your-api-key"
)

# Use the tool in your chat completions
response = client.chat.completions.create(
    model="your-agent-model",
    messages=[{"role": "user", "content": "What Pokemon expansions were released in 2016?"}],
    tools=[CHROMA_SEARCH_TOOL],
    tool_choice="auto"
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        result = execute_tool(tool_call.function.name, args)
        print(result)
```

## Tool Definition JSON (for manual configuration)

If you need to manually paste the tool definition in a config file or API request:

```json
{
  "type": "function",
  "function": {
    "name": "search_pokemon_knowledge",
    "description": "Search the Pokemon Trading Card Game knowledge base for information. Use this tool when you need to find specific information about Pokemon TCG expansions, sets, cards, or game mechanics that may not be in your training data.",
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
```

## Testing the Tool

Run the test script:

```bash
cd src
python chroma_tool.py
```

Or test with the integrated chatbot:

```bash
python chat_with_tools.py
```

## Deployment Considerations

### 1. ChromaDB Path Configuration
Ensure your `chroma_db` directory is accessible from wherever the agent runs:

```python
# In chroma_tool.py, you may need to use an absolute path
client = chromadb.PersistentClient(path="/absolute/path/to/chroma_db")
```

### 2. Environment Variables
Create a `.env` file with:
```
AZURE_PROJECT_ENDPOINT=your-endpoint
AZURE_DEPLOYMENT_NAME=your-deployment
FOUNDRY_TOKEN=your-token  # if using Foundry API
```

### 3. Dependencies
Add to `requirements.txt`:
```
chromadb
openai
azure-identity
python-dotenv
```

## Troubleshooting

**Issue**: "Cannot create tool in Foundry UI"
- **Solution**: Use the Foundry SDK or API methods above

**Issue**: "Tool not being called by agent"
- **Solution**: Check that the tool description clearly indicates when to use it
- Verify `tool_choice` is set to `"auto"` or the specific tool name

**Issue**: "ChromaDB not found"
- **Solution**: Ensure the path to `chroma_db` is correct and accessible
- Run `chroma_ingestion.py` first to populate the database

**Issue**: "Authentication errors"
- **Solution**: Verify your Azure credentials and Foundry tokens are valid
- Check that `DefaultAzureCredential()` has access to the required resources
