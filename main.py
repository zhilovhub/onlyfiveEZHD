import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from random import randint

import data


class DiaryVkBot:
    def __init__(self, token: str) -> None:
        """Initialization"""
        self.vk_session = vk_api.VkApi(token=token)
        self.bot_long_poll = VkBotLongPoll(vk=self.vk_session, group_id=data.GROUP_ID)

    def send_message(self, user_id: int, message: str) -> None:
        """Send message to user"""
        self.vk_session.method(
            "messages.send",
            {
                "user_id": user_id,
                "message": message,
                "random_id": randint(0, 2 ** 10)
            }
        )

    def is_member(self, user_id: int) -> int:
        """Check is user member of the group"""
        is_member = self.vk_session.method(
            "groups.isMember",
            {
                "group_id": data.GROUP_ID,
                "user_id": user_id
            }
        )

        return is_member

    def listen(self) -> None:
        """Listening events"""
        for event in self.bot_long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_user:
                    if self.is_member(user_id=event.object.message["from_id"]):
                        self.send_message(user_id=event.object.message["from_id"], message=event.object.message["text"])
                    else:
                        self.send_message(user_id=event.object.message["from_id"], message="Перед использованием бота подпишись на группу!")

            elif event.type == VkBotEventType.GROUP_JOIN:
                self.send_message(user_id=event.object.user_id, message="Добро пожаловать в наше сообщество!\n"
                                                                        "Что может наш бот? (Инструкция)")

            else:
                print(event.type)


if __name__ == "__main__":
    my_bot = DiaryVkBot(token=data.TOKEN)
    my_bot.listen()
