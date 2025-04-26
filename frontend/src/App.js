import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userInfo, setUserInfo] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));  // ✅ 追蹤 token 狀態

  const handleRegister = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/register', {
        email,
        password
      });
      alert('Registration successful!');
    } catch (error) {
      if (error.response && error.response.data.detail === "Email already registered") {
        alert("This email has already been registered.");
      } else {
        alert('Registration failed');
        console.error(error);
      }
    }
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/login', {
        email,
        password
      });
      const token = response.data.access_token;
      localStorage.setItem('token', token);        // ✅ write to localStorage
      setToken(token);                             // ✅ update token state
      alert('Login successful!');
    } catch (error) {
      alert('Login failed');
      console.error(error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');              // ✅ token removed
    setToken(null);
    setUserInfo(null);
    alert('Logged out!');
  };

  const fetchUserInfo = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/me', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setUserInfo(res.data);
    } catch (error) {
      alert('Token invalid or expired');
      console.error(error);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>FastAPI + React Auth Demo</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      /><br />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      /><br />
      <button onClick={handleRegister}>Register</button>
      <button onClick={handleLogin} style={{ marginLeft: '1rem' }}>Login</button>
      <button onClick={fetchUserInfo} style={{ marginLeft: '1rem' }}>
        Get My Info
      </button>
      <button onClick={handleLogout} style={{ marginLeft: '1rem' }}>
        Logout
      </button>

      {token && (
        <>
          <h4>🔐 JWT Token:</h4>
          <code style={{ wordWrap: "break-word", display: "block" }}>{token}</code>
        </>
      )}

      {userInfo && (
        <>
          <h4>👤 User Info:</h4>
          <pre>{JSON.stringify(userInfo, null, 2)}</pre>
        </>
      )}
    </div>
  );
}

export default App;
