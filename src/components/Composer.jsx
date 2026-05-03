export default function Composer({ question, setQuestion, onAsk, onKeyDown, loading }) {
  return (
    <div className="composer-wrap">
      <div className="composer">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Ask Pokemaster anything..."
          rows={3}
          className="composer-textarea"
        />
        <button
          onClick={onAsk}
          disabled={loading || !question.trim()}
          className="send-button"
        >
          Send
        </button>
      </div>
    </div>
  );
}