# **GradeTractor API v2 Documentation**

## Base URL:
`https://gradetractor.onrender.com`

---

## Authentication

**GradeTractor API v2** uses JWT (JSON Web Tokens) for user authentication. Tokens are issued upon successful login and are required to access protected endpoints.

- **Access Token**: Grants access to protected resources for a limited period.
- **Refresh Token**: Used to generate a new access token once the current one expires.

---

### **Login**
- **Endpoint**: `/api/v2/login`
- **Method**: `POST`
- **Description**: Authenticates the user by validating their `studentID`, `classCode`, and `password`. Upon successful authentication, the user is issued an `access_token` and a `refresh_token`.

#### **Request Body** (JSON):
```json
{
  "classCode": "XYZ101",
  "studentID": "S12345",
  "password": "password123"
}
```

#### **Response**:
- **Success** (200 OK):
  ```json
  {
    "success": "login successful",
    "token": {
      "access_token": "your_access_token",
      "refresh_token": "your_refresh_token"
    }
  }
  ```
- **Error** (400 Bad Request): 
  ```json
  {
    "error": "Student ID or Password is incorrect"
  }
  ```
- **Error** (404 Not Found):
  ```json
  {
    "error": "Invalid class code"
  }
  ```

**Example cURL Request**:
```bash
curl -X POST https://gradetractor.onrender.com/api/v2/login \
     -H "Content-Type: application/json" \
     -d '{"classCode": "XYZ101", "studentID": "S12345", "password": "password123"}'
```

---

### **Retrieve Classes**
- **Endpoint**: `/api/v2/extractClasses`
- **Method**: `POST`
- **Description**: Fetches all available classes for a given student module (e.g., `emy`, `ety`).

#### **Request Body** (JSON):
```json
{
  "studentModule": "emy"
}
```

#### **Response**:
- **Success** (200 OK):
  ```json
  {
    "availableClasses": [
      "Class 1",
      "Class 2",
      "Class 3"
    ]
  }
  ```
- **Error** (404 Not Found):
  ```json
  {
    "error": "unknown module received",
    "available modules": ["emy", "ety", "mod", "mech"]
  }
  ```

**Example cURL Request**:
```bash
curl -X POST https://gradetractor.onrender.com/api/v2/extractClasses \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{"studentModule": "emy"}'
```

---

### **Generate Results**
- **Endpoint**: `/api/v2/genResult`
- **Method**: `POST`
- **Description**: Retrieves the student’s results for their registered courses, including technical courses like "Technical Communication" and others. Requires JWT authentication.

#### **Authentication**:
You need to include the `Authorization` header with a valid JWT access token:
```bash
Authorization: Bearer <access_token>
```

#### **Response**:
- **Success** (200 OK):
  ```json
  {
    "studentData": {
      "Technical Communication": 95,
      "Engineering Physics": 88,
      "Industrial Safety": 74,
      "name": "John Doe",
      "id": "S12345",
      "class": "XYZ101"
    }
  }
  ```
- **Error** (401 Unauthorized):
  ```json
  {
    "error": "Expired or invalid token"
  }
  ```

**Example cURL Request**:
```bash
curl -X POST https://gradetractor.onrender.com/api/v2/genResult \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{}'
```

---

## Utility Functions

### **colNumberToLetter(col_num)**
Converts a column number to its corresponding letter notation (e.g., `1 -> A`, `28 -> AB`).

#### **Example**:
```python
colNumberToLetter(1)  # Returns 'A'
colNumberToLetter(28) # Returns 'AB'
```

### **my_expired_token_callback(jwt_header, jwt_payload)**
This function is called when the user's access token expires. It returns a message indicating that the token has expired.

#### **Response**:
```json
{
  "message": "expired token"
}
```

### **handle_invalid(error)**
This function is called when an invalid token is detected. It returns an error message indicating that the token is invalid.

#### **Response**:
```json
{
  "message": "invalid token",
  "error": "error details"
}
```

---

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request. Here are some common error responses:

- **400 Bad Request**: The request could not be understood or is missing required parameters.
- **401 Unauthorized**: Invalid or expired JWT token.
- **404 Not Found**: The requested resource was not found (e.g., incorrect class code).
- **500 Internal Server Error**: A server error occurred while processing the request.

### Example Error Responses:

- **Invalid Student Credentials**:
  - **Status**: 401
  - **Response**:
  ```json
  {
    "error": "Student ID or Password is incorrect"
  }
  ```

- **Unknown Module**:
  - **Status**: 404
  - **Response**:
  ```json
  {
    "error": "unknown module received",
    "available modules": ["emy", "ety", "mod", "mech"]
  }
  ```

---

## Environment Variables

The API uses environment variables for configuration. Make sure the following environment variables are set:

- `googleCred`: The base64-encoded credentials for the Google Sheets API.
- `emyResultSheet`: The Google Spreadsheet ID for the "EMY" module.
- `etyResultSheet`: The Google Spreadsheet ID for the "ETY" module.
- `modResultSheet`: The Google Spreadsheet ID for the "MOD" module.
- `mechResultSheet`: The Google Spreadsheet ID for the "MECH" module.

These variables are essential for accessing and interacting with the corresponding Google Spreadsheets for each module.

---

## Conclusion

This API facilitates seamless interaction with Google Spreadsheets, providing authenticated access to student data, class lists, and results. It supports secure authentication via JWT and provides utility functions for data handling, such as column conversion. By following the endpoints, users can easily manage and retrieve student results for their courses.

---

This documentation covers the main functionality of API v2, ensuring that developers can quickly integrate with and utilize the GradeTractor system for various student management tasks.