import React from 'react';
import InteractionForm from './components/InteractionForm';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>🏥 AI-CRM HCP Module</h1>
        <div className="app-subtitle">Intelligent Healthcare Professional Interaction Management</div>
      </header>

      <main className="app-content">
        <InteractionForm />
        <ChatInterface />
      </main>

      <footer className="app-footer">
        Powered by LangGraph & Groq LLM (llama-3.3-70b-versatile)
      </footer>
    </div>
  );
}

export default App;

