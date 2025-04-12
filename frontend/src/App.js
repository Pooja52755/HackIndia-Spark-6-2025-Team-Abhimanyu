import React from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="App">
      <main>
        <div className="app-layout">
          <ChatInterface />
        </div>
      </main>
      
      <footer className="main-footer">
        <p>&copy; 2025 Cybersecurity Knowledge Assistant | <a href="#">Privacy Policy</a> | <a href="#">Terms of Use</a></p>
      </footer>
    </div>
  );
}

export default App;