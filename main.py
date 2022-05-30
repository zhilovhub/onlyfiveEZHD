from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent
from vk_api.keyboard import VkKeyboard

from random import randint

from database import DataBase
from keyboards import KeyBoards
import data


class DiaryVkBot:
    def __init__(self, token: str, database: DataBase) -> None:
        """Initialization"""
        self.vk_session = VkApi(token=token)
        self.bot_long_poll = VkBotLongPoll(vk=self.vk_session, group_id=data.GROUP_ID)
        self.database = database

    def listen(self) -> None:
        """Listening events"""
        for event in self.bot_long_poll.listen():
            print(event)
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_user:
                    if self.is_member(event.object.message["from_id"]):
                        self.filter_message(event)

                    else:
                        self.send_message(event.object.message["from_id"],
                                          "Перед использованием бота подпишись на группу!",
                                          self.get_keyboard("empty"))

            elif event.type == VkBotEventType.GROUP_JOIN:
                self.send_message(event.object.user_id, "Добро пожаловать в наше сообщество!\n"
                                                        "Что может наш бот? (Инструкция)",
                                  self.get_keyboard("menu"))

            else:
                print(event)

    def filter_message(self, event: VkBotMessageEvent) -> None:
        """Filtering messages"""
        if event.object.message["text"] == "Найти класс":
            self.send_message(event.object.message["from_id"], "Нахожу класс...",
                              self.get_keyboard("menu"))

        elif event.object.message["text"] == "Создать класс":
            self.send_message(event.object.message["from_id"], "Создаю класс...",
                              self.get_keyboard("menu"))

        elif event.object.message["text"] == "Мои классы":
            self.send_message(event.object.message["from_id"], "Твои классы...",
                              self.get_keyboard("menu"))

        elif event.object.message["text"] == "Создать беседу класса":
            self.send_message(event.object.message["from_id"], "Создаю беседу класса...",
                              self.get_keyboard("menu"))

        elif event.object.message["text"] == "Настройка беседы класса":
            self.send_message(event.object.message["from_id"], "Настройка беседы класса...",
                              self.get_keyboard("menu"))

        elif event.object.message["text"] == "Обращение в тех. поддержку":
            self.send_message(event.object.message["from_id"], "Вопрос принят...",
                              self.get_keyboard("menu"))

        else:
            self.send_message(event.object.message["from_id"], "Я бот и общаться пока что не умею :(",
                              self.get_keyboard("menu"))

    def send_message(self, user_id: int, message: str, keyboard: VkKeyboard) -> None:
        """Send message to user"""
        self.vk_session.method(
            "messages.send",
            {
                "user_id": user_id,
                "message": message,
                "keyboard": keyboard,
                "random_id": randint(0, 2 ** 10)
            }
        )

    def get_keyboard(self, keyboard_type: str) -> VkKeyboard:
        """Get the keyboard"""
        if keyboard_type == "empty":
            return KeyBoards.KEYBOARD_EMPTY.get_empty_keyboard()

        elif keyboard_type == "menu":
            return KeyBoards.KEYBOARD_MENU.get_keyboard()

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


if __name__ == "__main__":
    database = DataBase()

    my_bot = DiaryVkBot(token=data.TOKEN, database=database)
    my_bot.listen()
