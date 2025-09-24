from app.services.errors import UserNotFoundError, PasswordError
from app.core.utils import read_json, write_json
from app.core.utils import hash_password

class AdminService:
    def get_acc_by_id(self, acc_id: str, users: list[dict]) -> dict:
        for user in users:
            if user['id'] == acc_id:
                return user
        raise UserNotFoundError('User not found!')

    async def get_stats(
            self,
            users: str | None = None,
            courses: str | None = None,
            enrolments: str | None = None
    ) -> dict[str, list]:
        list_users = await read_json('users.json')
        list_courses = await read_json('courses.json')
        list_enrolments = await read_json('enrolments.json')

        stats = {}

        if users is None and courses is None and enrolments is None:
            stats.update({
                'users': list_users,
                'courses': list_courses,
                'enrolments': list_enrolments
            })
        else:
            if users is not None:
                stats['users'] = list_users
            if courses is not None:
                stats['courses'] = list_courses
            if enrolments is not None:
                stats['enrolments'] = list_enrolments

        return stats

    async def delete_account(self, user: dict, acc_id: str, curr_password: str):
        users = await read_json('users.json')
        user_acc = self.get_acc_by_id(acc_id, users)

        if hash_password(curr_password) != user['password']:
            raise PasswordError('Incorrect password')

        users.remove(user_acc)

        await write_json('users.json', users)

admin_service = AdminService()
