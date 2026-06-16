from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/spam", tags=["Spam Detection"])

class SpamRequest(BaseModel):
    text: str

class SpamResponse(BaseModel):
    is_spam: bool
    confidence: float
    message: str

@router.post("/analyze", response_model=SpamResponse)
async def analyze_spam(payload: SpamRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")
    
    # Mock analysis response
    text_lower = payload.text.lower()
    is_spam = "free" in text_lower or "winner" in text_lower or "money" in text_lower
    confidence = 0.95 if is_spam else 0.85
    msg = "Text identified as potential spam." if is_spam else "Text appears to be safe."
    
    return SpamResponse(
        is_spam=is_spam,
        confidence=confidence,
        message=msg
    )
