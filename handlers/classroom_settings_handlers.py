from supporting_functions import *
from states import States


class ClassroomSettingsHandlers(SupportingFunctions):
    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db)

    def s_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_CLASSROOM_SETTINGS"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("classroom_settings"))

        elif payload["text"] == "Основные":
            self.send_message(user_id, "Основные настройки класса", self.get_keyboard("main_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в меню класса...", self.get_keyboard("my_class_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_main_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻",
                              self.get_keyboard("main_classroom_settings"))

        elif payload["text"] == "Тип класса":
            keyboard_type_dictionary = {
                "Публичный": "access_menu_back_public",
                "Приглашения": "access_menu_back_invite",
                "Закрытый": "access_menu_back_close"
            }
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            access = self.classroom_db.get_classroom_access(classroom_id)
            keyboard_type = keyboard_type_dictionary[access]

            self.send_message(user_id, "Выберете новый тип класса (зеленым покрашен текущий тип):",
                              self.get_keyboard(keyboard_type))
            self.user_db.set_user_dialog_state(user_id, States.S_ACCESS_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Название класса":
            self.send_message(user_id, "Впиши новое название класса (длина не более 12 символов):",
                              self.get_keyboard("back_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Название школы":
            self.send_message(user_id, "Впиши новое название школы (длина не более 32 символа):",
                              self.get_keyboard("back_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Описание класса":
            self.send_message(user_id, "Напиши новое описание класса (длина не более 200 символов):",
                              self.get_keyboard("back_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Лимит участников":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

            self.send_message(user_id, f"Текущий лимит участников: {members_limit}\n\n"
                                       f"Впишите новое число максимального количества участников (не может быть меньше "
                                       f"текущего количества участников и не может быть больше 40)",
                              self.get_keyboard("back_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_LIMIT_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Опасная зона":
            self.send_message(user_id, "Место, где стоит быть поосторожнее",
                              self.get_keyboard("main_dangerous_zone_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в настройки класса...", self.get_keyboard("classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_main_dangerous_zone_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻",
                              self.get_keyboard("main_dangerous_zone_classroom_settings"))

        elif payload["text"] == "Удалить класс":
            self.send_message(user_id, "Ты уверен, что хочешь удалить класс?",
                              self.get_keyboard("main_dangerous_zone_delete_one_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id,
                                               States.S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в основные настройки класса...",
                              self.get_keyboard("main_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_main_dangerous_zone_delete_one_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻",
                              self.get_keyboard("main_dangerous_zone_delete_one_classroom_settings"))

        elif payload["text"] == "Да":
            self.send_message(user_id, "Последнее предупреждение",
                              self.get_keyboard("main_dangerous_zone_delete_two_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id,
                                               States.S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Нет":
            self.send_message(user_id, "Возвращаемся в опасную зону...",
                              self.get_keyboard("main_dangerous_zone_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_main_dangerous_zone_delete_two_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻",
                              self.get_keyboard("main_dangerous_zone_delete_two_classroom_settings"))

        elif payload["text"] == "Удалить":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            classroom_name = self.classroom_db.get_classroom_name(classroom_id)
            self.classroom_db.delete_classroom(classroom_id)

            self.send_message(user_id, f"Класс с именем {classroom_name} удалён!", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

        elif payload["text"] == "Не удалять":
            self.send_message(user_id, "Возвращаемся в опасную зону...",
                              self.get_keyboard("main_dangerous_zone_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_access_main_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_ACCESS_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            keyboard_type_dictionary = {
                "Публичный": "access_menu_back_public",
                "Приглашения": "access_menu_back_invite",
                "Закрытый": "access_menu_back_close"
            }
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            access = self.classroom_db.get_classroom_access(classroom_id)
            keyboard_type = keyboard_type_dictionary[access]

            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard(keyboard_type))

        elif payload["text"] in ["Публичный", "Приглашения", "Закрытый"]:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            self.classroom_db.update_classroom_access(classroom_id, payload["text"])

            self.send_message(user_id, f"Тип класса изменен на {payload['text']}!",
                              self.get_keyboard("main_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Назад к основным настройкам...", self.get_keyboard("main_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_classroom_name_main_classroom_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            if len(message) > 12:
                self.send_message(user_id, "Длина названия превышает 12 символов. Введите другое название:",
                                  self.get_keyboard("back_menu"))
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_classroom_name(classroom_id, message)

                self.send_message(user_id, f"Новое название класса: {message}",
                                  self.get_keyboard("main_classroom_settings"))
                self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Назад к основным настройкам...", self.get_keyboard("main_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_school_name_main_classroom_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            if len(message) > 32:
                self.send_message(user_id, "Длина названия превышает 32 символа. Введите другое название:",
                                  self.get_keyboard("back_menu"))
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_school_name(classroom_id, message)

                self.send_message(user_id, f"Новое название школы: {message}",
                                  self.get_keyboard("main_classroom_settings"))
                self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Назад к основным настройкам...", self.get_keyboard("main_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_description_main_classroom_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            if len(message) > 200:
                self.send_message(user_id, "Длина описания превышает 200 символов. Введите другое название:",
                                  self.get_keyboard("back_menu"))
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_classroom_description(classroom_id, message)

                self.send_message(user_id, f"Новое описание класса: {message}",
                                  self.get_keyboard("main_classroom_settings"))
                self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Назад к основным настройкам...", self.get_keyboard("main_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_limit_main_classroom_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_LIMIT_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            ask_message = f"Впишите новое число максимального количества участников (не может быть меньше " \
                          f"текущего количества участников и не может быть больше 40)"

            if message.strip().isdigit():
                new_members_limit = int(message.strip())

                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                members_count = len(self.classroom_db.get_dict_of_classroom_users(classroom_id))
                old_members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

                if new_members_limit == old_members_limit:
                    self.send_message(user_id, f"Такой лимит уже и так задан\n\n{ask_message}",
                                      self.get_keyboard("back_menu"))
                elif members_count <= new_members_limit <= 40:
                    self.classroom_db.update_classroom_members_limit(classroom_id, new_members_limit)

                    self.send_message(user_id, "Новый лимит участников сохранён!",
                                      self.get_keyboard("main_classroom_settings"))
                    self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)
                else:
                    self.send_message(user_id, f"Введенное число меньше текущего кол-ва участников или больше 40\n\n"
                                               f"{ask_message}", self.get_keyboard("back_menu"))
            else:
                self.send_message(user_id, f"Неверный формат записи\n\n{ask_message}", self.get_keyboard("back_menu"))

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Назад к основным настройкам...", self.get_keyboard("main_classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MAIN_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)
