from supporting_functions import *

from classroom import ClassroomCommands
from users import UserDataBase
from states import States


class StateHandlers(SupportingFunctions):
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
                    "text": "enter_the_classroom", "classroom_id": classroom_id
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


class CallbackPayloadHandlers(StateHandlers):
    def __init__(self, token: str, group_id: int, user_db: UserDataBase, classroom_db: ClassroomCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db)

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
