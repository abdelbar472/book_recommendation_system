# app/user/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_db_and_tables, close_db
from app.user.api import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup: Create database tables
    print("Starting up User Microservice...")
    await create_db_and_tables()
    print("Database tables created successfully!")
    yield
    # Shutdown: Close database connections
    print("Shutting down User Microservice...")
    await close_db()
    print("Database connections closed.")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "User Microservice",
        "status": "running",
        "version": settings.api_version
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.user.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )

