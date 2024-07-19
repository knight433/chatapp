import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { useNavigate } from 'react-router-dom';
import './ChatPage.css'; // Import the CSS file

const socket = io('http://localhost:5000');

function ChatPage() {
  const [username, setUsername] = useState('');
  const [groups, setGroups] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Retrieve the username from local storage or state management
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);

      // Emit the GetGroups event to fetch user's groups
      socket.emit('GetGroups', { username: storedUsername });

      // Listen for the GroupsList event to receive the list of groups
      socket.on('GroupsList', (listOfGroups) => {
        setGroups(listOfGroups);
      });
    } else {
      navigate('/');
    }

    return () => {
      socket.off('GroupsList');
    };
  }, [navigate]);

  const handleGroupClick = (group) => {
    navigate(`/group/${group}`, { state: { username } });
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>Chat Application</h1>
        <div className="logged-in">
          Logged in as: <span>{username}</span>
        </div>
        <div className="groups-list">
          <h2>Your Groups</h2>
          <ul>
            {groups.map((group, index) => (
              <li key={index}>
                <button onClick={() => handleGroupClick(group)}>{group}</button>
              </li>
            ))}
          </ul>
        </div>
      </header>
    </div>
  );
}

export default ChatPage;
