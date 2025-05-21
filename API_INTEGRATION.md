# ISWL Work Log API Integration Guide

## Test Endpoints (React.js Implementation)

Here's a sequence of API calls using React.js patterns and hooks:

1. **API Service Setup**
```javascript
// src/services/api.js
const API_BASE_URL = 'http://localhost:8000';

export const api = {
  // Auth endpoints
  register: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    return response.json();
  },

  login: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    return response.json();
  },

  getCurrentUser: async (token) => {
    const response = await fetch(`${API_BASE_URL}/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Work log endpoints
  createWorkLog: async (token, logData) => {
    const response = await fetch(`${API_BASE_URL}/logs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(logData),
    });
    return response.json();
  },

  getWorkLogs: async (token) => {
    const response = await fetch(`${API_BASE_URL}/logs`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  updateWorkLog: async (token, logId, updateData) => {
    const response = await fetch(`${API_BASE_URL}/logs/${logId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(updateData),
    });
    return response.json();
  },
};
```

2. **Authentication Context**
```javascript
// src/contexts/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          const userData = await api.getCurrentUser(token);
          setUser(userData);
        } catch (error) {
          console.error('Failed to load user:', error);
          setToken(null);
          localStorage.removeItem('token');
        }
      }
      setLoading(false);
    };

    loadUser();
  }, [token]);

  const login = async (email, password) => {
    const { access_token } = await api.login({ email, password });
    setToken(access_token);
    localStorage.setItem('token', access_token);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

3. **Example Component Usage**
```javascript
// src/components/WorkLogForm.js
import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';

export const WorkLogForm = () => {
  const { token } = useAuth();
  const [formData, setFormData] = useState({
    week_number: 1,
    day: 'Monday',
    date: new Date().toISOString().split('T')[0],
    working_hours: 8.5,
    task_description: '',
    status: 'pending',
    reviewer_id: null
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newLog = await api.createWorkLog(token, formData);
      console.log('Created work log:', newLog);
      // Handle success (e.g., show notification, reset form)
    } catch (error) {
      console.error('Failed to create work log:', error);
      // Handle error (e.g., show error message)
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  );
};
```

4. **Work Log List Component**
```javascript
// src/components/WorkLogList.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';

export const WorkLogList = () => {
  const { token } = useAuth();
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const data = await api.getWorkLogs(token);
        setLogs(data);
      } catch (error) {
        setError('Failed to fetch work logs');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
  }, [token]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {logs.map(log => (
        <div key={log.id}>
          <h3>Week {log.week_number} - {log.day}</h3>
          <p>Hours: {log.working_hours}</p>
          <p>Task: {log.task_description}</p>
          <p>Status: {log.status}</p>
        </div>
      ))}
    </div>
  );
};
```

5. **App Setup**
```javascript
// src/App.js
import React from 'react';
import { AuthProvider } from './contexts/AuthContext';
import { WorkLogForm } from './components/WorkLogForm';
import { WorkLogList } from './components/WorkLogList';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <h1>Work Log System</h1>
        <WorkLogForm />
        <WorkLogList />
      </div>
    </AuthProvider>
  );
}

export default App;
```

This React.js implementation provides:
- Centralized API service
- Authentication context for managing user state
- Reusable components for work log management
- Proper error handling and loading states
- Token management with localStorage
- Type-safe API calls

The code follows React best practices:
- Uses hooks for state management
- Implements context for global state
- Separates concerns (API, components, context)
- Handles loading and error states
- Provides reusable components

Would you like me to add any additional React.js specific features or explain any part in more detail?

## Landing Page

### Health Check
- **Endpoint**: `/`
- **Method**: GET
- **Description**: Simple health check endpoint to verify if the backend is running
- **Success Response** (200 OK):
  ```json
  {
    "message": "FastAPI backend is working ✅"
  }
  ```

## Authentication Endpoints

### 1. Login
- **Endpoint**: `/login`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
    "token_type": "bearer"
  }
  ```
- **Error Response** (401 Unauthorized):
  ```json
  {
    "detail": "Incorrect email or password"
  }
  ```

### 2. Register
- **Endpoint**: `/register`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "email": "newuser@example.com",
    "password": "newpassword"
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "id": 1,
    "email": "newuser@example.com"
  }
  ```
