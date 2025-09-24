# 🛠 Project Description

## FastAPI application where users can enrol for a course and manage enrolled courses.

### Admin

* Manages courses, instructors and students
* Can delete a user

### Instructor

* Create a course
* Update created courses
* Delete created courses
* Get a list of students enrolled for created courses

### Students

* Enrol for a course
* Get a list of courses enrolled for
* Cancel enrollments

![Static Badge](https://img.shields.io/badge/FastAPI-0.116.1-green?color=%23006400)
![Static Badge](https://img.shields.io/badge/Python-3.13-green?color=%23006400)

# 🧾 Steps to run and test endpoints

## 1. Clone repo

```shell
git clone https://github.com/Samson23-ux/LearnHub.git
```

## 2. Create enviroment

```shell
python -m venv venv
```

## 3. Activate enviroment

```shell
venv\Scripts\activate or source venv/bin/activate (for apple)
```

## 4. Run Server

```shell
uvicorn app.main:main --reload
```

## 5. Test Endpoints

```shell
run http://localhost:8000/docs on browser
```
