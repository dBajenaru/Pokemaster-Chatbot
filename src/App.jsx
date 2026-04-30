import { useEffect, useMemo, useRef, useState } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import Composer from './components/Composer';
import { createChat } from './data/createChat';
import { sendChatQuestion } from './services/chatApi';

export default function App() {
  const [chats, setChats] = useState([createChat()]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const activeChat = useMemo(() => {
    const currentId = activeChatId ?? chats[0]?.id;
    return chats.find((chat) => chat.id === currentId) ?? chats[0];
  }, [chats, activeChatId]);

  useEffect(() => {
    if (!activeChatId && chats[0]) {
      setActiveChatId(chats[0].id);
    }
  }, [activeChatId, chats]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [activeChat?.messages, loading]);

  function handleNewChat() {
    const newChat = createChat();
    setChats((prev) => [newChat, ...prev]);
    setActiveChatId(newChat.id);
    setQuestion('');
  }

  function updateActiveChat(updater) {
    setChats((prev) =>
      prev.map((chat) => (chat.id === activeChat.id ? updater(chat) : chat))
    );
  }

  async function handleAsk() {
    if (!question.trim() || !activeChat || loading) return;

    const currentQuestion = question.trim();

    const userMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: currentQuestion,
    };

    const chatTitle =
      activeChat.messages.length === 0
        ? currentQuestion.slice(0, 32)
        : activeChat.title;

    updateActiveChat((chat) => ({
      ...chat,
      title: chatTitle || 'New chat',
      messages: [...chat.messages, userMessage],
    }));

    setQuestion('');
    setLoading(true);

    try {
      const answer = await sendChatQuestion(currentQuestion);

      updateActiveChat((chat) => ({
        ...chat,
        messages: [
          ...chat.messages,
          {
            id: crypto.randomUUID(),
            role: 'assistant',
            content: answer,
          },
        ],
      }));
    } catch (error) {
      updateActiveChat((chat) => ({
        ...chat,
        messages: [
          ...chat.messages,
          {
            id: crypto.randomUUID(),
            role: 'assistant',
            content: error.message || 'Could not reach backend.',
          },
        ],
      }));
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  }

  return (
    <div className="app-shell">
      <Sidebar
        chats={chats}
        activeChatId={activeChat?.id}
        onSelectChat={setActiveChatId}
        onNewChat={handleNewChat}
      />

      <main className="main-panel">
        <ChatWindow
          activeChat={activeChat}
          loading={loading}
          messagesEndRef={messagesEndRef}
        />

        <Composer
          question={question}
          setQuestion={setQuestion}
          onAsk={handleAsk}
          onKeyDown={handleKeyDown}
          loading={loading}
        />
      </main>
    </div>
  );
}