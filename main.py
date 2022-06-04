from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent
from vk_api.keyboard import VkKeyboard
from vk_api.exceptions import VkApiError

from random import randint

from database import DataBase
from keyboards import KeyBoards
from states import States
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
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_user:
                    user_id = event.object.message["from_id"]
                    user_information = self.get_user_info(user_id)

                    self.database.insert_new_user(user_information["user_id"],
                                                  user_information["screen_name"],
                                                  user_information["first_name"],
                                                  False
                                                  )

                    if self.is_member(user_id):
                        if self.database.check_user_is_ready(user_id):
                            if self.database.get_user_dialog_state(user_id) == States.S_NOTHING.value:
                                self.filter_message(event, user_id)
                        else:
                            self.database.set_user_is_ready(user_id)
                            self.send_message(user_id, "Добро пожаловать в наше сообщество!\n"
                                                       "Что может наш бот? (Инструкция)",
                                              self.get_keyboard("menu"))

                    else:
                        self.send_message(event.object.message["from_id"],
                                          "Перед использованием бота подпишись на группу!",
                                          self.get_keyboard("empty"))

            else:
                print(event)

    def filter_message(self, event: VkBotMessageEvent, user_id: int) -> None:
        """Filtering messages"""
        if event.object.message["text"] == "Найти класс":
            self.send_message(event.object.message["from_id"], "Нахожу класс...",
                              self.get_keyboard("menu"))

        elif event.object.message["text"] == "Создать класс":
            self.send_message(event.object.message["from_id"], "Напишите название будущего класса:",
                              self.get_keyboard("empty"))
            self.database.set_user_dialog_state(user_id, States.S_ENTER_NAME_CLASSCREATE.value)

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

    def get_keyboard(self, keyboard_type: str) -> VkKeyboard:
        """Get the keyboard"""
        if keyboard_type == "empty":
            return KeyBoards.KEYBOARD_EMPTY.get_empty_keyboard()

        elif keyboard_type == "menu":
            return KeyBoards.KEYBOARD_MENU.get_keyboard()

    def send_message(self, user_id: int, message: str, keyboard: VkKeyboard) -> None:
        """Send message to user"""
        try:
            self.vk_session.method(
                "messages.send",
                {
                    "user_id": user_id,
                    "message": message,
                    "keyboard": keyboard,
                    "random_id": randint(0, 2 ** 10)
                }
            )
        except VkApiError as e:
            print(e)

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

    def get_user_info(self, user_id: int) -> dict:
        """Get information about user"""
        user_information = self.vk_session.method(
            "users.get",
            {
                "user_ids": user_id,
                "fields": "screen_name"
            }
        )[0]

        return {
            "user_id": user_id,
            "screen_name": user_information["screen_name"],
            "first_name": user_information["first_name"]
        }


if __name__ == "__main__":
    database = DataBase()

    my_bot = DiaryVkBot(token=data.TOKEN, database=database)
    my_bot.listen()
