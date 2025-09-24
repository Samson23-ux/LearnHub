import copy, string, secrets
from app.schemas.users import Account, AccountCreate, AccountUpdate
from app.schemas.users import PasswordUpdate, AccountSignIn
from app.core.utils import read_json, write_json
from app.services.errors import UserNotFoundError, UserExistError
from app.services.errors import PasswordError, EmailError
from app.core.utils import hash_password

class AccountService:
    def generate_token(self) -> str:
        token = ''
        char = string.ascii_letters + string.digits
        for _ in range(9):
            token += secrets.choice(char)
        return token

    def is_user_exist(self, email: str, users: list[dict]) -> bool:
        for user in users:
            email = email.lower().strip()
            if email == user['email'].lower().strip():
                return True
        return False

    def get_acc_by_id(self, acc_id: str, users: list[dict]) -> dict:
        for user in users:
            if user['id'] == acc_id:
                return user
        raise UserNotFoundError('User not found!')

    async def get_accounts(self, role: str | None = None) -> list[dict]:
        users = await read_json('users.json')
        if role:
            users = [usr for usr in users if usr['role'] == role]

        if not users:
            raise UserNotFoundError('User not found!')

        accounts = copy.deepcopy(users)

        for acc in accounts:
            del acc['password']
        return accounts

    async def get_account(self, username: str) -> dict:
        users = await read_json('users.json')
        for user in users:
            username = username.lower().strip()
            if user['username'] == username:
                account = user.copy()
                del account['password']
                return account
        raise UserNotFoundError('User not found!')

    async def create_account(self, account: AccountCreate) -> dict:
        users = await read_json('users.json')

        acc = Account(
            **account.model_dump(),
            id=str(len(users) + 1)
        )
        acc.password = hash_password(acc.password)

        if self.is_user_exist(acc.email, users):
            raise UserExistError('User already exist!')

        users.append(acc.model_dump())
        await write_json('users.json', users)

        user = self.get_acc_by_id(acc.id, users)
        user_acc = user.copy()
        del user_acc['password']

        return user_acc

    async def sign_in(self, acc_id: str, account: AccountSignIn) -> dict:
        users = await read_json('users.json')
        user = self.get_acc_by_id(acc_id, users)

        email = account.email.lower().strip()
        if email != user['email'].lower().strip():
            raise EmailError('Invalid email!')

        if hash_password(account.password) != user['password']:
            raise PasswordError('Incorrect Password!')

        user['token'] = self.generate_token()
        user_acc = user.copy()
        del user_acc['password']

        await write_json('users.json', users)

        return user_acc

    async def sign_out(self, acc_id: str) -> dict:
        users = await read_json('users.json')
        user = self.get_acc_by_id(acc_id, users)

        del user['token']

        user_acc = user.copy()
        del user_acc['password']

        await write_json('users.json', users)

        return user_acc

    async def update_account(self, acc_id: str, account_update: AccountUpdate) -> dict:
        users = await read_json('users.json')
        user_acc = self.get_acc_by_id(acc_id, users)

        if hash_password(account_update.curr_password) != user_acc['password']:
            raise PasswordError('Incorrect password!')

        if account_update.username is not None:
            usrs = [usr for usr in users if usr['username'] != user_acc['username']]
            if self.is_user_exist(account_update.username, usrs):
                raise UserExistError('Username already exist!')

        acc_update = account_update.model_dump(exclude_unset=True, exclude={'curr_password'})

        for key, value in acc_update.items():
            for k, _ in user_acc.items():
                if key == k:
                    user_acc[key] = value

        await write_json('users.json', users)

        account = user_acc.copy()
        del account['password']

        return account

    async def update_password(self, acc_id: str, password_update: PasswordUpdate) -> dict:
        users = await read_json('users.json')
        user_acc = self.get_acc_by_id(acc_id, users)

        if hash_password(password_update.curr_password) != user_acc['password']:
            raise PasswordError('Incorrect password')

        user_acc['password'] = hash_password(password_update.new_password)

        await write_json('users.json', users)

        account = user_acc.copy()
        del account['password']

        return account

account_service = AccountService()
