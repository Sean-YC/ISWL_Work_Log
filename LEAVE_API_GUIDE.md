# Leave Request API Guide

## 📋 Overview

This guide documents all API endpoints for the Leave Request system. The system allows users to apply for leave, view their leave balance, and manage leave requests.

## 🔗 API Endpoints

### 1. Get Leave Balance

**Endpoint:** `GET /leaves/balance`

**Description:** Get current user's available leave balance (Annual Leave, Sick Leave, Personal Leave)

**Request:**
```javascript
const getLeaveBalance = async () => {
  try {
    const response = await fetch('/leaves/balance', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const balance = await response.json();
      console.log('Leave balance:', balance);
      return balance;
    }
  } catch (error) {
    console.error('Error fetching leave balance:', error);
  }
};
```

**Response Format:**
```json
{
  "user_id": 1,
  "annual_leave": 10,
  "sick_leave": 5,
  "personal_leave": 5
}
```

---

### 2. Create Leave Request

**Endpoint:** `POST /leaves/`

**Description:** Submit a new leave request

**Request:**
```javascript
const createLeaveRequest = async (leaveData) => {
  try {
    const response = await fetch('/leaves/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(leaveData)
    });
    
    if (response.ok) {
      const leaveRequest = await response.json();
      console.log('Leave request created:', leaveRequest);
      return leaveRequest;
    } else {
      const errorData = await response.json();
      console.error('Failed to create leave request:', errorData);
    }
  } catch (error) {
    console.error('Error creating leave request:', error);
  }
};
```

**Request Body Format:**
```json
{
  "leave_type": "annual_leave",  // "annual_leave", "sick_leave", or "personal_leave"
  "start_date": "2024-12-24",
  "end_date": "2024-12-26",
  "reason": "Family Emergency",
  "contact": "123-456-7890"  // optional
}
```

**Response Format:**
```json
{
  "id": 123,
  "user_id": 1,
  "leave_type": "annual_leave",
  "start_date": "2024-12-24",
  "end_date": "2024-12-26",
  "reason": "Family Emergency",
  "contact": "123-456-7890",
  "status": "pending",
  "reviewer_id": null,
  "created_at": "2024-12-20"
}
```

---

### 3. Get All Leave Requests

**Endpoint:** `GET /leaves/`

**Description:** Get all leave requests for the current user (Recent Requests)

**Request:**
```javascript
const getLeaveRequests = async () => {
  try {
    const response = await fetch('/leaves/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const leaves = await response.json();
      console.log('Leave requests:', leaves);
      return leaves;
    }
  } catch (error) {
    console.error('Error fetching leave requests:', error);
  }
};
```

**Response Format:**
```json
[
  {
    "id": 123,
    "user_id": 1,
    "leave_type": "annual_leave",
    "start_date": "2024-12-24",
    "end_date": "2024-12-26",
    "reason": "Family Emergency",
    "contact": "123-456-7890",
    "status": "approved",
    "reviewer_id": 2,
    "created_at": "2024-12-20"
  },
  {
    "id": 124,
    "user_id": 1,
    "leave_type": "sick_leave",
    "start_date": "2024-11-15",
    "end_date": "2024-11-15",
    "reason": "Fever and Cold",
    "contact": null,
    "status": "approved",
    "reviewer_id": 2,
    "created_at": "2024-11-10"
  },
  {
    "id": 125,
    "user_id": 1,
    "leave_type": "personal_leave",
    "start_date": "2024-10-05",
    "end_date": "2024-10-05",
    "reason": "vacation",
    "contact": null,
    "status": "rejected",
    "reviewer_id": 2,
    "created_at": "2024-10-01"
  }
]
```

---

### 4. Update Leave Request

**Endpoint:** `PUT /leaves/{leave_id}`

**Description:** Update a leave request (only pending requests can be updated by owner)

