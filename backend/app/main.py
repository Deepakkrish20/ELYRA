from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import spam, poem, movie

app = FastAPI(
    title="InsightAI API",
    description="Content Intelligence API for Spam, Poem, and Movie analysis",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# Include routers under the /api prefix
api_router = APIRouter(prefix="/api")
api_router.include_router(spam.router)
api_router.include_router(poem.router)
api_router.include_router(movie.router)

app.include_router(api_router)
