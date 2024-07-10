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

  useEffect(() => {
    // Fetch group messages when component mounts
    socket.emit('GetGroupMessages', { username, groupid: groupName });

    // Listen for messages from the server
    socket.on('messages', (mesg) => {
      setMessages(mesg);
    });

    // Cleanup on unmount
    return () => {
      socket.off('messages');
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

      // Update local messages state immediately
      setMessages((prevMessages) => [
        ...prevMessages,
        { user: username, content: newMessage },
      ]);

      setNewMessage('');
    }
  };

  const handleSendSummary = () => {
    const selectedMessages = messages.filter((msg, index) => checkedMessages[index]);
    socket.emit('messagesForSummary', { messages: selectedMessages });
  };

  return (
    <div>
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
      <form onSubmit={handleSendMessage}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message"
        />
        <button type="submit">Send</button>
      </form>
      <button onClick={handleSendSummary}>Send Selected Messages for Summary</button>
    </div>
  );
}

export default GroupPage;
