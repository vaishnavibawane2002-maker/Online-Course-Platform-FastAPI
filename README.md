# 🚀 Online Course Platform (FastAPI Project)

## 📌 Project Overview
The **Advanced Online Course Platform** is a backend system built using FastAPI.  
It allows users to manage courses, enroll students, track progress, and perform advanced operations like search, filtering, sorting, and pagination.

## 🎯 Key Features

### 📚 Course Management
- Add new courses
- Update course details
- Delete courses
- View all courses
- Get course by ID

### 👩‍🎓 Student Enrollment
- Enroll students into courses
- Prevent duplicate or invalid enrollments
- Block enrollment for inactive courses

### 📊 Progress Tracking
- Update student progress
- Track learning completion

### 🔍 Advanced Functionalities
- Search courses by keyword
- Filter courses by category & price
- Sort courses (ascending/descending)
- Pagination support
- Combined browsing (search + pagination)

### 📈 Statistics
- Total courses
- Active / inactive courses
- Enrollment count

## 🛠️ Technologies Used
- Python
- FastAPI
- Pydantic
- Uvicorn



## 📂 Project Structure


fastapi_online_course_platform

 - main.py
 - requirements.txt
 - screenshots
 - README.md

## ▶️ How to Run the Project

### Step 1: Install dependencies

pip install -r requirements.txt


### Step 2: Run the server

uvicorn main:app --reload


## 🌐 API Documentation

After running the server, open:

👉 Swagger UI:

http://127.0.0.1:8000/docs
