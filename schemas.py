from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    question: str
    student_id: Optional[int] = None
