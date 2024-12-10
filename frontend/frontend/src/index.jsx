import { h, render } from 'preact';
import { useState } from 'preact/hooks';
import axios from 'axios';
import Markdown from 'markdown-to-jsx';
import './style.css';

const Logo = () => (
<svg fill="#45a049" width="70px" height="70px" viewBox="0 0 32 32" id="icon" xmlns="http://www.w3.org/2000/svg">
  <defs>
	<style>{`
	  .cls-1 {
		fill: none;
	  }
	`}</style>
  </defs>
  <path d="M27,24a2.9609,2.9609,0,0,0-1.2854.3008L21.4141,20H18v2h2.5859l3.7146,3.7148A2.9665,2.9665,0,0,0,24,27a3,3,0,1,0,3-3Zm0,4a1,1,0,1,1,1-1A1.0009,1.0009,0,0,1,27,28Z"/>
  <path d="M27,13a2.9948,2.9948,0,0,0-2.8157,2H18v2h6.1843A2.9947,2.9947,0,1,0,27,13Zm0,4a1,1,0,1,1,1-1A1.0009,1.0009,0,0,1,27,17Z"/>
  <path d="M27,2a3.0033,3.0033,0,0,0-3,3,2.9657,2.9657,0,0,0,.3481,1.373L20.5957,10H18v2h3.4043l4.3989-4.2524A2.9987,2.9987,0,1,0,27,2Zm0,4a1,1,0,1,1,1-1A1.0009,1.0009,0,0,1,27,6Z"/>
  <path d="M18,6h2V4H18a3.9756,3.9756,0,0,0-3,1.3823A3.9756,3.9756,0,0,0,12,4H11a9.01,9.01,0,0,0-9,9v6a9.01,9.01,0,0,0,9,9h1a3.9756,3.9756,0,0,0,3-1.3823A3.9756,3.9756,0,0,0,18,28h2V26H18a2.0023,2.0023,0,0,1-2-2V8A2.0023,2.0023,0,0,1,18,6ZM12,26H11a7.0047,7.0047,0,0,1-6.92-6H6V18H4V14H7a3.0033,3.0033,0,0,0,3-3V9H8v2a1.0009,1.0009,0,0,1-1,1H4.08A7.0047,7.0047,0,0,1,11,6h1a2.0023,2.0023,0,0,1,2,2v4H12v2h2v4H12a3.0033,3.0033,0,0,0-3,3v2h2V21a1.0009,1.0009,0,0,1,1-1h2v4A2.0023,2.0023,0,0,1,12,26Z"/>
  <rect id="_Transparent_Rectangle_" data-name="&lt;Transparent Rectangle&gt;" class="cls-1" width="32" height="32"/>
</svg>
);

const Header = () => (
	<div className="header">
	  <div className="logo">
		<Logo/>
	  </div>
	  <h1 className="title">KETE Projekt 2024</h1>
	  <div className="additional-content">
		{/* Platz für weitere Dinge */}
	  </div>
	</div>
  );

const App = () => {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setIsLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/query', {
        query,
      });
      setChatHistory((prev) => [
        ...prev,
        { question: query, answer: response.data.result },
      ]);
    } catch (error) {
      console.error('Error:', error);
      setChatHistory((prev) => [
        ...prev,
        { question: query, answer: 'Ein Fehler ist aufgetreten.' },
      ]);
    } finally {
      setIsLoading(false);
      setQuery('');
    }
  };

  const handleInputChange = (e) => {
	setQuery(e.currentTarget.value);
  };

  return (
		<>
		<Header/>
		<div className="chat-container">
		  <div className="chat-history">
			  {chatHistory.slice().reverse().map((entry, index) => (
				  <div key={index} className="chat-entry">
					  <div className="chat-question">
						  <span className="message-badge">I</span>
						  {entry.question}
					  </div>
					  <div className="chat-answer">
						  <span className="message-badge">A</span>
						  <Markdown
							  options={{
								  forceBlock: true,
								  overrides: {
									  h1: { props: { className: 'answer-heading' } },
									  h2: { props: { className: 'answer-subheading' } },
									  p: { props: { className: 'answer-paragraph' } },
									  ul: { props: { className: 'answer-list' } },
									  li: { props: { className: 'answer-list-item' } },
								  },
							  }}
						  >{entry.answer}</Markdown>
					  </div>
				  </div>
			  ))}
		  </div>
		  <form onSubmit={handleSubmit} className="chat-input">
			  <input
				  type="text"
				  value={query}
				  onChange={(e) => setQuery(e.currentTarget.value)}
				  placeholder="Stellen Sie Ihre Frage..."
				  disabled={isLoading} />
			  <button type="submit" disabled={isLoading}>
				  {isLoading ? 'Wird verarbeitet...' : 'Senden'}
			  </button>
		  </form>
	  </div></>
  );
};

render(<App />, document.getElementById('app'));