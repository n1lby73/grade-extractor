# Student Results Report Generator API

This project provides an API for generating individual student report cards based on results stored in an Excel file (`result.xlsx`) and a template (`template.xlsx`). The API allows users to upload student result data, generate reports, and identify students who are on probation or termination based on their course scores.

## API Overview

The application is built using Flask and exposes several API endpoints to upload data, generate reports, and manage student results.

### Available API Endpoints

- **POST /api/v1/login**: User login endpoint to authenticate and receive a JWT token.
- **POST /api/v1/reg**: Registration endpoint for new users.
- **POST /api/v1/result**: Uploads the `result.xlsx` file (student results).
- **POST /api/v1/template**: Uploads the `template.xlsx` file (student report template).
- **GET /api/v1/extractClasses**: Fetches all classes listed in the uploaded results file.
- **POST /api/v1/genresult**: Generates individual reports for students based on the selected class.

## Prerequisites

- Python 3.x
- Flask
- Flask-JWT-Extended
- openpyxl (for Excel file processing)
- Pandas (for processing student data)

You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## How to Use

This project uses a REST API for interacting with the system. You will need to use HTTP requests to communicate with the API. You can use tools like **Postman** or **cURL**, or you can integrate the API calls into your own system.

How to Use

To interact with the API, follow these steps:

-  User Authentication:
    -    Register or log in to the system to receive an authentication token.

- Upload Results Database:
    - Upload the student results file (result.xlsx) that contains student grades.

- Upload Template:
    - Upload the report template file (template.xlsx), which is used to generate individual student reports.

- Generate Reports:
    - Once the results and template are uploaded, select a class and generate individual student reports. These reports include details about probation or termination status based on student performance.

## API Documentation

For full API endpoint details, including request bodies, responses, and authentication instructions, please refer to the [API Documentation](https://github.com/n1lby73/grade-extractor/blob/main/Api_Documentation.md).

The documentation includes all necessary details to interact with the API, including:

- **Login:** Authentication process to obtain a JWT token.

- **Register:** Endpoint to register new users.

- **File Uploads:** How to upload results and template files.

- **Generate Reports:** Instructions for generating student reports by class.

### File Format Requirements

#### **`result.xlsx` (Student Data)**

- **Sheet Names**: Each sheet represents a class. The system will process sheets that contain "emy" or "ety" in their name and exclude sheets with "Assessment" or ">".
- **Row 3**: Contains the number of courses.
- **Row 5**: Contains course names.
- **Row 7 onward**: Contains student names in the format "Last Name, First Name, Middle Name".
- **Score Columns**: Student scores are listed next to their names.
- **Average Column**: The column after the last course column is for the average score.

#### **`template.xlsx` (Report Template)**

This template should contain placeholders for student names and course scores. The application will fill these placeholders with the data from the `result.xlsx` file.

## Authentication

- All endpoints except for **login** and **registration** require authentication.
- You must include the `Authorization: Bearer <access_token>` header in your requests to authenticated endpoints.
- The `access_token` is received upon successful login and is used to authenticate your requests.


## How to Test the API

To test the API, you can use tools like **Postman** or **cURL** to send requests to the endpoints. Make sure to:
1. Register a user via the **/api/v1/reg** endpoint.
2. Log in using the **/api/v1/login** endpoint to retrieve the `access_token`.
3. Use the token to authenticate other API requests (e.g., upload files and generate reports).

## License

This project is licensed under the MIT License.
