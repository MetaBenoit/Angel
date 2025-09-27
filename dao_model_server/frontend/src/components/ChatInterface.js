import React, { useState, useEffect, useRef } from 'react';
import { chatAPI } from '../services/api';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      content: "Sawasdee ka! I'm Dao from Ires - your LifeStyle Broker in Pattaya! I help people find not just properties, but the perfect lifestyle here. Originally from Bangkok myself, so I understand both city vibes. What brings you to explore Pattaya living?",
      sender: 'assistant',
      timestamp: new Date()
    }
  ]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState('');
  const [settings, setSettings] = useState({
    temperature: 0.7,
    maxTokens: 1024
  });
  const [showSettings, setShowSettings] = useState(false);
  const messagesEndRef = useRef(null);

  const samplePrompts = [
    "Hi Dao! I'm looking for a condo in Pattaya with sea view",
    "What lifestyle differences are there between Jomtien and Central Pattaya?",
    "I'm considering moving from Bangkok - what should I know?",
    "Can foreigners really own property in Thailand legally?",
    "What's your honest take on Pattaya as a lifestyle investment?"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      content: message,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setMessage('');
    setLoading(true);
    setError(null);

    try {
      const response = await chatAPI.sendMessage(
        message,
        conversationId,
        settings.temperature,
        settings.maxTokens
      );

      const assistantMessage = {
        id: Date.now() + 1,
        content: response.response,
        sender: 'assistant',
        timestamp: new Date(response.timestamp),
        processingTime: response.processing_time,
        modelInfo: response.model_info
      };

      setMessages(prev => [...prev, assistantMessage]);
      setConversationId(response.conversation_id);

    } catch (error) {
      console.error('Error sending message:', error);
      setError(error.message);
      
      const errorMessage = {
        id: Date.now() + 1,
        content: `Sorry, I encountered an error: ${error.message}. Please try again or contact our Ires office directly.`,
        sender: 'assistant',
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handlePromptClick = (prompt) => {
    setMessage(prompt);
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        content: "Sawasdee ka! I'm Dao from Ires - your LifeStyle Broker. How can I help you explore the perfect Pattaya lifestyle today?",
        sender: 'assistant',
        timestamp: new Date()
      }
    ]);
    setConversationId(null);
    setError(null);
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="chat-interface">
      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)} className="error-dismiss">×</button>
        </div>
      )}
      
      <div className="messages-container">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.sender} ${msg.isError ? 'error' : ''}`}>
            <div className="message-header">
              <span className="sender">{msg.sender === 'user' ? 'You' : 'Dao'}</span>
              <span className="timestamp">{formatTime(msg.timestamp)}</span>
              {msg.processingTime && (
                <span className="processing-time">({msg.processingTime.toFixed(2)}s)</span>
              )}
            </div>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        
        {loading && (
          <div className="loading active">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            Dao is thinking...
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="input-section">
        <div className="input-container">
          <div className="input-wrapper">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask Dao about Pattaya lifestyle and properties... (Press Ctrl+Enter to send)"
              className="message-input"
              rows="2"
              disabled={loading}
            />
          </div>
          <div className="button-group">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="settings-button"
              title="Chat Settings"
            >
              ⚙️
            </button>
            <button
              onClick={handleSendMessage}
              disabled={!message.trim() || loading}
              className="send-button"
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  Sending...
                </>
              ) : (
                <>
                  Send
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22,2 15,22 11,13 2,9"></polygon>
                  </svg>
                </>
              )}
            </button>
          </div>
        </div>

        {showSettings && (
          <div className="settings-panel">
            <div className="setting-group">
              <label htmlFor="temperature">Response Style: {settings.temperature}</label>
              <input
                id="temperature"
                type="range"
                min="0.1"
                max="2.0"
                step="0.1"
                value={settings.temperature}
                onChange={(e) => setSettings(prev => ({ ...prev, temperature: parseFloat(e.target.value) }))}
              />
            </div>
            <div className="setting-group">
              <label htmlFor="maxTokens">Response Length: {settings.maxTokens}</label>
              <input
                id="maxTokens"
                type="range"
                min="50"
                max="2048"
                step="50"
                value={settings.maxTokens}
                onChange={(e) => setSettings(prev => ({ ...prev, maxTokens: parseInt(e.target.value) }))}
              />
            </div>
          </div>
        )}

        <div className="sample-prompts">
          <h4>Ask Dao about:</h4>
          <div className="prompt-chips">
            {samplePrompts.map((prompt, index) => (
              <button
                key={index}
                className="prompt-chip"
                onClick={() => handlePromptClick(prompt)}
                disabled={loading}
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>

        <div className="action-buttons">
          <button onClick={clearChat} className="clear-button" disabled={loading}>
            Start Fresh
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
