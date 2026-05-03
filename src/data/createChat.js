export function createChat(title = 'New chat') {
  return {
    id: crypto.randomUUID(),
    title,
    messages: [],
    createdAt: Date.now(),
  };
}