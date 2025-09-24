from fastapi import FastAPI
from app.middleware import LogRequestMiddleware
from app.routers import auth, users, courses, enrolments, admin
from app.services.errors import UserExistError, EmailError
from app.services.errors import PasswordError, UserNotFoundError
from app.services.errors import CourseExistError, CourseNotFoundError
from app.services.errors import EnrolmentExistError, EnrolmentNotFoundError
from app.services.errors import enrolment_not_found_handler, enrolment_exist_handler
from app.services.errors import user_exist_handler, invalid_email_handler, invalid_password_handler
from app.services.errors import user_not_found_handler, course_exist_handler, course_not_found_handler

app = FastAPI(title='LearnHub')

#middleware
app.add_middleware(LogRequestMiddleware)

#routers
app.include_router(auth.router, prefix='/auth', tags=['Auth'])
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(courses.router, prefix='/courses', tags=['Courses'])
app.include_router(enrolments.router, prefix='/courses', tags=['Enrolments'])
app.include_router(admin.router, prefix='/admin', tags=['Admin'])

#exception handlers
app.add_exception_handler(UserExistError, user_exist_handler)
app.add_exception_handler(EmailError, invalid_email_handler)
app.add_exception_handler(PasswordError, invalid_password_handler)
app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(CourseNotFoundError, course_not_found_handler)
app.add_exception_handler(CourseExistError, course_exist_handler)
app.add_exception_handler(EnrolmentNotFoundError, enrolment_not_found_handler)
app.add_exception_handler(EnrolmentExistError, enrolment_exist_handler)