- **Error Response** (400 Bad Request):
  ```json
  {
    "detail": "Email already registered"
  }
  ```

### 3. Get Current User
- **Endpoint**: `/me`
- **Method**: GET
- **Headers Required**: 
  ```
  Authorization: Bearer <your_jwt_token>
  ```
- **Success Response** (200 OK):
  ```json
  {
    "id": 1,
    "email": "user@example.com"
  }
  ```
- **Error Response** (401 Unauthorized):
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```

## Work Log Endpoints

### 1. Create Work Log
- **Endpoint**: `/logs`
- **Method**: POST
- **Headers Required**: 
  ```
  Authorization: Bearer <your_jwt_token>
  ```
- **Request Body**:
  ```json
  {
    "week_number": 1,
    "day": "Monday",
    "date": "2024-03-18",
    "working_hours": 8.5,
    "task_description": "Completed feature X",
    "status": "pending",
    "reviewer_id": null
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "id": 1,
    "user_id": 1,
    "week_number": 1,
    "day": "Monday",
    "date": "2024-03-18",
    "working_hours": 8.5,
    "task_description": "Completed feature X",
    "status": "pending",
    "reviewer_id": null
  }
  ```

### 2. Get My Work Logs
- **Endpoint**: `/logs`
- **Method**: GET
- **Headers Required**: 
  ```
  Authorization: Bearer <your_jwt_token>
  ```
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": 1,
      "user_id": 1,
      "week_number": 1,
      "day": "Monday",
      "date": "2024-03-18",
      "working_hours": 8.5,
      "task_description": "Completed feature X",
      "status": "pending",
      "reviewer_id": null
    },
    // ... more logs
  ]
  ```

## Data Models

### User Model
```typescript
interface User {
  id: number;
  email: string;
  role: string;  // Note: Role field exists but role-based access control is not yet implemented
}
```

### Work Log Model
```typescript
interface WorkLog {
  id: number;
  user_id: number;
  week_number: number;
  day: string;
  date: string;  // ISO date format
  working_hours: number;
  task_description: string;
  status: 'pending' | 'approved' | 'rejected';
  reviewer_id: number | null;
}
```

## Important Notes

1. **JWT Token**:
   - The JWT token is returned in the `access_token` field of the login response
   - Token type is always "bearer"
   - Include the token in all authenticated requests in the Authorization header

2. **CORS Configuration**:
   - Backend is configured to accept requests from `http://localhost:3000`
   - All methods and headers are allowed
   - Credentials are allowed

3. **Port Information**:
   - The backend runs on the default FastAPI port (8000)
   - Access the API at `http://localhost:8000`

4. **Request Headers**:
   - For authenticated endpoints, always include:
     ```
     Authorization: Bearer <your_jwt_token>
     ```
   - Content-Type should be `application/json` for POST requests

5. **Error Handling**:
   - All endpoints return appropriate HTTP status codes
   - Error messages are returned in the `detail` field of the response
   - Common status codes:
     - 200: Success
     - 400: Bad Request
     - 401: Unauthorized
     - 404: Not Found
     - 500: Internal Server Error

6. **Security Notes**:
   - Always use HTTPS in production
   - Store JWT tokens securely (e.g., in memory or secure cookies)
   - Never store tokens in localStorage
   - Implement token refresh mechanism if needed

## Example Usage

### Login Request
```javascript
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  const data = await response.json();
  return data.access_token;
};
```

### Create Work Log
```javascript
const createWorkLog = async (token, logData) => {
  const response = await fetch('http://localhost:8000/logs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(logData),
  });
  
  if (!response.ok) {
    throw new Error('Failed to create work log');
  }
  
  return response.json();
};
```

### Get My Work Logs
```javascript
const getMyWorkLogs = async (token) => {
  const response = await fetch('http://localhost:8000/logs', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to get work logs');
  }
  
  return response.json();
};
```