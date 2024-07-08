// ChatPage.js
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { useNavigate } from 'react-router-dom';

const socket = io('http://localhost:5000');

function ChatPage() {
  const [username, setUsername] = useState('');
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const [groups, setGroups] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Retrieve the username from local storage or state management
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);
    } else {
      navigate('/');
    }

    // Fetch initial messages
    const fetchMessages = async () => {
      try {
        const response = await fetch('http://localhost:5000/get-messages');
        const data = await response.json();
        setChat(data.messages);
      } catch (error) {
        console.error("Error fetching messages", error);
      }
    };

    // Fetch user's groups
    const fetchGroups = async () => {
      try {
        const response = await fetch('http://localhost:5000/get-user-groups', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username: storedUsername })
        });
        const data = await response.json();
        setGroups(data.groups);
      } catch (error) {
        console.error("Error fetching user's groups", error);
      }
    };

    fetchMessages();
    fetchGroups();

    // Listen for new messages
    socket.on('message', msg => {
      setChat(prevChat => [...prevChat, msg]);
    });

    return () => {
      socket.off('message');
    };
  }, [navigate]);

  const handleSendMessage = () => {
    if (message.trim()) {
      socket.send({ username, message });
      setMessage('');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chat Application</h1>
        <div className='loggedIn'>
          Logged in as: {username}
        </div>
        <div className="groups-list">
          <h2>Your Groups</h2>
          <ul>
            {groups.map((group, index) => (
              <li key={index}>{group}</li>
            ))}
          </ul>
        </div>
        <div className="chat-window">
          {chat.map((msg, index) => (
            <p key={index}>{msg}</p>
          ))}
        </div>
        <input 
          type="text" 
          value={message} 
          onChange={e => setMessage(e.target.value)} 
          placeholder="Type your message"
        />
        <button onClick={handleSendMessage}>Send Message</button>
      </header>
    </div>
  );
}

export default ChatPage;
