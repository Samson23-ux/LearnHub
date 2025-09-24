from fastapi import Request
from fastapi.responses import JSONResponse

#errors
class UserExistError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class PasswordError(Exception):
    pass

class EmailError(Exception):
    pass

class CourseExistError(Exception):
    pass

class CourseNotFoundError(Exception):
    pass

class EnrolmentNotFoundError(Exception):
    pass

class EnrolmentExistError(Exception):
    pass


#handlers
def user_exist_handler(request: Request, exc: UserExistError):
    return JSONResponse(
        status_code=400,
        content='User already exist!'
)

def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content='User not Found!'
)

def invalid_email_handler(request: Request, exc: EmailError):
    return JSONResponse(
        status_code=400,
        content='Invalid email!'
)

def invalid_password_handler(request: Request, exc: PasswordError):
    return JSONResponse(
        status_code=400,
        content='Invalid password!'
)

def course_exist_handler(request: Request, exc: CourseExistError):
    return JSONResponse(
        status_code=400,
        content='Course already exist!'
)

def course_not_found_handler(request: Request, exc: CourseNotFoundError):
    return JSONResponse(
        status_code=404,
        content='Course not Found!'
)

def enrolment_not_found_handler(request: Request, exc: EnrolmentNotFoundError):
    return JSONResponse(
        status_code=404,
        content='Enrolment not Found!'
)

def enrolment_exist_handler(request: Request, exc: EnrolmentExistError):
    return JSONResponse(
        status_code=400,
        content='User already enrolled!'
)
