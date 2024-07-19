import React, { useState, useEffect } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import io from 'socket.io-client';
import './GroupPage.css';  // Import the CSS file

const socket = io('http://localhost:5000');

function GroupPage() {
  const { groupName } = useParams();
  const location = useLocation();
  const { username } = location.state;
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [checkedMessages, setCheckedMessages] = useState({});
  const [summarizedText, setSummarizedText] = useState('');
  const [emotion, setEmotion] = useState('');

  useEffect(() => {
    // Fetch group messages when component mounts
    socket.emit('GetGroupMessages', { username, groupid: groupName });

    // Listen for messages from the server
    socket.on('messages', (mesg) => {
      setMessages(mesg);
    });

    // Listen for new messages from the server
    socket.on('new_message', (msg) => {
      if (msg.group_id === groupName) {
        setMessages((prevMessages) => [...prevMessages, msg]);
      }
    });

    // Listen for summarized text from the server
    socket.on('summarized_text', (text) => {
      console.log(text);
      setSummarizedText(text);
    });

    // Listen for emotion classification result
    socket.on('emotion', (emo) => {
      setEmotion(emo);
    });

    // Cleanup on unmount
    return () => {
      socket.off('messages');
      socket.off('new_message');
      socket.off('summarized_text');
      socket.off('emotion');
    };
  }, [groupName, username]);

  const handleCheckboxChange = (index) => {
    setCheckedMessages((prevCheckedMessages) => ({
      ...prevCheckedMessages,
      [index]: !prevCheckedMessages[index],
    }));
  };

  const handleSendMessage = (event) => {
    event.preventDefault();
    if (newMessage.trim()) {
      const messageData = {
        username,
        message: newMessage,
        group_id: groupName,
      };

      // Send message to the backend
      socket.emit('SendMessage', messageData);

      setNewMessage('');
    }
  };

  const handleSendSummary = () => {
    const selectedMessages = messages.filter((msg, index) => checkedMessages[index]);
    socket.emit('messagesForSummary', { messages: selectedMessages });
  };

  const handleEmotionClassification = () => {
    const selectedMessages = messages.filter((msg, index) => checkedMessages[index]);
    socket.emit('emotionClassifier', { messages: selectedMessages });
  };

  return (
    <div className="group-container">
      <h1>Group: {groupName}</h1>
      <h2>Logged in as: {username}</h2>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className="message">
            <input
              type="checkbox"
              checked={checkedMessages[index] || false}
              onChange={() => handleCheckboxChange(index)}
            />
            <p>
              <strong>{msg.user}:</strong> {msg.content}
            </p>
          </div>
        ))}
      </div>
      <form onSubmit={handleSendMessage} className="message-form">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message"
        />
        <button type="submit">Send</button>
      </form>
      <button onClick={handleSendSummary}>Send Selected Messages for Summary</button>
      {summarizedText && (
        <div className="summarized-text">
          <h3>Summary:</h3>
          <p>{summarizedText}</p>
        </div>
      )}
      <button onClick={handleEmotionClassification}>Classify Emotion of Selected Messages</button>
      {emotion && (
        <div className="emotion-result">
          <h3>Emotion Classification Result:</h3>
          <p>{emotion}</p>
        </div>
      )}
    </div>
  );
}

export default GroupPage;
