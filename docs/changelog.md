# Changelog

## [v2.0.0] - 2025-02-10

### Added
- **Google Sheets Integration**: 
  - Replaced the previous method of downloading Excel files with direct interaction with Google Sheets. The API now retrieves student result data and generates reports directly from Google Sheets without requiring file downloads or uploads.
- **New API Endpoints for v2**:
  - **POST /api/v2/login**: Allows users to log in and receive JWT tokens.
  - **POST /api/v2/extractClasses**: Retrieves all available classes for a selected module from Google Sheets.
  - **POST /api/v2/genResult**: Generates individual student reports based on class data from Google Sheets.

### Changed
- **JWT Authentication**: Improved authentication and token management with JWT tokens.
- **Class Data Handling**: Adjusted data retrieval and parsing for courses, grades, and student information from Google Sheets, including dynamic column letter conversion.
- **Error Handling**: Enhanced error handling for API requests, particularly around token expiration and invalid tokens.
- **Data Handling Transition**: Moved away from file uploads (Excel sheets) in favor of direct API calls to Google Sheets for improved efficiency and accuracy.

### Deprecated
- **File Uploads**:
  - Removed the file upload method for the student results (`result.xlsx`) and template (`template.xlsx`), now replaced by direct access to Google Sheets.

---

## [v1.1.0] - 2025-02-01

### Added
- **File Uploads**:
  - **POST /api/v1/result**: Allows users to upload an Excel file (`result.xlsx`) containing student results.
  - **POST /api/v1/template**: Allows users to upload an Excel template file (`template.xlsx`) to generate student reports.
  
- **Report Generation**:
  - **POST /api/v1/genresult**: Allows users to generate individual student reports after uploading the result and template files.

### Changed
- **API Documentation**: Updated to include detailed explanations for the `result.xlsx` and `template.xlsx` formats.

---

## [v1.0.0] - 2024-12-20

### Added
- **Initial Release**: 
  - Basic functionality for generating student report cards from uploaded `result.xlsx` and `template.xlsx` files.
  - User registration and login functionality with JWT token-based authentication.
  - Endpoint for extracting classes from the `result.xlsx` file.
  