import { h } from 'preact';
import { useState } from 'preact/hooks';
import axios from 'axios';

const App = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setResult('');
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/query', { query });
      setResult(response.data.result);
    } catch (error) {
      console.error('Error:', error);
      setResult('Ein Fehler ist aufgetreten.');
    } finally {
      setIsLoading(false);
      setQuery('');
    }
  };

  const formatResult = (text) => {
    return text.split('\n').map((line, index) => {
      if (line.startsWith('Agent')) {
        return <h3 key={index}>{line}</h3>;
      } else if (line.endsWith(':')) {
        return <h4 key={index}>{line}</h4>;
      } else if (line.startsWith('-')) {
        return <li key={index}>{line.substring(1).trim()}</li>;
      } else if (line.trim() === '') {
        return <br key={index} />;
      } else {
        return <p key={index}>{line}</p>;
      }
    });
  };

  return (
    <div>
      <h1>AI Query System</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Stellen Sie Ihre Frage..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Wird verarbeitet...' : 'Anfragen'}
        </button>
      </form>
      {isLoading && (
        <div class="loading-bar">
          <div class="loading-progress"></div>
        </div>
      )}
      {result && (
        <div>
          <h2>Antwort:</h2>
          <div>{formatResult(result)}</div>
        </div>
      )}
    </div>
  );
};

export default App;