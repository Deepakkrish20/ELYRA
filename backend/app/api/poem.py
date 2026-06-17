from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.services.poem_analyzer import analyze_poem_text

router = APIRouter(prefix="/poem", tags=["Poem Analysis"])

class PoemRequest(BaseModel):
    text: str

class SuggestedPoem(BaseModel):
    title: str
    author: str

class PoemResponse(BaseModel):
    emotions: Dict[str, float]
    poetic_devices: List[str]
    intention: str
    suitable_age_group: str
    moral: str
    meaning: str
    real_life_example: str
    suggested_poems: List[SuggestedPoem]

@router.post("/analyze", response_model=PoemResponse)
async def analyze_poem(payload: PoemRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Poem content cannot be empty.")
    
    result = analyze_poem_text(payload.text)
    return PoemResponse(**result)
