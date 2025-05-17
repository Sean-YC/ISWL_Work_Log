# ISWL Work Log API Integration Guide

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