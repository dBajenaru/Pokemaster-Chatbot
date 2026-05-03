from flask import Flask, request, jsonify
from flask_cors import CORS

from src.config import settings
from src.agents.chat_with_tools import (
    client,
    deployment_name,
    CHROMA_SEARCH_TOOL,
    run_agent_turn,
)


app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

tools = [CHROMA_SEARCH_TOOL]

# In-memory session store:
# {
#   "chat-id-1": [ {role: "...", content: "..."}, ... ],
#   "chat-id-2": [ ... ]
# }
chat_sessions = {}


@app.get("/")
def home():
    return jsonify({"status": "ok"})


@app.get("/chats")
def list_chats():
    return jsonify({
        "chatIds": list(chat_sessions.keys())
    })


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}

    chat_id = (data.get("chatId") or "").strip()
    question = (data.get("question") or "").strip()

    if not chat_id:
        return jsonify({"error": "chatId is required"}), 400

    if not question:
        return jsonify({"error": "Question is required"}), 400

    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = []

    messages = chat_sessions[chat_id]
    messages.append({"role": "user", "content": question})

    try:
        answer = run_agent_turn(
            client=client,
            deployment_name=deployment_name,
            messages=messages,
            tools=tools,
        )

        return jsonify({
            "chatId": chat_id,
            "answer": answer,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/chat/reset")
def reset_chat():
    data = request.get_json(silent=True) or {}
    chat_id = (data.get("chatId") or "").strip()

    if not chat_id:
        return jsonify({"error": "chatId is required"}), 400

    chat_sessions[chat_id] = []
    return jsonify({"chatId": chat_id, "status": "reset"})


@app.delete("/chat/<chat_id>")
def delete_chat(chat_id):
    chat_sessions.pop(chat_id, None)
    return jsonify({"chatId": chat_id, "status": "deleted"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)