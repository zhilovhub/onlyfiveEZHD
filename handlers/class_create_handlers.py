from supporting_functions import *
from states import States


class ClassCreateHandlers(SupportingFunctions):
    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db)

    def s_enter_class_name_class_create_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_CLASS_NAME_CLASSCREATE"""
        if payload is None:
            if len(message) > 12:
                self.send_message(user_id, "Длина названия превышает 12 символов. Введите другое название:",
                                  self.get_keyboard("just_menu"))
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_classroom_name(classroom_id, message)

                next_state, keyboard_type, trans_message = States.get_next_state_config(
                    States.S_ENTER_CLASS_NAME_CLASSCREATE)
                trans_message = f"Название класса: {message}\n\n" + trans_message

                self.state_transition(user_id, next_state, keyboard_type, trans_message)

        elif payload["text"] == "Главное меню":
            self.cancel_creating_classroom(user_id)

    def s_enter_school_name_class_create_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_SCHOOL_NAME_CLASSCREATE"""
        if payload is None:
            if len(message) > 32:
                self.send_message(user_id, "Длина названия превышает 32 символа. Введите другое название:",
                                  self.get_keyboard("back_menu"))
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_school_name(classroom_id, message)

                next_state, keyboard_type, trans_message = States.get_next_state_config(
                    States.S_ENTER_SCHOOL_NAME_CLASSCREATE)
                trans_message = f"Название школы будущего класса: {message}\n\n" + trans_message

                self.state_transition(user_id, next_state, keyboard_type, trans_message)

        elif payload["text"] == "Главное меню":
            self.cancel_creating_classroom(user_id)

        elif payload["text"] == "Назад":
            self.user_db.set_user_dialog_state(user_id, States.S_ENTER_CLASS_NAME_CLASSCREATE.value)

            self.send_message(user_id, "Напишите название будущего класса (макс. 12 символов):",
                              self.get_keyboard("just_menu"))

    def s_enter_access_class_create_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_ENTER_ACCESS_CLASSCREATE"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("access_menu_back"))

        elif payload["text"] == "Главное меню":
            self.cancel_creating_classroom(user_id)

        elif payload["text"] == "Назад":
            next_state, keyboard_type, trans_message = \
                States.get_next_state_config(States.S_ENTER_CLASS_NAME_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, trans_message)

        elif payload["text"] in ["Публичный", "Заявки", "Закрытый"]:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            self.classroom_db.update_classroom_access(classroom_id, payload["text"])

            next_state, keyboard_type, trans_message = States.get_next_state_config(States.S_ENTER_ACCESS_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, trans_message)

    def s_enter_description_class_create_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_DESCRIPTION_CLASSCREATE"""
        if payload is None:
            if len(message) > 200:
                self.send_message(user_id, "Длина названия превышает 200 символа. Введите другое название:",
                                  self.get_keyboard("back_menu"))
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_classroom_description(classroom_id, message)
                classroom_name, school_name, access, description = \
                    self.classroom_db.get_information_of_classroom(classroom_id)

                next_state, keyboard_type, trans_message = States.get_next_state_config(
                    States.S_ENTER_DESCRIPTION_CLASSCREATE)
                trans_message = f"Первоначальные настройки класса:\n" \
                                f"id: {classroom_id}\n" \
                                f"Название класса: {classroom_name}\n" \
                                f"Название школы: {school_name}\n" \
                                f"Тип класса: {access}\n" \
                                f"Описание класса: {description}\n\n" + trans_message

                self.state_transition(user_id, next_state, keyboard_type, trans_message)

        elif payload["text"] == "Главное меню":
            self.cancel_creating_classroom(user_id)

        elif payload["text"] == "Назад":
            next_state, keyboard_type, trans_message = \
                States.get_next_state_config(States.S_ENTER_SCHOOL_NAME_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, trans_message)

    def s_submit_class_create_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_SUBMIT_CLASSCREATE"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("submit_back"))

        elif payload["text"] == "Принять":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            role_id = self.role_db.insert_new_role(classroom_id, "Админ", is_admin=True)
            self.role_db.insert_new_role(classroom_id, "Участник", is_default_member=True)

            self.classroom_db.insert_new_user_in_classroom(user_id, classroom_id, role_id)
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.classroom_db.update_classroom_created(classroom_id, True)

            next_state, keyboard_type, trans_message = States.get_next_state_config(States.S_SUBMIT_CLASSCREATE)

            self.state_transition(user_id, next_state, keyboard_type, trans_message)

        elif payload["text"] == "Отклонить":
            next_state, keyboard_type, trans_message = States.get_next_state_config(States.S_ENTER_ACCESS_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, trans_message)

        elif payload["text"] == "Главное меню":
            self.cancel_creating_classroom(user_id)

    def cancel_creating_classroom(self, user_id: int) -> None:
        """Set state to States.S_NOTHING"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        self.classroom_db.delete_classroom(classroom_id)
        self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)
        self.send_message(user_id, "Создание класса отменено", self.get_keyboard("menu"))
