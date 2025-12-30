# import os
# from dotenv import load_dotenv
# load_dotenv()

# from langchain_groq import ChatGroq
# from studdata import STUDENTS


# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # --------------------------------------------------
# # LLM
# # --------------------------------------------------
# client = ChatGroq(
#     temperature=0,
#     groq_api_key=GROQ_API_KEY,
#     model_name="llama-3.1-8b-instant",
# )

# # --------------------------------------------------
# # EMBEDDINGS
# # --------------------------------------------------


# def ask_about_student(question, student_id):
#     student = next(
#         (s for s in STUDENTS if s["student_id"] == student_id),
#         None
#     )

#     if not student:
#         return {"answer": "I don't have that information. Please contact the admin."}

#     prompt = f"""
#         You are a student support assistant.
#         Answer ONLY using the data below.
#         If info is missing, say:
#         "I don't have that information. Please contact the admin."

#     STUDENT DATA:
#     {STUDENTS}

#     USER QUESTION:
#     {question}
#     """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "system", "content": "Never hallucinate. Use only given data."},
#             {"role": "user", "content": prompt}
#         ]
#     )

#     return {"answer": response.choices[0].message.content}



import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from studdata import STUDENTS

load_dotenv()

# --------------------------------------------------
# LLM
# --------------------------------------------------
llm = ChatGroq(
    temperature=0,
    model="llama-3.1-8b-instant",
)

# --------------------------------------------------
# STUDENT QA FUNCTION
# --------------------------------------------------
def ask_about_student(question: str, student_id: int):

    student = next(
        (s for s in STUDENTS if s["student_id"] == student_id),
        None
    )

    if not student:
        return {
            "answer": "I don't have that information. Please contact the admin."
        }

    prompt = f"""
You are a student support assistant.
Answer ONLY using the student data below.
Never guess or hallucinate.

If the answer is not present, say:
"I don't have that information. Please contact the admin."

STUDENT DATA:
{student}

QUESTION:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }

