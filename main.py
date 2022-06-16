from config import *

from users import UserDataBase
from classroom import ClassroomCommands

from keyboards import KeyBoards
from states import States

from json import loads


class SupportingFunctions:
    def __init__(self, token: str, group_id: int) -> None:
        """Initialization"""
        self.vk_session = VkApi(token=token)
        self.bot_long_poll = VkBotLongPoll(vk=self.vk_session, group_id=group_id)

    def send_message(self, user_id: int, message: str, keyboard=None) -> None:
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

    def send_message_event_answer(self, event_id: str, user_id: int, peer_id: int, event_data: str) -> None:
        """Send message to user after callback-button using"""
        try:
            self.vk_session.method(
                "messages.sendMessageEventAnswer",
                {
                    "event_id": event_id,
                    "user_id": user_id,
                    "peer_id": peer_id,
                    "event_data": event_data
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

        elif keyboard_type == "cancel":
            return KeyBoards.KEYBOARD_CANCEL.get_keyboard()

        elif keyboard_type == "yes_no_cancel_back":
            return KeyBoards.KEYBOARD_YES_NO_CANCEL_BACK.get_keyboard()

        elif keyboard_type == "submit_back":
            return KeyBoards.KEYBOARD_SUBMIT_BACK.get_keyboard()

        elif keyboard_type == "my_class_menu":
            return KeyBoards.KEYBOARD_MY_CLASS_MENU.get_keyboard()

    def is_member(self, user_id: int) -> int:
        """Check is user member of the group"""
        is_member = self.vk_session.method(
            "groups.isMember",
            {
                "group_id": GROUP_ID,
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


class Handlers(SupportingFunctions):
    def __init__(self, token: str, group_id: int, user_db: UserDataBase, classroom_db: ClassroomCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id)
        self.user_db = user_db
        self.classroom_db = classroom_db

    def s_nothing_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_NOTHING"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Найти класс":
            self.send_message(user_id, "Нахожу класс...",
                              self.get_keyboard("menu"))

        elif payload["text"] == "Создать класс":
            classroom_id = self.classroom_db.insert_new_classroom(user_id)
            self.classroom_db.update_user_customize_classroom(user_id, classroom_id)
            self.send_message(user_id, "Напишите название будущего класса (макс. 32 символа):",
                              self.get_keyboard("cancel"))

            self.user_db.set_user_dialog_state(user_id, States.S_ENTER_CLASS_NAME_CLASSCREATE.value)

        elif payload["text"] == "Мои классы":
            user_classrooms_dictionary = self.classroom_db.get_user_classrooms_with_role(user_id)

            if not user_classrooms_dictionary:
                self.send_message(user_id, "Пока что ты не состоишь ни в одном классе!", self.get_keyboard("menu"))

            for classroom_id, role in user_classrooms_dictionary.items():
                keyboard = VkKeyboard(inline=True)
                keyboard.add_callback_button("Войти", payload={
                    "type": "enter_the_classroom", "classroom_id": classroom_id
                })

                members_dictionary = self.classroom_db.get_list_of_classroom_users(classroom_id)
                classroom_name, school_name, access, description = \
                    self.classroom_db.get_information_for_creating_classroom(classroom_id)

                self.send_message(user_id, f"#{classroom_id}\n"
                                           f"Класс: {classroom_name}\n"
                                           f"Школа: {school_name}\n"
                                           f"Описание: {description}\n"
                                           f"Могут ли все участники приглашать: {'Да' if access else 'Нет'}\n"
                                           f"Вы: {role}\n"
                                           f"Участники: {len(members_dictionary)}", keyboard.get_keyboard())

        elif payload["text"] == "Создать беседу класса":
            self.send_message(user_id, "Создаю беседу класса...",
                              self.get_keyboard("menu"))

        elif payload["text"] == "Настройка беседы класса":
            self.send_message(user_id, "Настройка беседы класса...",
                              self.get_keyboard("menu"))

        elif payload["text"] == "Обращение в тех. поддержку":
            self.send_message(user_id, "Вопрос принят...",
                              self.get_keyboard("menu"))

    def s_enter_class_name_class_create_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_CLASS_NAME_CLASSCREATE"""
        if payload is None:
            if len(message) > 32:
                self.send_message(user_id, "Длина названия превышает 32 символа. Введите другое название:",
                                  self.get_keyboard("cancel"))
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_classroom_name(classroom_id, message)

                next_state, keyboard_type, messages = States.get_next_state_config(
                    States.S_ENTER_CLASS_NAME_CLASSCREATE)
                self.send_message(user_id, f"Название класса: {message}", self.get_keyboard("empty"))

                self.state_transition(user_id, next_state, keyboard_type, messages)

        elif payload["text"] == "Отменить":
            self.cancel_creating_classroom(user_id)

    def s_enter_school_name_class_create_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_SCHOOL_NAME_CLASSCREATE"""
        if payload is None:
            if len(message) > 32:
                self.send_message(user_id, "Длина названия превышает 32 символа. Введите другое название:",
                                  self.get_keyboard("cancel"))
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_school_name(classroom_id, message)

                next_state, keyboard_type, messages = States.get_next_state_config(
                    States.S_ENTER_SCHOOL_NAME_CLASSCREATE)
                self.send_message(user_id, f"Название школы будущего класса: {message}", self.get_keyboard("empty"))

                self.state_transition(user_id, next_state, keyboard_type, messages)

        elif payload["text"] == "Отменить":
            self.cancel_creating_classroom(user_id)

        elif payload["text"] == "На шаг назад":
            self.user_db.set_user_dialog_state(user_id, States.S_ENTER_CLASS_NAME_CLASSCREATE.value)

            self.send_message(user_id, "Напишите название будущего класса (макс. 32 символа):",
                              self.get_keyboard("cancel"))

    def s_enter_access_class_create_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_ENTER_ACCESS_CLASSCREATE"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Отменить":
            self.cancel_creating_classroom(user_id)

        elif payload["text"] == "На шаг назад":
            next_state, keyboard_type, messages = States.get_next_state_config(States.S_ENTER_CLASS_NAME_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, messages)

        elif payload["text"] == "Да":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            self.classroom_db.update_classroom_access(classroom_id, True)

            next_state, keyboard_type, messages = States.get_next_state_config(States.S_ENTER_ACCESS_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, messages)

        elif payload["text"] == "Нет":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            self.classroom_db.update_classroom_access(classroom_id, False)

            next_state, keyboard_type, messages = States.get_next_state_config(States.S_ENTER_ACCESS_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, messages)

    def s_enter_description_class_create_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_DESCRIPTION_CLASSCREATE"""
        if payload is None:
            if len(message) > 200:
                self.send_message(user_id, "Длина названия превышает 200 символа. Введите другое название:",
                                  self.get_keyboard("cancel_back"))
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_classroom_description(classroom_id, message)
                classroom_name, school_name, access, description = \
                    self.classroom_db.get_information_for_creating_classroom(classroom_id)

                next_state, keyboard_type, messages = States.get_next_state_config(
                    States.S_ENTER_DESCRIPTION_CLASSCREATE)
                self.send_message(user_id, f"Первоначальные настройки класса:\n"
                                           f"id: {classroom_id}\n"
                                           f"Название класса: {classroom_name}\n"
                                           f"Название школы: {school_name}\n"
                                           f"Могут ли участники приглашать: {'Да' if access else 'Нет'}\n"
                                           f"Описание класса: {description}",
                                  self.get_keyboard("empty"))

                self.state_transition(user_id, next_state, keyboard_type, messages)

        elif payload["text"] == "Отменить":
            self.cancel_creating_classroom(user_id)

        elif payload["text"] == "На шаг назад":
            next_state, keyboard_type, messages = States.get_next_state_config(States.S_ENTER_SCHOOL_NAME_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, messages)

    def s_submit_class_create_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_SUBMIT_CLASSCREATE"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Принять":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            self.classroom_db.update_user_customize_classroom(user_id, "null")
            self.classroom_db.update_classroom_created(classroom_id, True)

            next_state, keyboard_type, messages = States.get_next_state_config(States.S_SUBMIT_CLASSCREATE)
            self.send_message(user_id, "Поздравляю! Класс создан", self.get_keyboard("menu"))

            self.state_transition(user_id, next_state, keyboard_type, messages)

        elif payload["text"] == "Отклонить":
            next_state, keyboard_type, messages = States.get_next_state_config(States.S_ENTER_ACCESS_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, messages)

    def s_in_class_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling STATES.S_IN_CLASS_MYCLASSES"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", keyboard=self.get_keyboard("menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def state_transition(self, user_id: int, next_state, keyboard_type: str, messages: list) -> None:
        """Changes states"""
        self.user_db.set_user_dialog_state(user_id, next_state.value)

        if messages:
            for message in messages[:-1]:
                self.send_message(user_id, message, self.get_keyboard("empty"))

            self.send_message(user_id, messages[-1], self.get_keyboard(keyboard_type))

    def cancel_creating_classroom(self, user_id: int) -> None:
        """Set state to States.S_NOTHING"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        self.classroom_db.delete_classroom(classroom_id)
        self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)
        self.send_message(user_id, "Создание класса отменено", self.get_keyboard("menu"))

    def p_enter_the_classroom_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with type: enter_the_classroom"""
        if current_dialog_state == States.S_NOTHING.value:
            classroom_id = payload["classroom_id"]
            classroom_name = self.classroom_db.get_classroom_name(classroom_id)
            self.classroom_db.update_user_customize_classroom(user_id, classroom_id)

            self.send_message(user_id, f"Ты в классе {classroom_name}", self.get_keyboard("my_class_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES.value)
        else:
            self.send_message(user_id, "Закончи текущее действие или выйди в главное меню")


class DiaryVkBot(Handlers):
    def __init__(self, token: str, group_id: int, user_db: UserDataBase, classroom_db: ClassroomCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db)

    def listen(self) -> None:
        """Listening events"""
        for event in self.bot_long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_user:
                    user_id = event.object.message["from_id"]  # Getting user_id
                    message = event.object.message["text"]  # Getting message's text
                    payload = loads(event.object.message["payload"]) if "payload" in event.object.message else None  # Payload

                    user_information = self.get_user_info(user_id)  # User_id, first_name, nickname

                    self.user_db.insert_new_user(user_id,
                                                 user_information["screen_name"],
                                                 user_information["first_name"],
                                                 False
                                                 )  # Will add a new user if user writes his first message
                    self.classroom_db.insert_new_customizer(user_id)

                    if self.is_member(user_id):  # Checking first condition

                        if self.user_db.check_user_is_ready(user_id):  # Checking second condition
                            current_dialog_state = self.user_db.get_user_dialog_state(user_id)
                            self.filter_dialog_state(user_id, message, payload, current_dialog_state)
                        else:
                            self.user_db.set_user_is_ready(
                                user_id)  # First condition is True but this is a first user's message
                            self.send_message(user_id, "Добро пожаловать в наше сообщество!\n"
                                                       "Что может наш бот? (Инструкция)",
                                              self.get_keyboard("menu"))
                    else:
                        self.send_message(user_id,  # User is not a member
                                          "Перед использованием бота подпишись на группу!",
                                          self.get_keyboard("empty"))
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                event_id = event.object["event_id"]
                user_id = event.object["user_id"]
                peer_id = event.object["peer_id"]
                payload = event.object["payload"]

                self.send_message_event_answer(event_id, user_id, peer_id, "")
                if self.is_member(user_id):
                    current_dialog_state = self.user_db.get_user_dialog_state(user_id)
                    self.filter_payload_type(user_id, payload, current_dialog_state)
                else:
                    self.send_message(user_id,
                                      "Перед использованием бота подпишись на группу!",
                                      self.get_keyboard("empty"))

            else:
                print(event)

    def filter_dialog_state(self, user_id: int, message: str, payload: dict, current_dialog_state: int) -> None:
        """Filtering dialog states"""
        match current_dialog_state:
            case States.S_NOTHING.value:
                self.s_nothing_handler(user_id, payload)

            # CLASSCREATE
            case States.S_ENTER_CLASS_NAME_CLASSCREATE.value:
                self.s_enter_class_name_class_create_handler(user_id, message, payload)

            case States.S_ENTER_SCHOOL_NAME_CLASSCREATE.value:
                self.s_enter_school_name_class_create_handler(user_id, message, payload)

            case States.S_ENTER_ACCESS_CLASSCREATE.value:
                self.s_enter_access_class_create_handler(user_id, payload)

            case States.S_ENTER_DESCRIPTION_CLASSCREATE.value:
                self.s_enter_description_class_create_handler(user_id, message, payload)

            case States.S_SUBMIT_CLASSCREATE.value:
                self.s_submit_class_create_handler(user_id, payload)

            # MYCLASSES
            case States.S_IN_CLASS_MYCLASSES.value:
                self.s_in_class_my_classes_handler(user_id, payload)

    def filter_payload_type(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Filtering payload types"""
        match payload["type"]:
            case "enter_the_classroom":
                self.p_enter_the_classroom_handler(user_id, payload, current_dialog_state)

            case "time_table_menu":
                pass


if __name__ == "__main__":
    with connect(
            host=HOST,
            user=USER,
            password=PASSWORD
    ) as connection_to_create_db:
        with connection_to_create_db.cursor() as cursor:
            cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}""")

    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    user_db = UserDataBase(connection)
    classroom_db = ClassroomCommands(connection)

    my_bot = DiaryVkBot(token=TOKEN, group_id=GROUP_ID,
                        user_db=user_db,
                        classroom_db=classroom_db
                        )

    my_bot.listen()
