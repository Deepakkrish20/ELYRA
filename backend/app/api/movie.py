from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.movie_classifier import classify_movie

router = APIRouter(prefix="/movie", tags=["Movie Analysis"])

class MovieRequest(BaseModel):
    title: str
    year: Optional[str] = ""

class GenreConfidence(BaseModel):
    name: str
    confidence: float

class MovieResponse(BaseModel):
    title: str
    year: str
    genres: List[GenreConfidence]
    advisories: Dict[str, str]
    key_themes: List[str]
    runtime_estimate: str
    watchability_status: str
    summary: str

@router.post("/analyze", response_model=MovieResponse)
async def analyze_movie(payload: MovieRequest):
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="Movie title cannot be empty.")
        
    result = classify_movie(
        title=payload.title,
        year=payload.year
    )
    
    return MovieResponse(
        title=result["title"],
        year=result["year"],
        genres=[GenreConfidence(name=g["name"], confidence=g["confidence"]) for g in result["genres"]],
        advisories=result["advisories"],
        key_themes=result["key_themes"],
        runtime_estimate=result["runtime_estimate"],
        watchability_status=result["watchability_status"],
        summary=result["summary"]
    )
