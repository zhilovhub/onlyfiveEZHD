import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from random import randint

import data


class DiaryVkBot:
    def __init__(self, token: str) -> None:
        """Initialization"""
        self.vk_session = vk_api.VkApi(token=token)
        self.long_poll = VkLongPoll(vk=self.vk_session)

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
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.from_user:
                    if event.to_me:
                        if self.is_member(user_id=event.user_id):
                            pass
                        else:
                            self.send_message(user_id=event.user_id, message="Перед использованием бота подпишись на группу!")


if __name__ == "__main__":
    my_bot = DiaryVkBot(token=data.TOKEN)
    my_bot.listen()
