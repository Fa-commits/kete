import { h } from 'preact';
import { useState, useEffect } from 'preact/hooks';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import AIQueryInput from './components/AIQueryInput';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [aiResponse, setAiResponse] = useState(null);

  const handleSend = (text) => {
    setMessages([...messages, { id: Date.now(), text, sender: 'user' }]);
  };

  const handleQuery = async (query) => {
    // Hier würden wir die Anfrage an unser Backend senden
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await response.json();
    setAiResponse(data.result);
  };

  useEffect(() => {
    if (aiResponse) {
      setMessages([...messages, { id: Date.now(), text: aiResponse, sender: 'ai' }]);
    }
  }, [aiResponse]);

  return (
    <div class="chat-app">
      <ChatWindow messages={messages} />
      <MessageInput onSend={handleSend} />
      <AIQueryInput onQuery={handleQuery} />
    </div>
  );
};

export default App;