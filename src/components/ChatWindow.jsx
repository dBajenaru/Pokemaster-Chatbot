import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ChatWindow({ activeChat, loading, messagesEndRef }) {
  return (
    <div className="messages">
      {activeChat?.messages.length ? (
        activeChat.messages.map((message) => (
          <div
            key={message.id}
            className={`message-row ${message.role === 'user' ? 'user-row' : 'assistant-row'}`}
          >
            <div className={`message-bubble ${message.role === 'user' ? 'user-bubble' : 'assistant-bubble'}`}>
              {message.role === 'assistant' ? (
                <div className="markdown-body">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </ReactMarkdown>
                </div>
              ) : (
                <p className="message-text">{message.content}</p>
              )}
            </div>
          </div>
        ))
      ) : (
        <div className="empty-state">
          <h1 className="empty-title">Pokemaster</h1>
          <p className="empty-text">Ask a Pokémon question to start this chat.</p>
        </div>
      )}

      {loading && (
        <div className="message-row assistant-row">
          <div className="message-bubble assistant-bubble">Thinking...</div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}
