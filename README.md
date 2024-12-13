# grade-extractor
extract grades of every course per students from a excel sheet and email to individual parent


### API Documentation for **GradeTractor API**

Base URL:  
`https://gradetractor.onrender.com`

---

### Authentication

#### **Login**
- **Endpoint**: `/api/v1/login`
- **Method**: `POST`
- **Description**: Logs a user in and returns a JWT token for authentication.
  
- **Request Body** (JSON):
  ```json
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```

- **Response**:
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
      "Error": "Email or password is incorrect"
    }
    ```

---

#### **Register**
- **Endpoint**: `/api/v1/reg`
- **Method**: `POST`
- **Description**: Registers a new user and stores their email and password (hashed) in the database.
  
- **Request Body** (JSON):
  ```json
  {
    "email": "new_user@example.com",
    "password": "new_user_password"
  }
  ```

- **Response**:
  - **Success** (201 Created):
    ```json
    {
      "message": "Data inserted successfully",
      "inserted_id": "inserted_user_id"
    }
    ```
  - **Error** (400 Bad Request): 
    ```json
    {
      "Error": "Mail already exist"
    }
    ```

---

### Results Management

#### **Upload Results Database**
- **Endpoint**: `/api/v1/result`
- **Method**: `POST`
- **Description**: Uploads the results database (a `.xlsx` file).
  
- **Request**:
  - `file`: The results file (must be `.xlsx` format).

- **Response**:
  - **Success** (200 OK):
    ```json
    {
      "message": "File uploaded successfully"
    }
    ```
  - **Error** (400 Bad Request): 
    ```json
    {
      "error": "Invalid file format. Please upload a file with the .xlsx extension."
    }
    ```

---

#### **Upload Template**
- **Endpoint**: `/api/v1/template`
- **Method**: `POST`
- **Description**: Uploads the template file (a `.xlsx` file) to generate the reports.
  
- **Request**:
  - `file`: The template file (must be `.xlsx` format).

- **Response**:
  - **Success** (200 OK):
    ```json
    {
      "message": "File uploaded successfully"
    }
    ```
  - **Error** (400 Bad Request): 
    ```json
    {
      "error": "Invalid file format. Please upload a file with the .xlsx extension."
    }
    ```

---

#### **Get All Classes**
- **Endpoint**: `/api/v1/extractClasses`
- **Method**: `GET`
- **Description**: Fetches all classes from the uploaded results file.

- **Response**:
  - **Success** (200 OK):
    ```json
    {
      "allClasses": ["Class A", "Class B", "Class C"]
    }
    ```
  - **Error** (404 Not Found): 
    ```json
    {
      "error": "Results database not uploaded. Please upload the results file before proceeding."
    }
    ```

---

#### **Generate Results**
- **Endpoint**: `/api/v1/genresult`
- **Method**: `POST`
- **Description**: Generates the individual results for a given class, including probation and termination lists.

- **Request Body** (JSON):
  ```json
  {
    "className": "Class A"
  }
  ```

- **Response**:
  - **Success** (200 OK):
    - The response will be a **zip file** containing the generated individual reports for the selected class.
  
  - **Error** (400 Bad Request):
    ```json
    {
      "error": "Results database not uploaded. Please upload the results file before proceeding."
    }
    ```
  - **Error** (404 Not Found): 
    ```json
    {
      "error": "Class {className} not found. Please ensure the class exists in the uploaded results file."
    }
    ```

---

### Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request. Below are some common error responses:

- **400 Bad Request**: The request could not be understood or was missing required parameters (e.g., missing file, invalid format).
- **401 Unauthorized**: Invalid or expired JWT token.
- **404 Not Found**: The requested resource was not found (e.g., missing class in the results).
- **500 Internal Server Error**: An error occurred on the server while processing the request.

---

### JWT Authentication

For endpoints requiring JWT authentication (`/api/v1/result`, `/api/v1/template`, `/api/v1/extractClasses`, `/api/v1/genresult`), you must include the `Authorization` header with the `Bearer <access_token>`.

Example:
```bash
Authorization: Bearer <access_token>
```

The `access_token` can be obtained by logging in through the `/api/v1/login` endpoint.

---

### Notes:

- The **Results Database** and **Template** files should be in `.xlsx` format.
- After uploading the results database and template, the system validates if both files are available before proceeding.
- For **Generating Results**, you must specify the class name (from the available classes) to generate individual reports.
- The generated reports include a list of students on probation or termination based on their performance.