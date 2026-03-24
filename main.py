from fastapi import FastAPI, Query, Response
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI()

# ------------------ DATA ------------------

courses = [
    {"id": 1, "title": "Python Basics", "category": "Programming", "price": 1000, "is_active": True},
    {"id": 2, "title": "Data Science", "category": "Data", "price": 2000, "is_active": True},
    {"id": 3, "title": "Web Development", "category": "Programming", "price": 1500, "is_active": False},
    {"id": 4, "title": "Machine Learning", "category": "AI", "price": 3000, "is_active": True},
    {"id": 5, "title": "Deep Learning", "category": "AI", "price": 3500, "is_active": True},
    {"id": 6, "title": "SQL Mastery", "category": "Database", "price": 1200, "is_active": True},
    {"id": 7, "title": "Excel for Data Analysis", "category": "Data", "price": 800, "is_active": True},
    {"id": 8, "title": "Power BI Dashboard", "category": "Data", "price": 1800, "is_active": True},
]

enrollments = []
course_counter = 9
enroll_counter = 1

# ------------------ DAY 1 ------------------

@app.get("/")
def home():
    return {"message": "Welcome to Advanced Online Course Platform"}

@app.get("/courses")
def get_courses():
    return {"total": len(courses), "courses": courses}

@app.get("/courses/summary")
def summary():
    active = [c for c in courses if c["is_active"]]
    return {
        "total": len(courses),
        "active": len(active),
        "inactive": len(courses) - len(active)
    }


# ------------------ DAY 2 ------------------

class EnrollRequest(BaseModel):
    student_name: str = Field(..., min_length=2)
    course_id: int = Field(..., gt=0)

class CourseModel(BaseModel):
    title: str
    category: str
    price: int
    is_active: bool = True

# ------------------ DAY 3 ------------------

def find_course(course_id):
    return next((c for c in courses if c["id"] == course_id), None)

def is_duplicate(title):
    return any(c["title"].lower() == title.lower() for c in courses)

# ------------------ ENROLL ------------------

@app.post("/enroll")
def enroll(req: EnrollRequest):
    global enroll_counter

    course = find_course(req.course_id)

    if not course:
        return {"error": "Course not found"}

    if not course["is_active"]:
        return {"error": "Course inactive"}

    record = {
        "enroll_id": enroll_counter,
        "student_name": req.student_name,
        "course_id": req.course_id,
        "progress": 0,
        "date": str(datetime.now())
    }

    enrollments.append(record)
    enroll_counter += 1

    return record

# ------------------ DAY 4 CRUD ------------------

@app.post("/courses")
def add_course(course: CourseModel, response: Response):
    global course_counter

    if is_duplicate(course.title):
        return {"error": "Duplicate course"}

    new_course = {"id": course_counter, **course.dict()}
    courses.append(new_course)
    course_counter += 1

    response.status_code = 201
    return new_course

@app.put("/courses/{course_id}")
def update_course(course_id: int, price: Optional[int] = None, is_active: Optional[bool] = None):
    course = find_course(course_id)

    if not course:
        return {"error": "Not found"}

    if price:
        course["price"] = price
    if is_active is not None:
        course["is_active"] = is_active

    return course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    course = find_course(course_id)

    if not course:
        return {"error": "Not found"}

    courses.remove(course)
    return {"message": "Deleted successfully"}

# ------------------ DAY 5 WORKFLOW ------------------

@app.post("/progress/{enroll_id}")
def update_progress(enroll_id: int, progress: int):
    for e in enrollments:
        if e["enroll_id"] == enroll_id:
            e["progress"] = progress
            return e
    return {"error": "Enrollment not found"}

@app.get("/enrollments")
def get_enrollments():
    return {"total": len(enrollments), "data": enrollments}

# ------------------ EXTRA WORKFLOW ------------------

@app.get("/student/{name}")
def get_student_courses(name: str):
    data = [e for e in enrollments if e["student_name"].lower() == name.lower()]
    return {"courses": data}

# ------------------ DAY 6 ADVANCED ------------------

@app.get("/courses/search")
def search(keyword: Optional[str] = None):
    if not keyword:
        return {"message": "Provide keyword"}

    result = [c for c in courses if keyword.lower() in c["title"].lower()]
    return {"count": len(result), "results": result}



@app.get("/courses/filter")
def filter_courses(category: Optional[str] = None, max_price: Optional[int] = None):
    data = courses

    if category:
        data = [c for c in data if c["category"].lower() == category.lower()]

    if max_price:
        data = [c for c in data if c["price"] <= max_price]

    return {"count": len(data), "data": data}

@app.get("/courses/sort")
def sort_courses(sort_by: str = "price", order: str = "asc"):
    sorted_data = sorted(courses, key=lambda x: x[sort_by])

    if order == "desc":
        sorted_data.reverse()

    return sorted_data

@app.get("/courses/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return courses[start:start + limit]

@app.get("/courses/browse")
def browse(keyword: Optional[str] = None, page: int = 1, limit: int = 3):
    data = courses

    if keyword:
        data = [c for c in data if keyword.lower() in c["title"].lower()]

    start = (page - 1) * limit
    return data[start:start + limit]

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for c in courses:
        if c["id"] == course_id:
            return c
    return {"error": "Course not found"}
# ------------------ STATS ------------------

@app.get("/stats")
def stats():
    total_revenue = sum(c["price"] for c in courses)
    return {
        "total_courses": len(courses),
        "total_enrollments": len(enrollments),
        "total_revenue": total_revenue
    }