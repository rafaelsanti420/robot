import { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/api/')
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage('error'));
  }, []);

  return (
    <div>
      <h1>Robot Platform UI</h1>
      <p>API says: {message}</p>
    </div>
  );
}

export default App;
