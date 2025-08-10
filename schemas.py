from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ProfileAnalysis(BaseModel):
    attractiveness_score: int  # 1-10
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    red_flags: List[str]
    overall_assessment: str

class ConversationAnalysis(BaseModel):
    context_summary: str
    suggested_replies: List[str]
    conversation_health: str  # good/concerning/red_flag
    next_steps: List[str]

class BioSuggestion(BaseModel):
    improved_bio: str
    key_changes: List[str]
    reasoning: str

class RoastResponse(BaseModel):
    roast_content: str
    constructive_feedback: List[str]
    humor_level: str  # mild/medium/savage
