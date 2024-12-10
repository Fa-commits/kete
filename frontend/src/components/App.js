import { h } from "preact";
import { useState } from "preact/hooks";
import axios from "axios";
import ReactMarkdown from "react-markdown";

const App = () => {
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/query", {
        query,
      });
      setChatHistory((prev) => [
        ...prev,
        { question: query, answer: response.data.result },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setChatHistory((prev) => [
        ...prev,
        { question: query, answer: "Ein Fehler ist aufgetreten." },
      ]);
    } finally {
      setIsLoading(false);
      setQuery("");
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {chatHistory.map((entry, index) => (
          <div key={index} className="chat-entry">
            <div className="chat-question">
              <span className="message-badge">I</span>
              {entry.question}
            </div>
            <div className="chat-answer">
              <span className="message-badge">A</span>
              <ReactMarkdown>{entry.answer}</ReactMarkdown>
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Stellen Sie Ihre Frage..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Wird verarbeitet..." : "Senden"}
        </button>
      </form>
    </div>
  );
};

export default App;
