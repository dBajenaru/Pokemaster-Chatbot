export async function sendChatQuestion(question) {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || 'Request failed.');
  }

  return data.answer || 'No answer returned.';
}