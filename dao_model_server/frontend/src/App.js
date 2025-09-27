import React, { useEffect, useState } from 'react';
import ChatInterface from './components/ChatInterface';
import ModelInfo from './components/ModelInfo';
import './styles/App.css';

function App() {
  const [particles, setParticles] = useState([]);

  // Create animated particles
  useEffect(() => {
    const particleCount = 50;
    const newParticles = [];
    
    for (let i = 0; i < particleCount; i++) {
      newParticles.push({
        id: i,
        left: Math.random() * 100,
        top: Math.random() * 100,
        delay: Math.random() * 6,
        duration: Math.random() * 3 + 3
      });
    }
    
    setParticles(newParticles);
  }, []);

  return (
    <div className="App">
      <div className="particles">
        {particles.map(particle => (
          <div
            key={particle.id}
            className="particle"
            style={{
              left: `${particle.left}%`,
              top: `${particle.top}%`,
              animationDelay: `${particle.delay}s`,
              animationDuration: `${particle.duration}s`
            }}
          />
        ))}
      </div>
      
      <div className="container">
        <div className="header">
          <h1 className="title">Ires</h1>
          <p className="subtitle">Your LifeStyle Broker</p>
          <div className="model-badge">
            <div className="status-dot"></div>
            Meet Dao • Pattaya Lifestyle Expert • Online Now
          </div>
        </div>

        <div className="demo-container">
          <ChatInterface />
        </div>

        <ModelInfo />
      </div>
    </div>
  );
}

export default App;
