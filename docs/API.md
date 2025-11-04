# API Documentation

## Overview

This is a RESTful API built with Flask that provides authentication, user management, and game catalog functionality.

## Base URL

```
http://localhost:5100
```

## Standard Response Format

All API responses follow this standard format:

```json
{
  "success": boolean,
  "data": object | array | null,
  "message": string,
  "timestamp": string (ISO 8601 format)
}
```

### Success Response Example

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com"
    }
  },
  "message": "Operation successful",
  "timestamp": "2025-01-15T10:30:45.123Z"
}
```

### Error Response Example

```json
{
  "success": false,
  "data": null,
  "message": "Invalid email or password",
  "timestamp": "2025-01-15T10:30:45.123Z"
}
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Protected endpoints require an `Authorization` header with a Bearer token.

### Header Format

```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### Health Check

#### GET /api/v1/health/status

Check if the API is running.

**Response:**

```json
{
  "success": true,
  "data": {
    "status": "healthy"
  },
  "message": "API is running",
  "timestamp": "2025-01-15T10:30:45.123Z"
}
```

---

### Authentication Endpoints

#### POST /api/v1/auth/register

Register a new user account.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Validation Rules:**
- Email must be valid format
- Password must be at least 8 characters

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "User registered successfully",
  "timestamp": "2025-01-15T10:30:45.123Z"
}
```

**Error Responses:**
- 400: Invalid input data
- 409: Email already exists

---

#### POST /api/v1/auth/login

Authenticate and receive access tokens.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Login successful",
  "timestamp": "2025-01-15T10:30:45.123Z"
}
```

**Error Responses:**
- 400: Missing credentials
- 401: Invalid email or password

---

#### POST /api/v1/auth/refresh

Refresh an expired access token using a refresh token.

**Request Body:**

```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Token refreshed successfully",
  "timestamp": "2025-01-15T10:30:45.123Z"
}
```

**Error Responses:**
- 400: Missing refresh token
- 401: Invalid or expired refresh token
- 404: User not found

---

#### POST /api/v1/auth/logout

Logout the current user (client should discard tokens).

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**

```json
{
  "success": true,
  "data": null,
  "message": "Logout successful",
  "timestamp": "2025-01-15T10:30:45.123Z"
}
```

**Error Responses:**
- 401: Missing or invalid token

---

### User Management Endpoints

#### GET /api/v1/users/profile

Get the current user's profile.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "createdAt": "2025-01-15T10:00:00.000Z",
    "updatedAt": "2025-01-15T10:30:00.000Z"
  },
  "message": "Profile retrieved successfully",
  "timestamp": "2025-01-15T10:30:45.123Z"
}
```

**Error Responses:**
- 401: Missing or invalid token
- 500: Server error

---

#### PUT /api/v1/users/profile

Update the current user's profile.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "email": "newemail@example.com"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "newemail@example.com",
    "createdAt": "2025-01-15T10:00:00.000Z",
    "updatedAt": "2025-01-15T10:35:00.000Z"
  },
  "message": "Profile updated successfully",
  "timestamp": "2025-01-15T10:35:45.123Z"
}
```

**Error Responses:**
- 400: Invalid input data
- 401: Missing or invalid token
- 409: Email already in use
- 500: Server error

---

#### DELETE /api/v1/users/account

Delete the current user's account.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**

```json
{
  "success": true,
  "data": null,
  "message": "Account deleted successfully",
  "timestamp": "2025-01-15T10:40:45.123Z"
}
```

**Error Responses:**
- 401: Missing or invalid token
- 500: Server error

---

### Game Endpoints

#### GET /api/games

Get a list of all games.

**Success Response (200):**

```json
[
  {
    "id": 1,
    "title": "Pipeline Panic",
    "description": "Build your DevOps pipeline before chaos ensues",
    "publisher": {
      "id": 1,
      "name": "DevGames Inc"
    },
    "category": {
      "id": 1,
      "name": "Strategy"
    },
    "starRating": 4.5
  }
]
```

---

#### GET /api/games/{id}

Get details of a specific game by ID.

**URL Parameters:**
- `id` (integer): Game ID

**Success Response (200):**

```json
{
  "id": 1,
  "title": "Pipeline Panic",
  "description": "Build your DevOps pipeline before chaos ensues",
  "publisher": {
    "id": 1,
    "name": "DevGames Inc"
  },
  "category": {
    "id": 1,
    "name": "Strategy"
  },
  "starRating": 4.5
}
```

**Error Responses:**
- 404: Game not found

---

## Security Features

### Password Security
- Passwords are hashed using bcrypt with 12 salt rounds
- Minimum password length: 8 characters
- Passwords are never returned in API responses

### JWT Tokens
- Access tokens expire after 24 hours
- Refresh tokens expire after 7 days
- Tokens are signed with HS256 algorithm

### Rate Limiting
- Default: 100 requests per 15 minutes per IP address
- Applied globally to all endpoints

### Security Headers
All responses include the following security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: default-src 'self'`

### CORS
CORS is configured to allow requests from:
- `http://localhost:4321`
- `http://localhost:3000`

Allowed methods: GET, POST, PUT, DELETE, OPTIONS
Allowed headers: Content-Type, Authorization

### Input Validation
- All email addresses are validated using regex patterns
- Input is sanitized to prevent XSS attacks
- Required fields are validated before processing

---

## Error Codes

| Status Code | Meaning |
|------------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Missing or invalid authentication |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 500 | Internal Server Error - Server error |

---

## Environment Variables

Create a `.env` file in the project root (see `.env.example` for template):

```env
# JWT secret for token signing (required in production)
JWT_SECRET=your-secret-key-here

# Flask configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database URI (optional - defaults to SQLite)
# DATABASE_URI=postgresql://user:password@localhost/dbname
```

---

## Testing

Run all tests:

```bash
./scripts/run-server-tests.sh
```

Or run tests individually:

```bash
source venv/bin/activate
PYTHONPATH=/path/to/project/server python -m unittest server/tests/test_auth.py
```

---

## Getting Started

1. Install dependencies:
```bash
./scripts/setup-env.sh
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the server:
```bash
./scripts/start-app.sh
```

The API will be available at `http://localhost:5100`

---

## Support

For issues or questions, please open an issue on the GitHub repository.
