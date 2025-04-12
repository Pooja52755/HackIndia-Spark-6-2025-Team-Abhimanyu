import React from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Cybersecurity Knowledge Assistant</h1>
        <p>Explore cybersecurity concepts with AI and structured knowledge</p>
      </header>
      
      <main>
        <div className="app-layout">
          <ChatInterface />
        </div>
      </main>
      
      <footer>
        <div className="footer-content">
          <div className="footer-section">
            <h3>About</h3>
            <p>This chatbot combines MeTTa knowledge representation with Google Gemini's natural language capabilities to provide accurate cybersecurity information.</p>
          </div>
          <div className="footer-section">
            <h3>Resources</h3>
            <ul>
              <li><a href="#">Cybersecurity Best Practices</a></li>
              <li><a href="#">Threat Intelligence</a></li>
              <li><a href="#">Security Tools Guide</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h3>Contact</h3>
            <p>For support or feedback, please <a href="mailto:support@example.com">contact us</a>.</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2025 Cybersecurity Knowledge Chatbot | All Rights Reserved</p>
        </div>
      </footer>
    </div>
  );
}

export default App;