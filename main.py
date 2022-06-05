from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api.exceptions import VkApiError

from random import randint

from database import DataBase
from keyboards import KeyBoards
from states import States
import data


class Handlers:
    def __init__(self, token: str, group_id: int) -> None:
        """Initialization"""
        self.vk_session = VkApi(token=token)
        self.bot_long_poll = VkBotLongPoll(vk=self.vk_session, group_id=group_id)
        self.database = DataBase()

    def s_nothing_handler(self, user_id: int, message: str) -> None:
        """Handling States.S_NOTHING"""
        if message == "Найти класс":
            self.send_message(user_id, "Нахожу класс...",
                              self.get_keyboard("menu"))

        elif message == "Создать класс":
            self.send_message(user_id, "Напишите название будущего класса:",
                              self.get_keyboard("cancel_back"))
            self.database.set_user_dialog_state(user_id, States.S_ENTER_NAME_CLASSCREATE.value)

        elif message == "Мои классы":
            self.send_message(user_id, "Твои классы...",
                              self.get_keyboard("menu"))

        elif message == "Создать беседу класса":
            self.send_message(user_id, "Создаю беседу класса...",
                              self.get_keyboard("menu"))

        elif message == "Настройка беседы класса":
            self.send_message(user_id, "Настройка беседы класса...",
                              self.get_keyboard("menu"))

        elif message == "Обращение в тех. поддержку":
            self.send_message(user_id, "Вопрос принят...",
                              self.get_keyboard("menu"))

        else:
            self.send_message(user_id, "Я бот и общаться пока что не умею :(",
                              self.get_keyboard("menu"))

    def s_enter_name_class_create_handler(self, user_id: int, message: str) -> None:
        """Handling States.S_ENTER_NAME_CLASSCREATE"""
        if message == "Отменить":
            self.database.set_user_dialog_state(user_id, States.S_NOTHING.value)
            self.send_message(user_id, "Создание класса отменено",
                              self.get_keyboard("menu"))

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

    @staticmethod
    def get_keyboard(keyboard_type: str) -> VkKeyboard:
        """Get the keyboard"""
        if keyboard_type == "empty":
            return KeyBoards.KEYBOARD_EMPTY.get_empty_keyboard()

        elif keyboard_type == "menu":
            return KeyBoards.KEYBOARD_MENU.get_keyboard()

        elif keyboard_type == "cancel_back":
            return KeyBoards.KEYBOARD_CANCEL_BACK.get_keyboard()


class DiaryVkBot(Handlers):
    def __init__(self, token: str, group_id: int, database: DataBase) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id)
        self.database = database

    def listen(self) -> None:
        """Listening events"""
        for event in self.bot_long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_user:
                    user_id = event.object.message["from_id"]  # Getting user_id
                    message = event.object.message["text"]  # Getting message's text
                    user_information = self.get_user_info(user_id)  # User_id, first_name, nickname

                    self.database.insert_new_user(user_information["user_id"],
                                                  user_information["screen_name"],
                                                  user_information["first_name"],
                                                  False
                                                  )  # Will add a new user if user writes his first message

                    if self.is_member(user_id):  # Checking first condition

                        if self.database.check_user_is_ready(user_id):  # Checking second condition
                            current_dialog_state = self.database.get_user_dialog_state(user_id)
                            self.filter_dialog_state(user_id, message, current_dialog_state)
                        else:
                            self.database.set_user_is_ready(user_id)  # First condition is True but this is a first user's message
                            self.send_message(user_id, "Добро пожаловать в наше сообщество!\n"
                                                       "Что может наш бот? (Инструкция)",
                                              self.get_keyboard("menu"))
                    else:
                        self.send_message(user_id,  # User is not a member
                                          "Перед использованием бота подпишись на группу!",
                                          self.get_keyboard("empty"))
            else:
                print(event)

    def filter_dialog_state(self, user_id: int, message: str, current_dialog_state: int) -> None:
        """Filtering dialog states"""
        match current_dialog_state:
            case States.S_NOTHING.value:
                super().s_nothing_handler(user_id, message)

            case States.S_ENTER_NAME_CLASSCREATE.value:
                super().s_enter_name_class_create_handler(user_id, message)

    @staticmethod
    def get_keyboard(keyboard_type: str) -> VkKeyboard:
        """Get the keyboard"""
        if keyboard_type == "empty":
            return KeyBoards.KEYBOARD_EMPTY.get_empty_keyboard()

        elif keyboard_type == "menu":
            return KeyBoards.KEYBOARD_MENU.get_keyboard()

        elif keyboard_type == "cancel_back":
            return KeyBoards.KEYBOARD_CANCEL_BACK.get_keyboard()

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
    my_bot = DiaryVkBot(token=data.TOKEN, group_id=data.GROUP_ID, database=database)

    my_bot.listen()
