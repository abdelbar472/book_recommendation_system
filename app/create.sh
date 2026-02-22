#!/bin/bash

PROJECT_ROOT="$(pwd)"
cd "$PROJECT_ROOT"

# Create microservices directory
mkdir -p microservices
cd microservices

# Define services array
services=("user-service" "follow-service" "interaction-service" "book-service" "recommendation-service" "api-gateway")

for service in "${services[@]}"; do
    echo "Creating $service..."

    # Create directory structure
    mkdir -p "$service/app/api"
    mkdir -p "$service/app/core"
    mkdir -p "$service/app/db"
    mkdir -p "$service/app/schemas"
    mkdir -p "$service/app/services"

    # Create Python files
    touch "$service/app/__init__.py"
    touch "$service/app/api/__init__.py"
    touch "$service/app/api/routes.py"
    touch "$service/app/core/__init__.py"
    touch "$service/app/core/config.py"
    touch "$service/app/core/security.py"
    touch "$service/app/db/__init__.py"
    touch "$service/app/db/database.py"
    touch "$service/app/db/models.py"
    touch "$service/app/schemas/__init__.py"
    touch "$service/app/schemas/schemas.py"
    touch "$service/app/services/__init__.py"
    touch "$service/app/services/service.py"
    touch "$service/app/main.py"

    # requirements.txt
    cat > "$service/requirements.txt" <<EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
httpx==0.25.2
psycopg2-binary==2.9.9
redis==5.0.1
python-dotenv==1.0.0
EOF

    # Add vector DB dependencies for recommendation service
    if [ "$service" == "recommendation-service" ]; then
        cat >> "$service/requirements.txt" <<EOF
sentence-transformers==2.2.2
chromadb==0.4.18
numpy==1.24.3
EOF
    fi

    # .env
    db_name=$(echo "$service" | tr '-' '_')
    cat > "$service/.env" <<EOF
DATABASE_URL=postgresql://user:password@localhost:5432/$db_name
SECRET_KEY=your-secret-key-change-this
SERVICE_NAME=$service
SERVICE_PORT=800X
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
EOF

    # .gitignore
    cat > "$service/.gitignore" <<EOF
__pycache__/
*.py[cod]
*\$py.class
.env
.venv
venv/
env/
*.db
*.sqlite3
.pytest_cache/
.coverage
.idea/
.vscode/
alembic/versions/
EOF

    # Dockerfile
    cat > "$service/Dockerfile" <<EOF
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
EOF

    # main.py
    cat > "$service/app/main.py" <<EOF
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import routes

app = FastAPI(title=settings.SERVICE_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

@app.get("/")
async def root():
    return {"service": settings.SERVICE_NAME, "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
EOF

    # config.py
    cat > "$service/app/core/config.py" <<EOF
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "$service"
    SERVICE_PORT: int = 8000
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
EOF

    echo "$service created successfully!"
done

echo "All microservices created successfully!"
