import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import io from 'socket.io-client';
import './login.css'; // Importing the CSS file

const socket = io('http://localhost:5000');

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Listen for login response from the server
    socket.on('login_response', (data) => {
      if (data.status === 'success') {
        // Store the username in local storage and navigate to the chat page
        localStorage.setItem('username', data.username);
        navigate('/chat');
      } else {
        // Display the error message
        setError(data.message);
      }
    });

    // Cleanup the listener when component unmounts
    return () => {
      socket.off('login_response');
    };
  }, [navigate]);

  const handleLogin = () => {
    if (username.trim() && password.trim()) {
      // Emit a login event to the server with username and password
      socket.emit('login', { username, password });
    } else {
      setError('Username and password are required');
    }
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <h1>Login to Chat</h1>
        <div className="login-form">
          <input 
            type="text" 
            className="form-control" 
            value={username} 
            onChange={e => setUsername(e.target.value)} 
            placeholder="Enter your username"
          />
          <input 
            type="password" 
            className="form-control" 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
            placeholder="Enter your password"
          />
          <button className="btn-primary" onClick={handleLogin}>Login</button>
          {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
