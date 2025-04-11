import React from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Cybersecurity Knowledge Chatbot</h1>
        <p>Powered by MeTTa and Google Gemini</p>
      </header>
      <main>
        <ChatInterface />
      </main>
      <footer>
        <p>&copy; 2025 Cybersecurity Knowledge Chatbot</p>
      </footer>
    </div>
  );
}

export default App;