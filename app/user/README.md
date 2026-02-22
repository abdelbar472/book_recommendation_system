# User Microservice

A FastAPI-based microservice for user authentication and management.

## Features

- **User Registration**: Create new user accounts with email verification
- **User Authentication**: JWT-based authentication with login/logout
- **User Profile**: View and manage user profiles
- **Password Hashing**: Secure password storage using bcrypt
- **Async Database**: SQLModel with async SQLAlchemy for database operations

## API Endpoints

### Authentication
- `POST /api/v1/users/register` - Register a new user
- `POST /api/v1/users/login` - Login and get JWT token
- `GET /api/v1/users/me` - Get current user profile (requires authentication)

### Health Check
- `GET /` - Service health check
- `GET /health` - Detailed health status

## Setup

### Prerequisites
- Python 3.10+
- pip

### Quick Start (Windows PowerShell)

```powershell
# Run the setup script
.\setup_user_service.ps1
```

### Quick Start (Linux/Mac)

```bash
# Make the script executable
chmod +x setup_user_service.sh

# Run the setup script
./setup_user_service.sh
```

### Manual Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run the Service**
   ```bash
   python -m uvicorn user.main:app --host 0.0.0.0 --port 8001 --reload
   ```

## Configuration

Edit the `.env` file to configure:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key (generate with `openssl rand -hex 32`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `CORS_ORIGINS`: Allowed CORS origins

## API Documentation

Once the service is running, visit:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## Project Structure

```
app/
├── user/
│   ├── __init__.py
│   ├── api.py          # API routes
│   ├── models.py       # Database models
│   ├── schemas.py      # Pydantic schemas
│   ├── services.py     # Business logic
│   └── main.py         # FastAPI application
├── config.py           # Configuration
├── database.py         # Database setup
├── requirements.txt    # Dependencies
├── .env                # Environment variables
└── setup_user_service.ps1  # Setup script
```

## Database

The service uses SQLite by default (`user_service.db`). To use a different database:

1. Update `DATABASE_URL` in `.env`
2. Install the appropriate driver (e.g., `asyncpg` for PostgreSQL)

Example for PostgreSQL:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/userdb
```

## Testing

Example API calls:

### Register a User
```bash
curl -X POST "http://localhost:8001/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8001/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "johndoe",
    "password": "securepassword123"
  }'
```

### Get Profile (with token)
```bash
curl -X GET "http://localhost:8001/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Docker Support

Build and run with Docker:

```bash
docker build -t user-microservice .
docker run -p 8001:8001 user-microservice
```

## Security Notes

- Always use HTTPS in production
- Change the `SECRET_KEY` in production
- Use strong passwords (min 8 characters)
- Implement rate limiting for authentication endpoints
- Add email verification for production use

## License

MIT

