import requests

STUDENT_API_URL = "http://92.205.109.210:8051/api/getallmark"




def get_student_marks(student_id: int):
    response = requests.get(STUDENT_API_URL)
    result = response.json()

    data = result.get("data", [])   # 🔥 FIX

    for record in data:
        if record.get("studentId") == student_id:
            return record

    return None


def get_stud():
     response = requests.get(STUDENT_API_URL)
     result = response.json()

     data = result.get("data", [])
     return data


def format_marks_answer(marks):
    if not marks:
        return "Your marks are not available yet. Please contact admin."

    s1 = marks.get("subject1")
    s2 = marks.get("subject2")
    s3 = marks.get("subject3")

    if s1 is None and s2 is None and s3 is None:
        return "Your results are not published yet. Please wait."

    total = (s1 or 0) + (s2 or 0) + (s3 or 0)

    return (
        f"📊 Here are your marks:\n"
        f"• Subject 1: {s1}\n"
        f"• Subject 2: {s2}\n"
        f"• Subject 3: {s3}\n"
        f"👉 Total: {total}\n\n"
        f"Great effort — keep pushing 🚀"
    )
