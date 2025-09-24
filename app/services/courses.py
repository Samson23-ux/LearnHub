from app.schemas.courses import Course, CourseCreate, CourseUpdate
from app.core.utils import read_json, write_json
from app.services.errors import CourseExistError, CourseNotFoundError

class CourseService:
    def is_course_exist(self, title: str, courses: list[dict]) -> bool:
        for course in courses:
            title = title.lower().strip()
            if title == course['title'].lower().strip():
                return True
        return False

    def get_course_by_id(self, course_id: str, courses: list[dict]) -> dict:
        for course in courses:
            if course['id'] == course_id:
                return course
        raise CourseNotFoundError('Course not found!')

    async def create_course(self, course_create: CourseCreate) -> dict:
        courses = await read_json('courses.json')

        course =  Course(
            id=str(len(courses) + 1),
            **course_create.model_dump()
        )

        if self.is_course_exist(course_create.title, courses):
            raise CourseExistError('Course already exist!')

        courses.append(course.model_dump())

        await write_json('courses.json', courses)

        user_course = self.get_course_by_id(course.id, courses)
        return user_course

    async def get_courses(self, instructor: str | None = None) -> list[dict]:
        courses = await read_json('courses.json')

        if instructor is not None:
            courses = [course for course in courses if course['instructor'] == instructor]

        if not courses:
            raise CourseNotFoundError('Course not found!')

        return courses

    async def get_course(self, title: str) -> dict:
        courses = await read_json('courses.json')

        for course in courses:
            title = title.lower().strip()
            if title == course['title'].lower().strip():
                return course
        raise CourseNotFoundError('Course not found!')

    async def update_course(self, course_id: str, course_update: CourseUpdate) -> dict:
        courses = await read_json('courses.json')
        user_course = self.get_course_by_id(course_id, courses)

        if course_update.title is not None:
            if self.is_course_exist(course_update.title, courses):
                raise CourseExistError('Course already exist!')

        course = course_update.model_dump(exclude_unset=True)

        for key, value in course.items():
            for k, _ in user_course.items():
                if key == k:
                    user_course[k] = value

        await write_json('courses.json', courses)

        return user_course

    async def delete_course(self, course_id: str):
        courses = await read_json('courses.json')
        user_course = self.get_course_by_id(course_id, courses)

        courses.remove(user_course)

        await write_json('courses.json', courses)


course_service = CourseService()
