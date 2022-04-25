import vk_api
from random import randint

import data


class DiaryVkBot:
    def __init__(self, token: str) -> None:
        """Initialization"""
        self.vk_session = vk_api.VkApi(token=token)

    def send_message(self, user_id: int, message: str) -> None:
        """Send message to user"""
        self.vk_session.method(
            "messages.send",
            {
                "user_id": user_id,
                "message": message,
                "random_id": randint(0, 2 ** 32)
            }
        )


if __name__ == "__main__":
    my_bot = DiaryVkBot(token=data.TOKEN)
    my_bot.send_message(user_id=data.ADMIN_ID, message="I am working")
