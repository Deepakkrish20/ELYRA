from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.spam_detector import detect_spam, correct_prediction

router = APIRouter(prefix="/spam", tags=["Spam Detection"])

class SpamRequest(BaseModel):
    text: str

class FeedbackRequest(BaseModel):
    text: str
    was_spam: bool
    is_spam: bool

class SpamResponse(BaseModel):
    is_spam: bool
    confidence: float
    message: str
    spam_score: float
    ham_score: float
    keywords_detected: list[str]

@router.post("/analyze", response_model=SpamResponse)
async def analyze_spam(payload: SpamRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")
    
    result = detect_spam(payload.text)
    return SpamResponse(**result)

@router.post("/feedback", response_model=SpamResponse)
async def feedback_spam(payload: FeedbackRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")
    
    result = correct_prediction(payload.text, payload.was_spam, payload.is_spam)
    return SpamResponse(**result)

