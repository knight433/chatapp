import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import io from 'socket.io-client';
import './SignUpPage.css'; // Import the CSS file

const socket = io('http://localhost:5000');

function SignUpPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignUp = () => {
    if (username.trim() && password.trim()) {
      // Emit a sign-up event to the server with username and password
      socket.emit('signup', { username, password });

      // Listen for sign-up response from the server
      socket.on('signup_response', (data) => {
        if (data.status === 'success') {
          navigate('/');
        } else {
          // Display the error message
          setError(data.message);
        }
      });
    } else {
      setError('Username and password are required');
    }
  };

  return (
    <div className="signup-container">
      <header className="signup-header">
        <h1>Sign Up</h1>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter your username"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
        />
        <button onClick={handleSignUp}>Sign Up</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </header>
    </div>
  );
}

export default SignUpPage;
