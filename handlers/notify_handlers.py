from supporting_functions import *


class NotificationHandlers(SupportingFunctions):
    def __init__(self, bot: Bot, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands, event_db: EventCommands) -> None:
        """Initialization"""
        super().__init__(bot=bot, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db, notification_db=notification_db, event_db=event_db)

    async def s_choose_user_for_notification_handler_my_classes(self, user_id: int, message: str, payload: dict
                                                                ) -> None:
        """Handling States.S_CHOOSE_USER_FOR_NOTIFICATION_MYCLASSES"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)

        if payload is None:
            roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
            members_text = self.get_members_text(roles_dictionary)
            ask_message = f"{members_text}\n\nВыбери, кого уведомить\n(впиши их номера через пробел, " \
                          f"например, 1 2 21 23):"

            members_message = message.split()
            for member in members_message:
                if not (member.isdigit() and 0 < int(member) <= len(members_dictionary)):
                    await self.state_transition(user_id, States.S_CHOOSE_USER_FOR_NOTIFICATION_MYCLASSES,
                                                f"Значение {member} не соответствует формату.\n\n{ask_message}")
                    break
            else:
                member_ids = []

                members_indexes = list(map(int, members_message))
                ind = 1
                for role in roles_dictionary:
                    for member_id in roles_dictionary[role]:
                        if ind in members_indexes:
                            member_ids.append(member_id)
                        ind += 1

                notification_id = self.notification_db.get_customizing_notification_id(user_id, classroom_id)
                student_ids = self.classroom_db.get_student_ids(member_ids, classroom_id)
                self.notification_db.insert_notification_students(notification_id, student_ids)

                await self.state_transition(user_id, States.S_ENTER_TEXT_FOR_NOTIFICATION_MYCLASSES,
                                            "Напиши текст уведомления (макс. 2000 символов):")

        elif payload["text"] == "Всех":
            member_ids = [member_id for member_id in self.classroom_db.get_dict_of_classroom_users(classroom_id)]

            notification_id = self.notification_db.get_customizing_notification_id(user_id, classroom_id)
            student_ids = self.classroom_db.get_student_ids(member_ids, classroom_id)
            self.notification_db.insert_notification_students(notification_id, student_ids)

            await self.state_transition(user_id, States.S_ENTER_TEXT_FOR_NOTIFICATION_MYCLASSES,
                                        "Напиши текст уведомления (макс. 2000 символов):")

        elif payload["text"] == "Назад":
            await self.cancel_creating_notification(user_id, to_main_menu=False)

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_notification(user_id, to_main_menu=True)

    async def s_enter_text_for_notification_handler_my_classes(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_TEXT_FOR_NOTIFICATION_MYCLASSES"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        notification_id = self.notification_db.get_customizing_notification_id(user_id, classroom_id)

        if payload is None:
            if len(message) <= 2000:
                self.notification_db.update_notification_text(notification_id, message)

                await self.state_transition(user_id, States.S_ENTER_DATE_FOR_NOTIFICATION_MYCLASSES,
                                            "Впиши дату и время, когда это уведомление прислать выбранным участникам, в"
                                            " формате DD.MM.YYYY hh:mm\nНапример, 01.09.2022 12:05")
            else:
                await self.state_transition(user_id, States.S_ENTER_TEXT_FOR_NOTIFICATION_MYCLASSES,
                                            f"Длина твоего текста больше 2000 символов!\n\n"
                                            f"Напиши текст уведомления (макс. 2000 символов):")

        elif payload["text"] == "Назад":
            roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
            members_text = self.get_members_text(roles_dictionary)

            self.notification_db.delete_notification_students(notification_id)

            await self.state_transition(user_id, States.S_CHOOSE_USER_FOR_NOTIFICATION_MYCLASSES,
                                        f"{members_text}\n\nВыбери, кого уведомить\n(впиши их номера через пробел, "
                                        f"например, 1 2 21 23):")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_notification(user_id, to_main_menu=True)

    async def s_enter_date_for_notification_handler_my_classes(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_DATE_FOR_NOTIFICATION_MYCLASSES"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        notification_id = self.notification_db.get_customizing_notification_id(user_id, classroom_id)

        if payload is None:
            pattern = "%d.%m.%Y %H:%M"
            ask_message = "Впиши дату и время, когда это уведомление прислать выбранным участникам, в формате" \
                          " DD.MM.YYYY hh:mm\nНапример, 01.09.2022 12:05"

            try:
                notification_datetime = datetime.strptime(message, pattern)
                if notification_datetime > datetime.now():
                    self.notification_db.update_notification_datetime(notification_id, notification_datetime)
                    notification_text = self.get_notification_text(notification_id)

                    await self.state_transition(user_id, States.S_ACCEPT_CREATE_NOTIFICATION_MYCLASSES,
                                                f"В {notification_datetime.strftime('%d.%m.%Y %H:%M')} выбранным "
                                                f"участникам придёт такое сообщение:\n\n{notification_text}\n\n"
                                                f"Создать уведомление?")
                else:
                    await self.state_transition(user_id, States.S_ENTER_DATE_FOR_NOTIFICATION_MYCLASSES,
                                                f"Введенное не может быть раньше, чем текущая дата и время\n\n"
                                                f"{ask_message}")
            except ValueError:
                await self.state_transition(user_id, States.S_ENTER_DATE_FOR_NOTIFICATION_MYCLASSES,
                                            f"Введенная запись не соответсвует формату\n\n{ask_message}")

        elif payload["text"] == "Назад":
            self.notification_db.update_notification_text(notification_id, None)

            await self.state_transition(user_id, States.S_ENTER_TEXT_FOR_NOTIFICATION_MYCLASSES,
                                        "Напиши текст уведомления (макс. 2000 символов):")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_notification(user_id, to_main_menu=True)

    async def s_accept_create_notification_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_ACCEPT_CREATE_NOTIFICATION_MYCLASSES"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        notification_id = self.notification_db.get_customizing_notification_id(user_id, classroom_id)

        if payload is None:
            await self.state_transition(user_id, States.S_ACCEPT_CREATE_NOTIFICATION_MYCLASSES,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Отклонить":
            self.notification_db.update_notification_datetime(notification_id, None)

            await self.state_transition(user_id, States.S_ENTER_DATE_FOR_NOTIFICATION_MYCLASSES,
                                        "Впиши дату и время, когда это уведомление прислать выбранным участникам, в "
                                        "формате DD.MM.YYYY hh:mm\nНапример, 01.09.2022 12:05")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_notification(user_id, to_main_menu=True)

    async def cancel_creating_notification(self, user_id: int, to_main_menu: bool) -> None:
        """Trans to classroom/main menu"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        notification_id = self.notification_db.get_customizing_notification_id(user_id, classroom_id)
        self.notification_db.delete_notification_from_diary(notification_id)
        if to_main_menu:
            await self.trans_to_main_menu(user_id)
        else:
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES2, "Главное меню класса",
                                        sign=self.get_sign(user_id))
