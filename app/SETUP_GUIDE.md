# User Microservice - Setup Summary

## 📦 What Has Been Created

A complete FastAPI-based user authentication microservice with the following structure:

```
app/
├── user/
│   ├── __init__.py           # Package initializer
│   ├── api.py                # API endpoints (register, login, profile)
│   ├── models.py             # User database model
│   ├── schemas.py            # Pydantic schemas for validation
│   ├── services.py           # Business logic & authentication
│   ├── main.py               # FastAPI application entry point
│   └── README.md             # Service documentation
├── config.py                 # Configuration management
├── database.py               # Database setup & session management
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── .env.example              # Environment template
├── .gitignore                # Git ignore file
├── Dockerfile                # Docker container configuration
├── docker-compose.yml        # Docker Compose orchestration
├── setup_user_service.ps1    # PowerShell setup script
├── setup_user_service.sh     # Bash setup script
└── test_api.py               # API testing script
```

## 🚀 Quick Start Guide

### Option 1: Using Setup Script (Recommended for Windows)

```powershell
cd D:\codes\simple-book-recommender\app
.\setup_user_service.ps1
```

### Option 2: Manual Setup

```powershell
# 1. Navigate to app directory
cd D:\codes\simple-book-recommender\app

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the service
python -m uvicorn user.main:app --host 0.0.0.0 --port 8001 --reload
```

### Option 3: Using Docker

```powershell
# Build and run with Docker Compose
docker-compose up --build
```

## 📡 API Endpoints

Once running, the service will be available at: **http://localhost:8001**

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/users/register` | Register new user | No |
| POST | `/api/v1/users/login` | Login & get JWT token | No |
| GET | `/api/v1/users/me` | Get current user profile | Yes |

### Health Check Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health status |

## 📚 API Documentation

Once the service is running, visit:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 🧪 Testing the API

### Method 1: Use the Test Script

```powershell
# Make sure service is running first
python test_api.py
```

### Method 2: Using cURL

**Register a user:**
```bash
curl -X POST "http://localhost:8001/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8001/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "johndoe",
    "password": "SecurePass123"
  }'
```

**Get Profile:**
```bash
curl -X GET "http://localhost:8001/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Method 3: Using Swagger UI

1. Open http://localhost:8001/docs
2. Click "Try it out" on any endpoint
3. Fill in the request body
4. Click "Execute"

## 🔧 Configuration

Edit `.env` file to configure:

```env
DATABASE_URL=sqlite+aiosqlite:///./user_service.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
API_PREFIX=/api/v1
```

**Important**: Change `SECRET_KEY` in production! Generate with:
```bash
openssl rand -hex 32
```

## 📦 Dependencies

Main dependencies installed:
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **SQLModel** - SQL database ORM
- **Pydantic** - Data validation
- **python-jose** - JWT token handling
- **passlib** - Password hashing
- **aiosqlite** - Async SQLite driver

## 🗄️ Database

- **Default**: SQLite (`user_service.db`)
- **Location**: `app/user_service.db`
- **Auto-created**: On first run

To use PostgreSQL instead:
```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
```

## 🔐 Security Features

✅ Password hashing with bcrypt
✅ JWT-based authentication
✅ Token expiration
✅ CORS middleware
✅ Input validation with Pydantic
✅ SQL injection protection with SQLModel

## 📝 Next Steps

1. **Start the service** using the setup script
2. **Test the API** using Swagger UI or test script
3. **Integrate with other microservices** (follow, book, etc.)
4. **Add email verification** for production
5. **Implement rate limiting** for security
6. **Set up monitoring** and logging

## 🐛 Troubleshooting

**Service won't start?**
- Check if port 8001 is available
- Verify Python 3.10+ is installed
- Check if all dependencies are installed

**Database errors?**
- Delete `user_service.db` and restart
- Check DATABASE_URL in .env

**Import errors?**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

## 📖 Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- JWT Introduction: https://jwt.io/introduction

## ✨ Features Implemented

✅ User registration with validation
✅ User login with JWT tokens
✅ Protected endpoints with authentication
✅ Password hashing and verification
✅ User profile management
✅ Health check endpoints
✅ API documentation (Swagger/ReDoc)
✅ Docker support
✅ Environment-based configuration
✅ Async database operations
✅ CORS middleware
✅ Proper error handling

---

**Service Status**: Ready for development ✅
**Port**: 8001
**Database**: SQLite (user_service.db)
**Documentation**: http://localhost:8001/docs

