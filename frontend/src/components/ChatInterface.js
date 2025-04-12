import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';
import axios from 'axios';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  // Sample questions for the welcome screen
  const sampleQuestions = [
    "What are the most common cybersecurity threats?",
    "How can I protect against SQL injection attacks?",
    "What tools are used for network security?",
    "What's the difference between IDS and IPS?",
    "Which threats are classified as data theft?",
    "How are ransomware attacks mitigated?",
    "What are the best practices for endpoint security?",
    "How do firewalls protect networks?"
  ];

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Format message text to handle markdown-like formatting
  const formatMessageText = (text) => {
    if (!text) return '';
    
    // Replace markdown bold with HTML strong tags
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Replace bullet points
    text = text.replace(/^•\s+(.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.+<\/li>)/gs, '<ul>$1</ul>');
    
    // Replace numbered lists
    text = text.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.+<\/li>)/gs, '<ol>$1</ol>');
    
    // Replace paragraphs (double newlines)
    text = text.replace(/\n\n/g, '</p><p>');
    
    // Wrap in paragraph tags
    text = `<p>${text}</p>`;
    
    // Fix any duplicate tags from the replacements
    text = text.replace(/<\/p><p><ul>/g, '<ul>');
    text = text.replace(/<\/ul><\/p><p>/g, '</ul>');
    text = text.replace(/<\/p><p><ol>/g, '<ol>');
    text = text.replace(/<\/ol><\/p><p>/g, '</ol>');
    
    return text;
  };
  
  // Get current time for message timestamp
  const getFormattedTime = () => {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message to chat with timestamp
    const userMessage = { 
      text: input, 
      sender: 'user', 
      timestamp: getFormattedTime() 
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Send request to backend
      const response = await axios.post('/chat', { message: input });
      
      // Add bot response to chat with timestamp
      setMessages(prev => [...prev, { 
        text: response.data.response, 
        sender: 'bot',
        timestamp: getFormattedTime()
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        text: 'Sorry, there was an error processing your request. Please try again.', 
        sender: 'bot',
        timestamp: getFormattedTime() 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle clicking on sample questions
  const handleSampleQuestionClick = (question) => {
    setInput(question);
  };
  
  // Function to handle keyboard shortcuts
  const handleKeyDown = (e) => {
    // Submit on Enter (but not with Shift+Enter)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && !isLoading) {
        handleSendMessage(e);
      }
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Cybersecurity Knowledge Chatbot</h1>
        <p>Powered by Google Gemini</p>
      </div>
      
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h2>Welcome to the Cybersecurity Knowledge Chatbot!</h2>
            <p>Ask me anything about cybersecurity threats, defenses, or best practices. I'm here to help you understand the complex world of cybersecurity using structured knowledge and AI.</p>
            
            <div className="sample-questions-container">
              <h3>Try asking one of these questions:</h3>
              <div className="sample-questions">
                {sampleQuestions.map((question, index) => (
                  <div 
                    key={index} 
                    className="sample-question-card"
                    onClick={() => handleSampleQuestionClick(question)}
                  >
                    <p>{question}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <div className="message-content">
                {message.sender === 'bot' ? (
                  <div 
                    className="formatted-message"
                    dangerouslySetInnerHTML={{ __html: formatMessageText(message.text) }}
                  />
                ) : (
                  <p>{message.text}</p>
                )}
                <div className="message-timestamp">{message.timestamp}</div>
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="message bot">
            <div className="message-content loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        {/* Invisible element for auto-scrolling */}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="input-container" onSubmit={handleSendMessage}>
        <div className="input-box">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your cybersecurity question here..."
            disabled={isLoading}
            autoFocus
          />
        </div>
        <button type="submit" disabled={isLoading || !input.trim()}>
          Send
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
          </svg>
        </button>
      </form>
      
      <div className="chat-footer">
        <p>&copy; 2025 Cybersecurity Knowledge Chatbot</p>
      </div>
    </div>
  );
};

export default ChatInterface;