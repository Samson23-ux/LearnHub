from app.core.utils import read_json, write_json
from app.schemas.enrolments import Enrol, EnrolCreate
from app.services.errors import EnrolmentNotFoundError, EnrolmentExistError

class EnrolService:
    def is_enrol_exist(self, student: str, course: str, enrols: list[dict]) -> bool:
        for enr in enrols:
            name = student.lower().strip()
            course = course.lower().strip()
            if name == enr['student'].lower().strip():
                if course == enr['course_title'].lower().strip():
                    return True
        return False

    async def get_enrolment_by_id(self, enrol_id: str, enrols: list[dict]) -> dict:
        for enr in enrols:
            if enr['id'] == enrol_id:
                return enr
        raise EnrolmentNotFoundError('Enrolment not found!')

    async def create_enrolments(self, enrol_create: EnrolCreate) -> dict:
        enrolments = await read_json('enrolments.json')

        enrol = Enrol(
            **enrol_create.model_dump(),
            id=str(len(enrolments) + 1)
        )

        if self.is_enrol_exist(enrol.student, enrol.course_title, enrolments):
            raise EnrolmentExistError('User already enrolled!')

        enrolments.append(enrol.model_dump())

        await write_json('enrolments.json', enrolments)

        enrolment = await self.get_enrolment_by_id(enrol.id, enrolments)

        return enrolment

    async def get_enrolments(self, instructor: str) -> list[dict]:
        enrolments = await read_json('enrolments.json')

        enrols = []

        for enrol in enrolments:
            instructor = instructor.lower().strip()
            if instructor == enrol['course_instructor'].lower().strip():
                enrols.append(enrol)

        if not enrols:
            raise EnrolmentNotFoundError('Enrolment not found!')

        return enrols

    async def get_student_enrolments(self, student: str) -> list[dict]:
        enrolments = await read_json('enrolments.json')

        enrols = []

        for enrol in enrolments:
            student = student.lower().strip()
            if student == enrol['student'].lower().strip():
                enrols.append(enrol)

        if not enrols:
            raise EnrolmentNotFoundError('Enrolment not found!')

        return enrols

    async def delete_enrolment(self, enrol_id: str):
        enrolments = await read_json('enrolments.json')

        enrolment = await self.get_enrolment_by_id(enrol_id, enrolments)

        enrolments.remove(enrolment)

        await write_json('enrolments.json', enrolments)

enrol_service = EnrolService()
