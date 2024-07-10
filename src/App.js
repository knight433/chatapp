import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './LoginPage';
import ChatPage from './ChatPage';
import GroupPage from './GroupPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/group/:groupName" element={<GroupPage />} />
      </Routes>
    </Router>
  );
}

export default App;
