export default function Sidebar({ chats, activeChatId, onSelectChat, onNewChat }) {
  return (
    <aside className="sidebar">
      <button className="new-chat-button" onClick={onNewChat}>
        + New chat
      </button>

      <div className="history-list">
        {chats.map((chat) => (
          <button
            key={chat.id}
            className={`history-item ${chat.id === activeChatId ? 'active' : ''}`}
            onClick={() => onSelectChat(chat.id)}
          >
            {chat.title}
          </button>
        ))}
      </div>
    </aside>
  );
}
