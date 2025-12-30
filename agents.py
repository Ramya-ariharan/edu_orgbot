
# agent.py

from rag_service import get_answer
from typing import Optional
# from rag.rag_service import get_answer
from stud_service import get_student_marks,format_marks_answer

from studdata import STUDENTS



def is_marks_question(question: str) -> bool:
    keywords = [
        "marks", "mark", "result", "score",
        "total", "my total", "my marks",
        "subject", "performance"
    ]
    q = question.lower()
    return any(k in q for k in keywords)

def chatbot_agent(question: str, student_id: Optional[int] = None):
    # 🔐 Personal query
    if is_marks_question(question):
        if not student_id:
            return (
                "For security reasons, I can’t access personal academic details. "
                "Please contact our HR/Admin team."
            )

        marks = get_student_marks(student_id)
        if not marks:
            return "No academic record found for your student ID."

        return format_marks_answer(marks)

    # 🌍 General question → RAG
    return get_answer(question)




    








