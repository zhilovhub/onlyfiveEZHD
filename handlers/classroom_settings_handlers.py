from supporting_functions import *


class ClassroomSettingsHandlers(SupportingFunctions):
    def __init__(self, bot: Bot, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands, event_db: EventCommands) -> None:
        """Initialization"""
        super().__init__(bot=bot, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db, notification_db=notification_db, event_db=event_db)

    async def s_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_CLASSROOM_SETTINGS"""
        if payload is None:
            await self.state_transition(user_id, States.S_CLASSROOM_SETTINGS, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Основные":
            trans_message = "Основные настройки класса"
            await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Уведомления":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            notification_dict = self.notification_db.get_notification_values_dict(user_id, classroom_id)

            trans_message = "Выбери, какие уведомления получать/не получать"
            await self.state_transition(user_id, States.S_NOTIFICATION_SETTINGS_CLASSROOM_SETTINGS, trans_message,
                                        *notification_dict.values())

        elif payload["text"] == "Назад":
            trans_message = "Возвращаемся в меню класса..."
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES, trans_message,
                                        sign=self.get_sign(user_id))

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_notification_settings_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_NOTIFICATION_SETTINGS_CLASSROOM_SETTINGS"""
        if payload is None:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            notification_dict = self.notification_db.get_notification_values_dict(user_id, classroom_id)

            await self.state_transition(user_id, States.S_NOTIFICATION_SETTINGS_CLASSROOM_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻", *notification_dict.values())

        elif payload["text"] in ["Кто-то вступил", "Кто-то ушел", "Новая заявка", "События"]:
            payload_text_meaning_dict = {
                "Кто-то вступил": "new_classmate",
                "Кто-то ушел": "leave_classmate",
                "Новая заявка": "requests",
                "События": "events"
            }
            notification_type = payload_text_meaning_dict[payload["text"]]

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            self.notification_db.update_notification_value(user_id, classroom_id, notification_type)
            notification_dict = self.notification_db.get_notification_values_dict(user_id, classroom_id)

            trans_message = "Сохранено!"
            await self.state_transition(user_id, States.S_NOTIFICATION_SETTINGS_CLASSROOM_SETTINGS,
                                        f"{trans_message}\n\n"
                                        f"Выбери, какие "
                                        f"уведомления получать/не"
                                        f" получать",
                                        *notification_dict.values())

        elif payload["text"] == "Назад":
            trans_message = "Настройки класса\n\nКоличество настроек зависит от твоей роли в этом классе!"
            await self.state_transition(user_id, States.S_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_main_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Тип класса":
            if payload["can"]:
                keyboard_type_kwargs = {
                    "Публичный": {"public_color": "positive", "invite_color": "negative", "close_color": "negative"},
                    "Заявки": {"public_color": "negative", "invite_color": "positive", "close_color": "negative"},
                    "Закрытый": {"public_color": "negative", "invite_color": "negative", "close_color": "positive"}
                }
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                access = self.classroom_db.get_classroom_access(classroom_id)
                keyboard_kwargs = keyboard_type_kwargs[access]

                trans_message = "Выберете новый тип класса (зеленым покрашен текущий тип):"
                await self.state_transition(user_id,
                                            States.S_ACCESS_MAIN_CLASSROOM_SETTINGS, trans_message, **keyboard_kwargs)
            else:
                await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS,
                                            "Ты не можешь изменять тип класса из-"
                                            "за своей роли")

        elif payload["text"] == "Название класса":
            if payload["can"]:
                trans_message = "Впиши новое название класса (длина не более 12 символов):"
                await self.state_transition(user_id, States.S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS, trans_message)
            else:
                await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS,
                                            "Ты не можешь изменять название класса"
                                            " из-за своей роли")

        elif payload["text"] == "Название школы":
            if payload["can"]:
                trans_message = "Впиши новое название школы (длина не более 32 символа):"
                await self.state_transition(user_id, States.S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS, trans_message)
            else:
                await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS,
                                            "Ты не можешь изменять название школы"
                                            " из-за своей роли")

        elif payload["text"] == "Описание класса":
            if payload["can"]:
                trans_message = "Напиши новое описание класса (длина не более 200 символов):"
                await self.state_transition(user_id, States.S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS, trans_message)
            else:
                await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS,
                                            "Ты не можешь изменять описание класса"
                                            " из-за своей роли")

        elif payload["text"] == "Лимит участников":
            if payload["can"]:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

                trans_message = f"Текущий лимит участников: {members_limit}\n\n" \
                                f"Впишите новое число максимального количества участников (не может быть меньше " \
                                f"текущего количества участников и не может быть больше 40)"
                await self.state_transition(user_id, States.S_LIMIT_MAIN_CLASSROOM_SETTINGS, trans_message)
            else:
                await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, "Ты не можешь изменять лимит"
                                                                                       " участников из-за своей роли")

        elif payload["text"] == "Опасная зона":
            trans_message = "Место, где стоит быть поосторожнее"
            await self.state_transition(user_id, States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Возвращаемся в настройки класса..."
            await self.state_transition(user_id, States.S_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_main_dangerous_zone_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS"""
        if payload is None:
            await self.state_transition(user_id, States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Покинуть класс":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_id = self.role_db.get_admin_role_id(classroom_id)
            role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)

            if admin_role_id == role_id:
                trans_message = "Ты не можешь покинуть класс будучи админом!"
                await self.state_transition(user_id, States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS, trans_message)
            else:
                self.classroom_db.delete_student(classroom_id, user_id)
                keyboard_kwarg = self.get_look_keyboard_kwargs(user_id, classroom_id)
                await self.notify_leave_classmate(user_id, classroom_id, kicked=False)

                trans_message = "Ты покинул класс!"
                await self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message,
                                            classroom_type=keyboard_kwarg)

        elif payload["text"] == "Удалить класс":
            trans_message = "Ты уверен, что хочешь удалить класс?"
            await self.state_transition(user_id, States.S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS,
                                        trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Возвращаемся в основные настройки класса..."
            await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_main_dangerous_zone_delete_one_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS"""
        if payload is None:
            await self.state_transition(user_id, States.S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Да":
            trans_message = "Последнее предупреждение"
            await self.state_transition(user_id, States.S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS,
                                        trans_message)

        elif payload["text"] == "Нет":
            trans_message = "Возвращаемся в опасную зону..."
            await self.state_transition(user_id, States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_main_dangerous_zone_delete_two_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS"""
        if payload is None:
            await self.state_transition(user_id, States.S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Удалить":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            classroom_name = self.classroom_db.get_classroom_name(classroom_id)
            self.classroom_db.delete_classroom(classroom_id)
            self.classroom_db.update_user_customize_classroom_id(user_id, None)

            trans_message = f"Класс с именем {classroom_name} удалён!"
            await self.state_transition(user_id, States.S_NOTHING, trans_message)

        elif payload["text"] == "Не удалять":
            trans_message = "Возвращаемся в опасную зону..."
            await self.state_transition(user_id, States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_access_main_classroom_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_ACCESS_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            keyboard_type_kwargs = {
                "Публичный": {"public_color": "positive", "invite_color": "negative", "close_color": "negative"},
                "Заявки": {"public_color": "negative", "invite_color": "positive", "close_color": "negative"},
                "Закрытый": {"public_color": "negative", "invite_color": "negative", "close_color": "positive"}
            }
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            access = self.classroom_db.get_classroom_access(classroom_id)
            keyboard_kwargs = keyboard_type_kwargs[access]

            await self.state_transition(user_id, States.S_ACCESS_MAIN_CLASSROOM_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻",
                                        **keyboard_kwargs)

        elif payload["text"] in ["Публичный", "Заявки", "Закрытый"]:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            self.classroom_db.update_classroom_access(classroom_id, payload["text"])

            trans_message = f"Тип класса изменен на {payload['text']}!"
            await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Назад к основным настройкам..."
            await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_classroom_name_main_classroom_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            if len(message) > 12:
                trans_message = "Длина названия превышает 12 символов. Введите другое название:"
                await self.state_transition(user_id, States.S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS, trans_message)
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_classroom_name(classroom_id, message)

                trans_message = f"Новое название класса: {message}"
                await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Назад к основным настройкам..."
            await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_school_name_main_classroom_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            if len(message) > 32:
                trans_message = "Длина названия превышает 32 символа. Введите другое название:"
                await self.state_transition(user_id, States.S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS, trans_message)
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_school_name(classroom_id, message)

                trans_message = f"Новое название школы: {message}"
                await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Назад к основным настройкам..."
            await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_description_main_classroom_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS"""
        if payload is None:
            if len(message) > 200:
                trans_message = "Длина описания превышает 200 символов. Введите другое название:"
                await self.state_transition(user_id, States.S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS, trans_message)
            else:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                self.classroom_db.update_classroom_description(classroom_id, message)

                trans_message = f"Новое описание класса: {message}"
                await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Назад к основным настройкам..."
            await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_limit_main_classroom_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
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
                    trans_message = f"Такой лимит уже и так задан\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_LIMIT_MAIN_CLASSROOM_SETTINGS, trans_message)
                elif members_count <= new_members_limit <= 40:
                    self.classroom_db.update_classroom_members_limit(classroom_id, new_members_limit)

                    trans_message = "Новый лимит участников сохранён!"
                    await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)
                else:
                    trans_message = f"Введенное число меньше текущего кол-ва участников или больше 40\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_LIMIT_MAIN_CLASSROOM_SETTINGS, trans_message)
            else:
                trans_message = f"Неверный формат записи\n\n{ask_message}"
                await self.state_transition(user_id, States.S_LIMIT_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Назад к основным настройкам..."
            await self.state_transition(user_id, States.S_MAIN_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)
