import React, { useState } from 'react';
import './App.css';

function App() {
  // --- State Management ---
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [personality, setPersonality] = useState('Default'); // New state for personality
  const [settingsOpen, setSettingsOpen] = useState(false); // New state for settings panel

  // --- Functions ---
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);

    try {
      // The API call now sends the full history and selected personality
      const response = await fetch('http://127.0.0.1:8000/api/chat/local', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          prompt: input,
          personality: personality,
          history: newMessages.slice(0, -1) // Send all messages except the current one
        }),
      });

      const data = await response.json();
      const aiMessage = { sender: 'ai', text: data.response };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = { sender: 'ai', text: `Error: Could not connect to backend. ${error}` };
      setMessages(prev => [...prev, errorMessage]);
    }
    
    setInput('');
  };

  const handleClearHistory = () => {
    setMessages([]);
  };

  // --- Rendered UI ---
  return (
    <div className="App">
      <header className="App-header">
        <h1>😇 Angel</h1>
        <p>Your private AI agent</p>
      </header>

      {/* Settings Button */}
      <div className="settings-toggle">
        <button onClick={() => setSettingsOpen(!settingsOpen)}>
          {settingsOpen ? 'Close Settings' : '⚙️ Angel Settings'}
        </button>
      </div>

      {/* Settings Panel (conditionally rendered) */}
      {settingsOpen && (
        <div className="settings-panel">
          <h3>Personality</h3>
          <select value={personality} onChange={(e) => setPersonality(e.target.value)}>
            <option value="Default">Default (Helpful)</option>
            <option value="Creative">Creative</option>
            <option value="Technical">Technical</option>
            <option value="Succinct">Succinct</option>
          </select>
        </div>
      )}

      <div className="main-content">
        <div className="chat-container">
          <div className="chat-header">
            <h2>Chat</h2>
            <button onClick={handleClearHistory} title="Clear Conversation History">🗑️</button>
          </div>
          <div className="chat-window">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                <p>{msg.text}</p>
              </div>
            ))}
          </div>
          <form onSubmit={handleSendMessage} className="chat-form">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask Angel anything..."
            />
            <button type="submit">Send</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;