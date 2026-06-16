from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter(prefix="/movie", tags=["Movie Analysis"])

class MovieRequest(BaseModel):
    synopsis: str

class GenreConfidence(BaseModel):
    name: str
    confidence: float

class MovieResponse(BaseModel):
    genres: List[GenreConfidence]
    advisories: Dict[str, str]
    key_themes: List[str]
    runtime_estimate: str

@router.post("/analyze", response_model=MovieResponse)
async def analyze_movie(payload: MovieRequest):
    if not payload.synopsis.strip():
        raise HTTPException(status_code=400, detail="Synopsis content cannot be empty.")
    
    # Mock analysis response
    return MovieResponse(
        genres=[
            {"name": "Sci-Fi", "confidence": 0.92},
            {"name": "Thriller", "confidence": 0.78},
            {"name": "Mystery", "confidence": 0.54}
        ],
        advisories={
            "violence": "Low",
            "language": "Moderate",
            "nudity": "None"
        },
        key_themes=["Artificial Intelligence", "Existentialism", "Corporate Greed"],
        runtime_estimate="105 - 120 mins"
    )
    
