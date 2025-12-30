# main.py

from fastapi import FastAPI
from agents import chatbot_agent
from typing import Optional 
from rag.studrag import ask_about_student

from stud_service import get_student_marks,get_stud

app = FastAPI()

@app.get("/")
def welcomepage():
 return{'data':'welcome'}

@app.post("/chat")
def chat(question: str, student_id: Optional[int] = None):
    answer = chatbot_agent(question, student_id)
    return {"answer": answer}

@app.get("/getallstud")
def getllstude():
   return get_stud()


@app.post("/studbot")
def studentBot(question:str, student_id:int):
   answer=ask_about_student(question,student_id)
   return answer
   



def is_personal_query(question: str) -> bool:
    keywords = ["my", "mine", "i", "me"]
    academic_terms = [
        "marks", "score", "result", "attendance",
        "fees", "payment", "progress", "remarks"
    ]

    q = question.lower()

    return (
        any(k in q for k in keywords)
        and any(t in q for t in academic_terms)
    )

@app.post("/studbot/withrag")
def studentBot(
    question: str,
    student_id: Optional[int] = None
):
    # 1️⃣ Personal question but NOT logged in
    if is_personal_query(question) and not student_id:
        return {
            "answer": "Please log in to access your personal academic details."
        }

    # 2️⃣ Personal question + logged in
    if is_personal_query(question) and student_id:
        return ask_about_student(question, student_id)

    # 3️⃣ General institute question → RAG
    answer = chatbot_agent(question)
    return {"answer": answer}





