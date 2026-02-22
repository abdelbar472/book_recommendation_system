"""
User Microservice - Overview

This microservice handles all user-related operations including:
- User registration
- User authentication (login/logout)
- User profile management
- JWT token generation and validation

Technology Stack:
- FastAPI: Modern, fast web framework
- SQLModel: SQL database ORM with Pydantic integration
- SQLite: Default database (easily switchable to PostgreSQL/MySQL)
- JWT: Token-based authentication
- bcrypt: Password hashing
- Pydantic: Data validation

Architecture:
- models.py: Database models (User table)
- schemas.py: Request/response schemas (validation)
- services.py: Business logic and authentication
- api.py: API endpoints/routes
- main.py: Application entry point
- database.py: Database configuration
- config.py: Settings management

Security Features:
✓ Password hashing with bcrypt
✓ JWT token authentication
✓ Input validation
✓ SQL injection protection
✓ CORS middleware

Database Schema:
User Table:
- id (UUID, primary key)
- email (unique, indexed)
- username (unique, indexed)
- first_name (optional)
- last_name (optional)
- bio (optional)
- website (optional)
- hashed_password (never exposed in API)
- created_at (timestamp)
- updated_at (timestamp)

API Endpoints:
POST /api/v1/users/register - Register new user
POST /api/v1/users/login - Login and get JWT token
GET /api/v1/users/me - Get current user profile (authenticated)

Integration Points:
- Can be integrated with Follow microservice for social features
- Can be integrated with Book microservice for book management
- Can be integrated with Recommendation microservice for personalized suggestions
- Uses JWT tokens that can be validated by other microservices

Running the Service:
Option 1: PowerShell script
    .\setup_user_service.ps1

Option 2: Direct uvicorn
    python -m uvicorn user.main:app --host 0.0.0.0 --port 8001 --reload

Option 3: Docker
    docker-compose up --build

Testing:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
- Test Script: python test_api.py

Next Steps for Full Book Recommender System:
1. ✓ User Microservice (COMPLETED)
2. Follow Microservice (following/followers)
3. Book Microservice (books, publishers, authors, sagas)
4. Media Microservice (ratings, comments, likes)
5. Recommendation Microservice (vector DB, embeddings)

Each microservice should:
- Run on its own port
- Have its own database
- Communicate via REST API or message queue
- Be independently deployable
- Have its own Docker container
"""

