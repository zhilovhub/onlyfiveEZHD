from only_five_cdz.decryptor_answers import get_answers_text
from only_five_cdz.config import *


class Handlers:
    def __init__(self, bot: Bot) -> None:
        """Initialization"""
        self.auth_data = None
        self.bot = bot

    async def set_auth_data(self) -> None:
        """Sets auth data"""
        url = 'https://uchebnik.mos.ru/api/sessions/demo'
        data = {"login": "", "password_hash2": ""}
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json; charset=UTF-8"
        }

        print(1)
        async with aiohttp.ClientSession(headers=headers) as session:
            print(2)
            async with session.post(url, data=dumps(data)) as response:
                print(3)
                self.auth_data = await response.json()
                print(4)

    async def is_member(self, user_id: int) -> int:
        """Check if user is member"""
        try:
            is_member = await self.bot.api.groups.is_member(group_id=GROUP_ID_CDZ, user_id=user_id)
            return is_member.value
        except Exception as e:
            print(e)

    async def send_message(self, user_id: int, message_text: str) -> None:
        """Sends messages"""
        try:
            await self.bot.api.messages.send(
                user_id=user_id,
                message=message_text,
                random_id=randint(0, 2147483648)
            )
        except Exception as e:
            print(e)

    async def handler(self, user_id: int, url: str) -> None:
        """handling url"""
        try:
            if "uchebnik.mos.ru" in url:
                parsed_answers = await self.parse_answers(url)
                answers_text = get_answers_text(parsed_answers)
                await self.send_message(user_id, answers_text)
            else:
                await self.send_message(user_id, "Ты должен отправить ссылку на мэш-тест")

        except Exception as e:
            await self.send_message(user_id, "Произошла какая-то ошибка. Информация подана администратору")
            await self.send_message(ADMIN_ID, str(e) + " " + str(user_id))

    async def parse_answers(self, url: str) -> list:
        """Parses answers"""
        def get_type(url: str) -> str:
            """Returns type of the test"""
            if 'homework' in url:
                return 'homework'

            return 'spec'

        def get_variant(url: str) -> str:
            """Returns variant of the test"""
            separated_url = url.split("/")
            if 'test_by_binding' in separated_url:
                return separated_url[separated_url.index('test_by_binding') + 1]
            elif 'homework' in separated_url:
                return separated_url[separated_url.index('homework') + 1].split("?")[0]
            elif "training_spec" in separated_url:
                return separated_url[separated_url.index("training_spec") + 1]

        parse_url = 'https://uchebnik.mos.ru/exam/rest/secure/testplayer/group'

        request_data = {
            'test_type': 'training_test',
            'generation_context_type': get_type(url=url),
            'generation_by_id': get_variant(url=url)
        }

        request_cookies = {
            'auth_token': self.auth_data['authentication_token'],
            'profile_id': str(self.auth_data['id']),
            'udacl': 'resh'
        }

        headers = {"Content-type": "application/json"}

        async with aiohttp.ClientSession(headers=headers, cookies=request_cookies) as session:
            async with session.post(parse_url, data=dumps(request_data)) as response:
                parsed_answers = await response.json()

        return parsed_answers
