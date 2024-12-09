import { h } from 'preact';
import { useState } from 'preact/hooks';

const AIQueryInput = ({ onQuery }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onQuery(query);
      setQuery('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onInput={e => setQuery(e.target.value)}
        placeholder="Stellen Sie eine Frage an die KI..."
      />
      <button type="submit">Fragen</button>
    </form>
  );
};

export default AIQueryInput;