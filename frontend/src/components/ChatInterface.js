import React, { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addChatMessage, updateMultipleFields, setCurrentInteractionId } from '../store/interactionSlice';
import { chatAPI } from '../services/api';
import './ChatInterface.css';

const ChatInterface = () => {
  const dispatch = useDispatch();
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);
  const chatMessages = useSelector((state) => state.interaction.chatMessages);

  const scrollToBottom = () => {
    // Use both methods for better compatibility
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
    // Also scroll the container directly
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    // Small delay to ensure DOM is updated
    setTimeout(() => {
      scrollToBottom();
    }, 100);
  }, [chatMessages, isTyping]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: input,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    dispatch(addChatMessage(userMessage));
    setInput('');
    setIsTyping(true);

    try {
      // Send message with current form data (for editing)
      const response = await chatAPI.sendMessage(input, formData);

      const assistantMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: response.response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      dispatch(addChatMessage(assistantMessage));

      // Handle actions from the AI
      if (response.action === 'create_interaction' && response.data) {
        // Update form with extracted data
        dispatch(updateMultipleFields(response.data));

        // Store the interaction ID if created
        if (response.data.interaction_id) {
          dispatch(setCurrentInteractionId(response.data.interaction_id));
        }
      } else if (response.action === 'update_interaction' && response.data) {
        // Update specific fields
        dispatch(updateMultipleFields(response.data));
      }

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      dispatch(addChatMessage(errorMessage));
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
  };

  const suggestions = [
    "Today I met with Dr. Smith and discussed Product X efficiency",
    "Log interaction with Dr. Johnson, positive sentiment",
    "Change the name to Dr. John",
    "Schedule a follow-up in 2 weeks",
  ];

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>🤖 AI Assistant</h2>
        <p>Describe your interaction and I'll fill the form for you</p>
      </div>

      <div className="chat-messages" ref={messagesContainerRef}>
        {chatMessages.length === 0 ? (
          <div className="empty-chat">
            <div className="empty-chat-icon">💬</div>
            <h3>Start a conversation</h3>
            <p>
              Tell me about your HCP interaction and I'll automatically fill out the form on the left.
              Try something like "Today I met with Dr. Smith..."
            </p>
          </div>
        ) : (
          <>
            {chatMessages.map((message) => (
              <div key={message.id} className={`chat-message ${message.sender}`}>
                <div className="chat-message-avatar">
                  {message.sender === 'user' ? '👤' : '🤖'}
                </div>
                <div className="chat-message-content">
                  <div className="chat-message-text">{message.text}</div>
                  <div className="chat-message-time">{message.timestamp}</div>
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="chat-message assistant">
                <div className="chat-message-avatar">🤖</div>
                <div className="chat-message-content">
                  <div className="typing-indicator">
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {chatMessages.length === 0 && (
        <div className="chat-suggestions">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              className="suggestion-chip"
              onClick={() => handleSuggestionClick(suggestion)}
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here... (e.g., 'Today I met with Dr. Smith')"
            rows="1"
          />
          <button
            className="chat-send-button"
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;

