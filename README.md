# Book Management REST API

A CRUD-based REST API built with FastAPI and Supabase for managing books, with JWT-based authentication, secure password hashing, and role-based authorization.

## Features

- User registration and authentication
- JWT-based authentication using Bearer tokens
- Secure password hashing and verification with `pwdlib`
- Role-based authorization with admin access control
- CRUD operations for books
- Request and response validation using Pydantic
- UUID validation
- User account status verification
- Structured HTTP error handling
- Interactive API documentation with Swagger UI

## Tech Stack

- **Python**
- **FastAPI**
- **Supabase**
- **PostgreSQL**
- **Pydantic**
- **JWT**
- **pwdlib**

## API Operations

The API provides the following book management operations:

| Method | Operation |
|--------|-----------|
| GET | Retrieve books |
| POST | Create a book |
| PUT | Update a book |
| PATCH | Partially update a book |
| DELETE | Delete a book |

## Authentication & Authorization

The API uses JWT-based authentication with HTTP Bearer tokens.

### Authentication Flow

1. User creates an account.
2. The password is securely hashed before being stored.
3. User logs in with their credentials.
4. The API generates a JWT access token.
5. The token is sent with protected API requests using the Bearer authentication scheme.
6. FastAPI dependencies validate the token and retrieve the current user.
7. Admin-only operations additionally verify the user's role.

JWT tokens include the user's ID and an expiration time.

## Database

The application uses Supabase as the backend database.

### Users Table

- `id`
- `full_name`
- `email`
- `password_hash`
- `role`
- `is_active`
- `created_at`

### Books Table

- `id`
- `title`
- `author`
- `genre`
- `language`

## Project Structure

```text
supabase-fastapi/
│
├── models/
│
├── routers/
│
├── database.py
├── dependencies.py
├── security.py
├── main.py
├── .env
├── .gitignore
└── README.md
