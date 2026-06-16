from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter(prefix="/poem", tags=["Poem Analysis"])

class PoemRequest(BaseModel):
    text: str

class PoemResponse(BaseModel):
    emotions: Dict[str, float]
    morals: List[str]
    poetic_devices: List[str]

@router.post("/analyze", response_model=PoemResponse)
async def analyze_poem(payload: PoemRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Poem content cannot be empty.")
    
    # Mock analysis response
    return PoemResponse(
        emotions={
            "Melancholy": 0.65,
            "Joy": 0.12,
            "Nostalgia": 0.84,
            "Awe": 0.45
        },
        morals=[
            "Time is transient and fleeting, encouraging the reader to treasure existing bonds.",
            "Nature serves as a quiet witness to human existence."
        ],
        poetic_devices=["Alliteration", "Metaphor", "Imagery"]
    )
