# FastAPI Standup App

## Overview

This project is a Dockerized FastAPI application with PostgreSQL as the backend database. It allows users to create standups, query their past standups by day or date, and includes an admin panel for user management. The application also demonstrates how ORMs can safeguard against SQL injection vulnerabilities.

## Features

- **User Authentication**: Users can log in to access their standups.
- **Standup Management**: Employees can create and view their daily standups.
- **Admin Panel**: Only admins can create or delete users.
- **SQL Injection Demonstration**: Shows how using raw SQL queries can lead to vulnerabilities compared to ORM queries.

## Project Structure

- `app/`: Contains the FastAPI application code.
  - `__init__.py`: Package initialization.
  - `config.py`: Application configuration settings.
  - `database.py`: Database setup and session management.
  - `utils.py`: Utility functions.
  - `schemas.py`: Pydantic schemas for request and response validation.
  - `models.py`: SQLAlchemy models for `User` and `Standup`.
  - `oauth2.py`: OAuth2 authentication and JWT handling.
  - `main.py`: Application entry point.
  - `requirements.txt`: Python dependencies for the FastAPI application.
  - `Dockerfile`: Docker configuration for the FastAPI application.

- `routers/`: Contains different API routers.
  - `auth.py`: Routes related to user authentication.
  - `standups.py`: Routes for managing standups.
  - `users.py`: Routes for managing users.
  - `sql_injection_demo.py`: Demonstrates SQL injection vulnerabilities.

- `.env`: Environment variables for database connection and initial admin user credentials.
- `docker-compose.yaml`: Docker Compose configuration for the application and database.
- `README.md`: This file.

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/fastapi-standup-app.git
   cd fastapi-standup-app
   ```

2. **Build and Start Containers**

    ```bash
    docker-compose up -d --build
    ```

3. **Initialize the Database**

    The application will automatically create the required tables and the initial admin user based on the credentials in the `.env` file.

4. **Accessing the Application**

    The FastAPI application will be accessible at http://localhost:8000. You can view the API documentation at http://localhost:8000/docs.

## API Endpoints

### User Endpoints

- **Login**
  - `POST /login`
  - Description: Authenticates users and returns a JWT token.
  - **Request Body**: 
    - `username` (string): The user's username.
    - `password` (string): The user's password.
  - **Response**: 
    - `access_token` (string): JWT token for authentication.
    - `token_type` (string): The type of token (e.g., "bearer").

### Standup Endpoints

- **Create Standup**
  - `POST /create_standup/`
  - Description: Allows users to create a new standup entry. Does not allow users to create standups for future dates. Standup date defaults to current day's if no date is provided.
  - **Request Body**: 
    - `standup_data` (object): Contains details about the standup.
      - `content` (string): The content of the standup.
      - `date` (string, date): The date of the standup.
  - **Response**: 
    - `id` (integer): The ID of the created standup.
    - `content` (string): The content of the standup.
    - `date` (string, date): The date of the standup.

- **Get Standups by Date**
  - `GET /by_date/{requested_date}/`
  - Description: Retrieves standups for a given date.
  - **Path Parameter**:
    - `requested_date` (string, date): The date for which to retrieve standups.
  - **Response**: 
    - `standups` (array of objects): List of standups for the specified date.

- **Get Standups by Days**
  - `GET /by_days/{days}/`
  - Description: Retrieves standups for the past number of days.
  - **Path Parameter**:
    - `days` (integer): Number of past days to retrieve standups for.
  - **Query Parameter**:
    - `v` (boolean, optional): Verbose mode (default: false).
  - **Response**: 
    - `standups` (array of objects): List of standups for the past specified days.

### Admin Panel Endpoints

- **Create User**
  - `POST /register`
  - Description: Allows admins to create new users.
  - **Request Body**: 
    - `user` (object): User details.
      - `username` (string): The user's username.
      - `password` (string): The user's password.
      - `email` (string): The user's email address.
  - **Response**: 
    - `id` (integer): The ID of the created user.
    - `username` (string): The username of the created user.
    - `email` (string): The email of the created user.

- **Delete User**
  - `DELETE /{id}`
  - Description: Allows admins to delete existing users.
  - **Path Parameter**:
    - `id` (integer): The ID of the user to delete.
  - **Response**: 
    - Status code `204 No Content`: Successfully deleted.

### User Endpoints

- **Get User**
  - `GET /{id}`
  - Description: Retrieves details of a specific user.
  - **Path Parameter**:
    - `id` (integer): The ID of the user to retrieve.
  - **Response**: 
    - `id` (integer): The user's ID.
    - `username` (string): The username of the user.
    - `email` (string): The email of the user.

- **Get Users**
  - `GET /`
  - Description: Retrieves a list of all users.
  - **Response**: 
    - `users` (array of objects): List of all users.

- **Update User**
  - `PUT /update/{id}`
  - Description: Allows users to update their own details.
  - **Path Parameter**:
    - `id` (integer): The ID of the user to update.
  - **Request Body**: 
    - `user_data` (object): User update details.
      - `username` (string, optional): New username.
      - `email` (string, optional): New email address.
  - **Response**: 
    - `id` (integer): The user's ID.
    - `username` (string): The updated username.
    - `email` (string): The updated email.

### SQL Injection Demonstration

- **Using ORM**
  - `GET /sql_injections/orm/{user_id}/`
  - Description: Retrieves standups using ORM, protected against SQL Injection.
  - **Path Parameter**:
    - `user_id` (integer): The ID of the user to retrieve standups for.
  - **Response**: 
    - `standups` (array of objects): List of standups for the specified user.
  - **Note**: This endpoint is secured with ORM and will reject invalid inputs that attempt SQL injection. If an invalid or malicious `user_id` is provided, it will return an error and not process the request.

- **Using Raw SQL**
  - `GET /sql_injections/raw/{user_id}/`
  - Description: Retrieves standups using raw SQL, demonstrating SQL Injection vulnerability.
  - **Path Parameter**:
    - `user_id` (integer): The ID of the user to retrieve standups for.
  - **Response**: 
    - `standups` (array of objects): List of standups for the specified user.
  - **Note**: This endpoint is vulnerable to SQL Injection. For example, if you pass `1` or `1=1` as the `user_id`, the endpoint will incorrectly display standups for all users in the database. This is because the raw SQL query is not protected against SQL Injection, potentially leaking information that should be restricted. In contrast, the ORM-based endpoint will not process such requests and will return an error, preventing unauthorized access to other users' data.



## Configuration 
- The application configuration, including database connection details and initial admin credentials, is managed via the `.env` file. Ensure you have this file configured before running the application.

## Notes

- This project is intended for educational purposes to demonstrate SQL injection vulnerabilities and ORM protection.
- Ensure that you secure your application properly before deploying it in a production environment.

## Contributing
    Feel free to open issues or submit pull requests to improve the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