**Request:**
```javascript
const updateLeaveRequest = async (leaveId, updateData) => {
  try {
    const response = await fetch(`/leaves/${leaveId}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updateData)
    });
    
    if (response.ok) {
      const updatedLeave = await response.json();
      console.log('Leave request updated:', updatedLeave);
      return updatedLeave;
    } else {
      const errorData = await response.json();
      console.error('Update failed:', errorData);
    }
  } catch (error) {
    console.error('Error updating leave request:', error);
  }
};
```

**Request Body Format:**
```json
{
  "leave_type": "sick_leave",  // optional
  "start_date": "2024-12-25",  // optional
  "end_date": "2024-12-27",    // optional
  "reason": "Updated reason",   // optional
  "contact": "987-654-3210"    // optional
}
```

**Note:** Regular users cannot update `status`. Only admins/supervisors can change status.

---

### 5. Delete Leave Request

**Endpoint:** `DELETE /leaves/{leave_id}`

**Description:** Delete a leave request (only pending requests can be deleted)

**Request:**
```javascript
const deleteLeaveRequest = async (leaveId) => {
  try {
    const response = await fetch(`/leaves/${leaveId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('Leave request deleted:', result);
      return result;
    } else {
      const errorData = await response.json();
      console.error('Delete failed:', errorData);
    }
  } catch (error) {
    console.error('Error deleting leave request:', error);
  }
};
```

**Response Format:**
```json
{
  "message": "Leave request deleted successfully",
  "leave_id": 123
}
```

---

## 📝 Field Descriptions

### Leave Types
- `annual_leave`: Annual vacation leave
- `sick_leave`: Medical/sick leave
- `personal_leave`: Personal leave

### Status Values
- `pending`: Waiting for approval
- `approved`: Request approved
- `rejected`: Request rejected

### Leave Request Fields
- `id`: Unique leave request identifier (integer)
- `user_id`: User ID who made the request (integer)
- `leave_type`: Type of leave (string enum)
- `start_date`: Start date of leave (YYYY-MM-DD)
- `end_date`: End date of leave (YYYY-MM-DD)
- `reason`: Reason for leave (string)
- `contact`: Contact information during leave (optional string)
- `status`: Request status (string enum)
- `reviewer_id`: ID of user who reviewed (optional integer)
- `created_at`: Date when request was created (YYYY-MM-DD)

---

## ⚠️ Important Notes

1. **Authentication Required**: All requests need a valid Authorization token
2. **Permission Restrictions**:
   - Regular users can only update/delete their own leave requests
   - Regular users cannot modify status
   - Only pending requests can be deleted or updated by owners
   - Admins/supervisors can approve/reject any leave requests
3. **Balance Validation**:
   - System checks if user has enough leave balance before approving request
   - If balance doesn't exist, it's created with default values (10 annual, 5 sick, 5 personal)
4. **Date Format**: YYYY-MM-DD
5. **Date Validation**: End date must be after start date

---

## 🚨 Error Handling

### Common Error Codes
- `400`: Bad Request (invalid dates, insufficient balance, etc.)
- `401`: Unauthorized (login required)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found (leave request doesn't exist)
- `422`: Validation Error (data validation failed)

### Error Response Format
```json
{
  "detail": "Error message or array of validation errors"
}
```

---

## 🔄 Complete Usage Flow

### Step 1: Get Leave Balance
```javascript
const balance = await getLeaveBalance();
// Display: Annual Leave: 10, Sick Leave: 5, Personal Leave: 5
```

### Step 2: Create Leave Request
```javascript
const leaveData = {
  leave_type: "annual_leave",
  start_date: "2024-12-24",
  end_date: "2024-12-26",
  reason: "Family Emergency",
  contact: "123-456-7890"
};

const newLeave = await createLeaveRequest(leaveData);
```

### Step 3: Get Recent Requests
```javascript
const leaves = await getLeaveRequests();
// Display in Recent Requests table
```

### Step 4: Update Leave (if pending)
```javascript
const updateData = {
  reason: "Updated reason"
};
const updatedLeave = await updateLeaveRequest(leaveId, updateData);
```

### Step 5: Delete Leave (if pending)
```javascript
const result = await deleteLeaveRequest(leaveId);
```

---

## 📚 Example: Complete Leave Request Workflow

```javascript
class LeaveManager {
  constructor(token) {
    this.token = token;
  }

  async getBalance() {
    const response = await fetch('/leaves/balance', {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
    return await response.json();
  }

  async createRequest(leaveData) {
    const response = await fetch('/leaves/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(leaveData)
    });
    return await response.json();
  }

  async getRequests() {
    const response = await fetch('/leaves/', {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
    return await response.json();
  }

  async deleteRequest(leaveId) {
    const response = await fetch(`/leaves/${leaveId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
    return await response.json();
  }
}

// Usage
const leaveManager = new LeaveManager(userToken);
const balance = await leaveManager.getBalance();
const requests = await leaveManager.getRequests();
```
