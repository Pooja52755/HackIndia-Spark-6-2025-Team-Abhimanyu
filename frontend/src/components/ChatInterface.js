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
  
  // Handle accordions toggle
  const toggleAccordion = (messageId, accordionIndex) => {
    setMessages(prevMessages => {
      return prevMessages.map(msg => {
        if (msg.id === messageId && msg.elements?.accordions) {
          const updatedAccordions = [...msg.elements.accordions];
          updatedAccordions[accordionIndex] = {
            ...updatedAccordions[accordionIndex],
            isOpen: !updatedAccordions[accordionIndex].isOpen
          };
          
          return {
            ...msg,
            elements: {
              ...msg.elements,
              accordions: updatedAccordions
            }
          };
        }
        return msg;
      });
    });
  };
  
  // Handle button actions
  const handleButtonClick = (action, text) => {
    // For now, we'll implement a simple action to insert the button text as a new query
    if (action === 'query') {
      setInput(text);
    } else if (action.startsWith('link:')) {
      window.open(action.substring(5), '_blank');
    }
  };
  
  // Get current time for message timestamp
  const getFormattedTime = () => {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Generate a unique ID for this message
    const messageId = `msg-${Date.now()}`;
    
    // Add user message to chat with timestamp
    const userMessage = { 
      id: `user-${messageId}`,
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
      const botResponse = { 
        id: `bot-${messageId}`,
        text: response.data.response, 
        sender: 'bot',
        timestamp: getFormattedTime(),
        elements: response.data.elements || {}
      };
      
      // Initialize isOpen property for accordions
      if (botResponse.elements?.accordions) {
        botResponse.elements.accordions = botResponse.elements.accordions.map(accordion => ({
          ...accordion,
          isOpen: false
        }));
      }
      
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        id: `error-${messageId}`,
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

  // Render message elements (images, links, etc.)
  const renderMessageElements = (message) => {
    if (!message.elements) return null;
    
    return (
      <div className="message-elements">
        {message.elements.images && message.elements.images.length > 0 && (
          <div className="message-images">
            {message.elements.images.map((image, index) => (
              <div key={`img-${index}`} className="message-image">
                <img 
                  src={image.url} 
                  alt={image.description} 
                  loading="lazy"
                />
                {image.description && (
                  <p className="image-caption">{image.description}</p>
                )}
              </div>
            ))}
          </div>
        )}
        
        {message.elements.links && message.elements.links.length > 0 && (
          <div className="message-links">
            <h4 className="links-heading">Useful Resources</h4>
            <ul className="links-list">
              {message.elements.links.map((link, index) => (
                <li key={`link-${index}`}>
                  <a href={link.url} target="_blank" rel="noopener noreferrer">
                    {link.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
        
        {message.elements.accordions && message.elements.accordions.length > 0 && (
          <div className="message-accordions">
            {message.elements.accordions.map((accordion, index) => (
              <div key={`accordion-${index}`} className="accordion">
                <div 
                  className="accordion-header"
                  onClick={() => toggleAccordion(message.id, index)}
                >
                  <span className="accordion-title">{accordion.title}</span>
                  <span className={`accordion-icon ${accordion.isOpen ? 'open' : ''}`}>
                    {accordion.isOpen ? '−' : '+'}
                  </span>
                </div>
                {accordion.isOpen && (
                  <div className="accordion-content">
                    <div 
                      dangerouslySetInnerHTML={{ 
                        __html: formatMessageText(accordion.content) 
                      }}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
        
        {message.elements.buttons && message.elements.buttons.length > 0 && (
          <div className="message-buttons">
            {message.elements.buttons.map((button, index) => (
              <button
                key={`btn-${index}`}
                className="interactive-button"
                onClick={() => handleButtonClick(button.action, button.text)}
              >
                {button.text}
              </button>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Cybersecurity Knowledge Assistant</h1>
      </div>
      
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h2>Welcome to the Cybersecurity Knowledge Assistant</h2>
            <p>Ask me anything about cybersecurity threats, defenses, or best practices.</p>
            
            <div className="sample-questions-container">
              <h3>Try asking:</h3>
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
          messages.map((message) => (
            <div key={message.id} className={`message ${message.sender}`}>
              <div className="message-content">
                {message.sender === 'bot' ? (
                  <>
                    <div 
                      className="formatted-message"
                      dangerouslySetInnerHTML={{ __html: formatMessageText(message.text) }}
                    />
                    {renderMessageElements(message)}
                  </>
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
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
          </svg>
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;