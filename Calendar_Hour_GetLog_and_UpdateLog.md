# API Usage Guide - Work Log System

## 🔗 API Endpoints

### 1. Get All Logs

**Endpoint:** `GET /logs/`

**Description:** Retrieve all work logs for the current user

**Request:**
```javascript
const fetchLogs = async () => {
  try {
    const response = await fetch('/logs/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const logs = await response.json();
      console.log('All logs:', logs);
      return logs; // Each log has an id field
    } else {
      console.error('Failed to fetch logs:', response.status);
    }
  } catch (error) {
    console.error('Error fetching logs:', error);
  }
};
```

**Request Format:**
```json
{}
```

**Response Format:**
```json
[
  {
    "id": 123, // unique logId
    "user_id": 1,
    "date": "2025-09-16",
    "start_time": "08:00:00",
    "end_time": "14:00:00",
    "task_description": "Work description",
    "status": "pending",
    "reviewer_id": null
  }
]
```

### 2. Update Log

**Endpoint:** `PUT /logs/{log_id}`

**Description:** Update a specific work log

**Request:**
```javascript
const updateLog = async (logId, updateData) => {
  try {
    const response = await fetch(`/logs/${logId}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updateData)
    });
    
    if (response.ok) {
      const updatedLog = await response.json();
      console.log('Log updated successfully:', updatedLog);
      return updatedLog;
    } else {
      const errorData = await response.json();
      console.error('Update failed:', errorData);
    }
  } catch (error) {
    console.error('Error updating log:', error);
  }
};
```

**Request Body Format:**
```json
{
  "start_time": "09:00:00",
  "end_time": "15:00:00",
  "task_description": "Updated work description" // optional
}
```

**Response Body Format:**
```json
{
  "id": 123, //${logId}
  "user_id": 1,
  "date": "2025-09-16",
  "start_time": "09:00:00",
  "end_time": "15:00:00",
  "task_description": "Updated work description", // optional
  "status": "pending",
  "reviewer_id": null
}
```

### 3. Delete Log

**Endpoint:** `DELETE /logs/{log_id}`

**Description:** Delete a specific work log

**Request:**
```javascript
const deleteLog = async (logId) => {
  try {
    const response = await fetch(`/logs/${logId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('Log deleted successfully:', result);
      return result;
    } else {
      const errorData = await response.json();
      console.error('Delete failed:', errorData);
    }
  } catch (error) {
    console.error('Error deleting log:', error);
  }
};
```

**Request Format:**
```json
{}
```

**Response Format:**
```json
{
  "message": "Log deleted successfully",
  "log_id": 123
}
```

## 🔄 Complete Usage Flow

### Step 1: Get Log List
```javascript
const logs = await fetchLogs();
// logs array contains all logs, each with a unique id
```

### Step 2: Select Log to Update
```javascript
const selectedLog = logs[0]; // Select the first log
const logId = selectedLog.id; // Get the log ID
```

### Step 3: Update Log
Example:
```javascript
const updateData = {
  task_description: "Updated description",
  start_time: "10:00:00",
  end_time: "16:00:00"
};

const updatedLog = await updateLog(logId, updateData);
```

### Step 4: Delete Log
Example:
```javascript
const deletedResult = await deleteLog(logId);
console.log(deletedResult.message); // "Log deleted successfully"
```

## 📝 Field Descriptions

### Log Fields
- `id`: Unique log identifier (integer)
- `user_id`: User ID (integer)
- `date`: Date (format: YYYY-MM-DD)
- `start_time`: Start time (format: HH:MM:SS)
- `end_time`: End time (format: HH:MM:SS)
- `task_description`: Task description (string)
- `status`: Status (pending/approved/rejected)
- `reviewer_id`: Reviewer ID (optional)

### Update Fields (all optional)
- `date`: Date
- `start_time`: Start time
- `end_time`: End time
- `task_description`: Task description
- `status`: Status (admin only)
- `reviewer_id`: Reviewer ID (admin only)

## ⚠️ Important Notes

1. **Authentication Required**: All requests need a valid Authorization token
2. **Permission Restrictions**:
   - Regular users can only update/delete their own logs
   - Regular users cannot modify status and reviewer_id
   - Admins can update/delete any logs
3. **Data Format**:
   - Date format: YYYY-MM-DD
   - Time format: HH:MM:SS
   - Task description is optional

## 🚨 Error Handling

### Common Error Codes
- `400`: Bad Request (invalid format)
- `401`: Unauthorized (login required)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found (log doesn't exist)
- `422`: Validation Error (data validation failed)

### Error Response Format
```json
{
  "detail": [
    {
      "type": "validation_error",
      "loc": ["body", "field_name"],
      "msg": "Error message",
      "input": "invalid_value"
    }
  ]
}
```