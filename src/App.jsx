import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleAsk() {
    if (!question.trim()) return;

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Request failed');
      }

      setAnswer(data.answer || '');
    } catch (err) {
      setError(err.message || 'Could not reach backend');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <h1>Pokemaster</h1>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        rows={5}
        placeholder="Ask a Pokémon question..."
        style={{ width: '100%', padding: '1rem' }}
      />

      <button onClick={handleAsk} disabled={loading} style={{ marginTop: '1rem' }}>
        {loading ? 'Thinking...' : 'Ask'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <section style={{ marginTop: '2rem' }}>
        <h2>Answer</h2>
        <div className="markdown-body" style={{ textAlign: 'left' }}>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {answer}
          </ReactMarkdown>
        </div>
      </section>
    </main>
  );
}