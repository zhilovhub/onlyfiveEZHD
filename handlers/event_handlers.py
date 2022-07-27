from supporting_functions import *


class EventHandlers(SupportingFunctions):
    def __init__(self, bot: Bot, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands, event_db: EventCommands) -> None:
        """Initialization"""
        super().__init__(bot=bot, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db, notification_db=notification_db, event_db=event_db)

    async def s_choose_event_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_CHOOSE_EVENT_MYCLASSES"""
        if payload is None:
            await self.state_transition(user_id, States.S_CHOOSE_EVENT_MYCLASSES, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "edit_event":
            message_event_id = payload["message_event_id"]
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            event_id = self.event_db.get_event_id_by_message_event_id(message_event_id, classroom_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            self.event_db.update_customizing_event_id(user_id, event_id)

            await self.state_transition(user_id, States.S_EDIT_EVENT_MYCLASSES,
                                        event_text + "\n\nПодробности события")

        elif payload["text"] == "Добавить событие":
            if payload["can"]:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                event_diary_id = self.event_db.get_event_diary_id(classroom_id)
                event_id = self.event_db.insert_new_event(event_diary_id)

                self.event_db.update_customizing_event_id(user_id, event_id)

                await self.state_transition(user_id,
                                            States.S_CHOOSE_EVENT_TYPE_MYCLASSES,
                                            "Выбери тип события\n\n‼1 - что-то одноразовое, например, встреча с кем-то "
                                            "(событие происходит в течение одного дня)\n\n"
                                            "⚠2 - что-то требующее коллективной работы людей, например, собрать"
                                            " какое-то кол-во чего-либо (событие может длиться один день или больше):")
            else:
                await self.state_transition(user_id, States.S_CHOOSE_EVENT_MYCLASSES,
                                            "Ты не можешь добавлять события из-за своей роли")

        elif payload["text"] == "Назад":
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES2, "Главное меню класса",
                                        sign=self.get_sign(user_id))

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_choose_event_type_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_CHOOSE_EVENT_TYPE_MYCLASSES"""
        if payload is None:
            await self.state_transition(user_id, States.S_CHOOSE_EVENT_TYPE_MYCLASSES,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] in ("1", "2"):
            payload_meaning_dict = {
                "1": False,
                "2": True
            }
            collective = payload_meaning_dict[payload["text"]]
            event_id = self.event_db.get_customizing_event_id(user_id)
            self.event_db.update_event_type(event_id, collective)

            if collective:
                await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_NAME_MYCLASSES,
                                            "Опиши событие (макс 200 символов):")
            else:
                await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_NAME_MYCLASSES,
                                            "Опиши событие (макс 200 символов):")

        elif payload["text"] == "Назад":
            await self.cancel_creating_event(user_id, to_main_menu=False)

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_enter_not_collective_event_name_handler(self, user_id: int, message: str, payload: dict
                                                        ) -> None:
        """Handling States.S_ENTER_NOT_COLLECTIVE_EVENT_NAME_MYCLASSES"""
        if payload is None:
            if len(message) < 200:
                event_id = self.event_db.get_customizing_event_id(user_id)
                self.event_db.update_event_label(event_id, message)

                await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_START_TIME_MYCLASSES,
                                            "Впиши дату и время начала события в следующем формате: YYYY-MM-DD hh:mm\n"
                                            "Например, 2022-09-05 13:05")
            else:
                await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_NAME_MYCLASSES,
                                            "Длина текста события превышает 200 символов.\nОпиши событие (макс 200 "
                                            "символов)")

        elif payload["text"] == "Назад":
            await self.state_transition(user_id,
                                        States.S_CHOOSE_EVENT_TYPE_MYCLASSES,
                                        "Выбери тип события\n\n‼1 - что-то одноразовое, например, встреча с кем-то "
                                        "(событие происходит в течение одного дня)\n\n"
                                        "⚠2 - что-то требующее коллективной работы людей, например, собрать"
                                        " какое-то кол-во чего-либо (событие может длиться один день или больше):")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_enter_not_collective_event_start_time_handler(self, user_id: int, message: str, payload: dict
                                                              ) -> None:
        """Handling States.S_ENTER_NOT_COLLECTIVE_EVENT_START_TIME_MYCLASSES"""
        if payload is None:
            try:
                event_start_time = datetime.strptime(message, "%Y-%m-%d %H:%M")

                event_id = self.event_db.get_customizing_event_id(user_id)
                self.event_db.update_event_start_time(event_id, event_start_time)

                await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_END_TIME_MYCLASSES,
                                            "Впиши время конца события в формате (или нажми пропустить, если событие "
                                            "не имеет продолжительности): hh:mm\nНапример, 13:05")
            except ValueError:
                await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_START_TIME_MYCLASSES,
                                            "Введенная запись не соответствует формату.\nВпиши дату и время начала "
                                            "события в следующем формате: YYYY-MM-DD hh:mm\nНапример, 2022-09-05 13:05")

        elif payload["text"] == "Назад":
            await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_NAME_MYCLASSES,
                                        "Опиши событие (макс 200 символов)")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_enter_not_collective_event_end_time_handler(self, user_id: int, message: str, payload: dict
                                                            ) -> None:
        """Handling States.S_ENTER_NOT_COLLECTIVE_EVENT_END_TIME_MYCLASSES"""
        if payload is None:
            try:
                event_end_time_hour_minute = datetime.strptime(message, "%H:%M")

                event_id = self.event_db.get_customizing_event_id(user_id)
                event_start_time = self.event_db.get_event_start_time(event_id)
                event_end_time = event_start_time.replace(hour=event_end_time_hour_minute.hour,
                                                          minute=event_end_time_hour_minute.minute)

                if event_end_time > event_start_time:
                    self.event_db.update_event_end_time(event_id, event_end_time)
                    self.event_db.update_event_message_event_id(event_id, auto=True)
                    event = self.event_db.get_classroom_event(event_id)
                    event_text = self.get_event_diary_text([event])

                    await self.state_transition(user_id, States.S_SUBMIT_EVENT_CREATE_MYCLASSES,
                                                f"{event_text}\n\nСоздать?", collective=False)
                else:
                    await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_END_TIME_MYCLASSES,
                                                "Время окончания события не может быть меньше или быть таким же, как "
                                                "время начала\nВпиши время конца события в формате (или нажми "
                                                "пропустить, если событие не имеет продолжительности): hh:mm\n"
                                                "Например, 13:05")
            except ValueError:
                await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_END_TIME_MYCLASSES,
                                            "Введенная запись не соответствует формату.\nВпиши время конца события в "
                                            "формате (или нажми пропустить, если событие "
                                            "не имеет продолжительности): hh:mm\nНапример, 13:05")

        elif payload["text"] == "Пропустить":
            event_id = self.event_db.get_customizing_event_id(user_id)
            self.event_db.update_event_end_time(event_id, None)
            self.event_db.update_event_message_event_id(event_id, auto=True)
            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_SUBMIT_EVENT_CREATE_MYCLASSES, f"{event_text}\n\nСоздать?",
                                        collective=False)

        elif payload["text"] == "Назад":
            await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_START_TIME_MYCLASSES,
                                        "Впиши дату и время начала события в следующем формате: YYYY-MM-DD hh:mm\n"
                                        "Например, 2022-09-05 13:05")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_enter_collective_event_name_handler(self, user_id: int, message: str, payload: dict
                                                    ) -> None:
        """Handling States.S_ENTER_COLLECTIVE_EVENT_NAME_MYCLASSES"""
        if payload is None:
            if len(message) < 200:
                event_id = self.event_db.get_customizing_event_id(user_id)
                self.event_db.update_event_label(event_id, message)

                await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_START_TIME_MYCLASSES,
                                            "Впиши дату начала события в следующем формате: YYYY-MM-DD\n"
                                            "Например, 2022-09-05")
            else:
                await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_NAME_MYCLASSES,
                                            "Длина текста события превышает 200 символов.\nОпиши событие (макс 200 "
                                            "символов)")

        elif payload["text"] == "Назад":
            await self.state_transition(user_id,
                                        States.S_CHOOSE_EVENT_TYPE_MYCLASSES,
                                        "Выбери тип события\n\n‼1 - что-то одноразовое, например, встреча с кем-то "
                                        "(событие происходит в течение одного дня)\n\n"
                                        "⚠2 - что-то требующее коллективной работы людей, например, собрать"
                                        " какое-то кол-во чего-либо (событие может длиться один день или больше):")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_enter_collective_event_start_time_handler(self, user_id: int, message: str, payload: dict
                                                          ) -> None:
        """Handling States.S_ENTER_COLLECTIVE_EVENT_START_TIME_MYCLASSES"""
        if payload is None:
            try:
                event_start_time = datetime.strptime(message, "%Y-%m-%d")

                event_id = self.event_db.get_customizing_event_id(user_id)
                self.event_db.update_event_start_time(event_id, event_start_time)

                await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_END_TIME_MYCLASSES,
                                            "Впиши дату конца события в формате (или нажми пропустить, если событие "
                                            "не имеет продолжительности больше одного дня): hh:mm\n"
                                            "Например, 2022-09-06")
            except ValueError:
                await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_START_TIME_MYCLASSES,
                                            "Введенная запись не соответствует формату.\nВпиши дату начала события в "
                                            "следующем формате: YYYY-MM-DD\nНапример, 2022-09-05")

        elif payload["text"] == "Назад":
            await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_NAME_MYCLASSES,
                                        "Опиши событие (макс 200 символов)")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_enter_collective_event_end_time_handler(self, user_id: int, message: str, payload: dict
                                                        ) -> None:
        """Handling States.S_ENTER_COLLECTIVE_EVENT_END_TIME_MYCLASSES"""
        if payload is None:
            try:
                event_end_time = datetime.strptime(message, "%Y-%m-%d")

                event_id = self.event_db.get_customizing_event_id(user_id)
                event_start_time = self.event_db.get_event_start_time(event_id)

                if event_end_time > event_start_time:
                    self.event_db.update_event_end_time(event_id, event_end_time)

                    await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_COUNT_MYCLASSES,
                                                "Впиши требуемое кол-во того, что нужно собрать (или нажми пропустить, "
                                                "если ничего собирать не нужно):")
                else:
                    await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_END_TIME_MYCLASSES,
                                                "Дата окончания события не может быть меньше или быть такой же, как "
                                                "дата начала\nВпиши дату конца события в формате (или нажми пропустить,"
                                                " если событие не имеет продолжительности больше одного дня): hh:mm\n"
                                                "Например, 2022-09-06")
            except ValueError:
                await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_END_TIME_MYCLASSES,
                                            "Введенная запись не соответствует формату.\nВпиши дату конца события в "
                                            "формате (или нажми пропустить, если событие не имеет продолжительности "
                                            "больше одного дня): hh:mm\nНапример, 2022-09-06")

        elif payload["text"] == "Пропустить":
            event_id = self.event_db.get_customizing_event_id(user_id)
            self.event_db.update_event_end_time(event_id, None)

            await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_COUNT_MYCLASSES,
                                        "Впиши требуемое кол-во того, что нужно собрать (или нажми пропустить, "
                                        "если ничего собирать не нужно):")

        elif payload["text"] == "Назад":
            await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_START_TIME_MYCLASSES,
                                        "Впиши дату начала события в следующем формате: YYYY-MM-DD\nНапример, "
                                        "2022-09-05")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_enter_collective_event_required_count_handler(self, user_id: int, message: str,
                                                              payload: dict) -> None:
        """Handling States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_COUNT_MYCLASSES"""
        if payload is None:
            if message.isdigit():
                count = int(message)

                if count < 2000000000:
                    event_id = self.event_db.get_customizing_event_id(user_id)
                    self.event_db.update_event_current_count(event_id, 0)
                    self.event_db.update_event_required_count(event_id, count)

                    await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_STUDENT_MYCLASSES,
                                                "Впиши требуемое кол-во участников (или нажми пропустить, если не нужна"
                                                " запись участников):")
                else:
                    await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_COUNT_MYCLASSES,
                                                "Введено слишком большое число\n"
                                                "Впиши требуемое кол-во того, что нужно собрать (или нажми пропустить, "
                                                "если ничего собирать не нужно):")
            else:
                await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_COUNT_MYCLASSES,
                                            "Введено не число\nВпиши требуемое кол-во того, что нужно собрать (или "
                                            "нажми пропустить, если ничего собирать не нужно):")

        elif payload["text"] == "Пропустить":
            event_id = self.event_db.get_customizing_event_id(user_id)
            self.event_db.update_event_current_count(event_id, None)
            self.event_db.update_event_required_count(event_id, None)

            await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_STUDENT_MYCLASSES,
                                        "Впиши требуемое кол-во участников (или нажми пропустить, если не нужна"
                                        " запись участников):")

        elif payload["text"] == "Назад":
            await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_END_TIME_MYCLASSES,
                                        "Впиши дату конца события в формате (или нажми пропустить, если событие не "
                                        "имеет продолжительности больше одного дня): hh:mm\nНапример, 2022-09-06")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_enter_collective_event_required_student_handler(self, user_id: int, message: str,
                                                                payload: dict) -> None:
        """Handling States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_STUDENT_MYCLASSES"""
        if payload is None:
            if message.isdigit():
                count = int(message)

                if count < 10000:
                    event_id = self.event_db.get_customizing_event_id(user_id)
                    self.event_db.update_event_required_students_count(event_id, count)
                    self.event_db.update_event_message_event_id(event_id, auto=True)
                    event = self.event_db.get_classroom_event(event_id)
                    event_text = self.get_event_diary_text([event])

                    await self.state_transition(user_id, States.S_SUBMIT_EVENT_CREATE_MYCLASSES,
                                                f"{event_text}\n\nСоздать?", collective=True)
                else:
                    await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_STUDENT_MYCLASSES,
                                                "Введено слишком большое число\n"
                                                "Впиши требуемое кол-во участников (или нажми пропустить, если не нужна"
                                                " запись участников):")
            else:
                await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_STUDENT_MYCLASSES,
                                            "Введено не число\nВпиши требуемое кол-во участников (или нажми пропустить,"
                                            " если не нужна запись участников):")

        elif payload["text"] == "Пропустить":
            event_id = self.event_db.get_customizing_event_id(user_id)
            self.event_db.update_event_required_students_count(event_id, None)
            self.event_db.update_event_message_event_id(event_id, auto=True)
            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_SUBMIT_EVENT_CREATE_MYCLASSES,
                                        f"{event_text}\n\nСоздать?", collective=True)

        elif payload["text"] == "Назад":
            await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_COUNT_MYCLASSES,
                                        "Впиши требуемое кол-во того, что нужно собрать (или нажми пропустить, если "
                                        "ничего собирать не нужно):")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_submit_event_create_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_SUBMIT_EVENT_CREATE_MYCLASSES"""
        if payload is None:
            await self.state_transition(user_id, States.S_SUBMIT_EVENT_CREATE_MYCLASSES,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Принять":
            event_id = self.event_db.get_customizing_event_id(user_id)
            self.event_db.update_event_created(event_id, True)

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            events = self.event_db.get_all_classroom_events(classroom_id)
            event_diary_text = self.get_event_diary_text(events)

            self.event_db.update_customizing_event_id(user_id, None)

            await self.notify_new_event(user_id, event_id, classroom_id, without_user_ids=[user_id])

            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES2,
                                        f"{event_diary_text}\n\nСобытие создано!", sign=self.get_sign(user_id))

        elif payload["text"] == "Отклонить":
            event_id = self.event_db.get_customizing_event_id(user_id)
            self.event_db.update_event_message_event_id(event_id, None)

            if payload["collective"]:
                await self.state_transition(user_id, States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_STUDENT_MYCLASSES,
                                            "Впиши требуемое кол-во участников (или нажми пропустить, если не нужна"
                                            " запись участников):")
            else:
                await self.state_transition(user_id, States.S_ENTER_NOT_COLLECTIVE_EVENT_END_TIME_MYCLASSES,
                                            "Впиши время конца события в формате (или нажми пропустить, если событие не"
                                            " имеет продолжительности): hh:mm\nНапример, 13:05")

        elif payload["text"] == "Главное меню":
            await self.cancel_creating_event(user_id, to_main_menu=True)

    async def s_edit_event_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_EVENT_MYCLASSES"""
        if payload is None:
            await self.state_transition(user_id, States.S_EDIT_EVENT_MYCLASSES, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Редактировать":
            if payload["can"]:
                event_id = self.event_db.get_customizing_event_id(user_id)

                event = self.event_db.get_classroom_event(event_id)
                event_text = self.get_event_diary_text([event])

                await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                            f"{event_text}\n\nНастройки события:")
            else:
                await self.state_transition(user_id, States.S_EDIT_EVENT_MYCLASSES, "Ты не можешь редактировать "
                                                                                    "события из-за своей роли!")

        elif payload["text"] == "Участвовать":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            student_id = self.classroom_db.get_student_id(user_id, classroom_id)
            event_id = self.event_db.get_customizing_event_id(user_id)

            self.event_db.insert_new_student(event_id, student_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.notify_new_leave_student_event(user_id, event_id, new=True, without_user_ids=[user_id])

            await self.state_transition(user_id, States.S_EDIT_EVENT_MYCLASSES, f"{event_text}\n\nТы участвуешь!")

        elif payload["text"] == "Покинуть":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            student_id = self.classroom_db.get_student_id(user_id, classroom_id)
            event_id = self.event_db.get_customizing_event_id(user_id)

            self.event_db.delete_student(event_id, student_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.notify_new_leave_student_event(user_id, event_id, new=False, without_user_ids=[user_id])

            await self.state_transition(user_id, States.S_EDIT_EVENT_MYCLASSES,
                                        f"{event_text}\n\nТы больше не участвуешь!")

        elif payload["text"] == "Удалить событие":
            if payload["can"]:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                event_id = self.event_db.get_customizing_event_id(user_id)

                await self.notify_delete_event(user_id, event_id, without_user_ids=[user_id])

                self.event_db.delete_event(event_id)
                self.event_db.update_customizing_event_id(user_id, None)

                classroom_events = self.event_db.get_all_classroom_events(classroom_id)
                if classroom_events:
                    event_diary_text = self.get_event_diary_text(classroom_events)
                    trans_message = f"{event_diary_text}\n\nСобытие удалено!\nВыбери номер события, рассмотреть" \
                                    f" который ты хочешь:"
                else:
                    trans_message = f"Событие удалено!\nСобытий в классе больше нет"

                await self.state_transition(user_id, States.S_CHOOSE_EVENT_MYCLASSES, trans_message)
            else:
                await self.state_transition(user_id, States.S_EDIT_EVENT_MYCLASSES, "Ты не можешь удалять событии из-за"
                                                                                    " своей роли!")

        elif payload["text"] == "Внести":
            trans_message = "Впиши количество, которое ты хочешь внести:"
            await self.state_transition(user_id, States.S_ADD_COUNT_COLLECTIVE_EVENT_MYCLASSES, trans_message)

        elif payload["text"] == "Убавить":
            trans_message = "Впиши количество, на которое ты хочешь уменьшить собранное:"
            await self.state_transition(user_id, States.S_DECREASE_COUNT_COLLECTIVE_EVENT_MYCLASSES, trans_message)

        elif payload["text"] == "Назад":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            events = self.event_db.get_all_classroom_events(classroom_id)
            event_diary_text = self.get_event_diary_text(events)

            self.event_db.update_customizing_event_id(user_id, None)

            trans_message = f"{event_diary_text}\n\nВыбери номер события, рассмотреть который ты хочешь!"
            await self.state_transition(user_id, States.S_CHOOSE_EVENT_MYCLASSES, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_add_count_collective_event_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ADD_COUNT_COLLECTIVE_EVENT_MYCLASSES"""
        if payload is None:
            if message.isdigit():
                count = int(message)

                if 0 < count < 2000000000:
                    event_id = self.event_db.get_customizing_event_id(user_id)
                    current_count = self.event_db.get_event_current_count(event_id)
                    self.event_db.update_event_current_count(event_id, current_count + count)

                    classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                    student_id = self.classroom_db.get_student_id(user_id, classroom_id)
                    event_students = self.event_db.get_event_students(event_id)
                    if student_id not in event_students:
                        self.event_db.insert_new_student(event_id, student_id)

                    event = self.event_db.get_classroom_event(event_id)
                    event_text = self.get_event_diary_text([event])

                    await self.state_transition(user_id, States.S_ADD_COUNT_COLLECTIVE_EVENT_MYCLASSES,
                                                f"{event_text}\n\nУспешно добавлено!\n\n"
                                                f"Впиши количество, которое ты хочешь внести:")
                else:
                    await self.state_transition(user_id, States.S_ADD_COUNT_COLLECTIVE_EVENT_MYCLASSES,
                                                "Введено слишком большое число или 0\n\n"
                                                "Впиши количество, которое ты хочешь внести:")
            else:
                await self.state_transition(user_id, States.S_ADD_COUNT_COLLECTIVE_EVENT_MYCLASSES,
                                            "Введено не число\n\nВпиши количество, которое ты хочешь внести:")

        elif payload["text"] == "Назад":
            event_id = self.event_db.get_customizing_event_id(user_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_EDIT_EVENT_MYCLASSES, f"{event_text}\n\nПодробности события")

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_decrease_count_collective_event_handler(self, user_id: int, message: str, payload: dict
                                                        ) -> None:
        """Handling States.S_DECREASE_COUNT_COLLECTIVE_EVENT_MYCLASSES"""
        if payload is None:
            if message.isdigit():
                count = int(message)

                if 0 < count < 2000000000:
                    event_id = self.event_db.get_customizing_event_id(user_id)
                    current_count = self.event_db.get_event_current_count(event_id)

                    if count <= current_count:
                        self.event_db.update_event_current_count(event_id, current_count - count)

                        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                        student_id = self.classroom_db.get_student_id(user_id, classroom_id)
                        event_students = self.event_db.get_event_students(event_id)
                        if student_id not in event_students:
                            self.event_db.insert_new_student(event_id, student_id)

                        event = self.event_db.get_classroom_event(event_id)
                        event_text = self.get_event_diary_text([event])

                        await self.state_transition(user_id, States.S_DECREASE_COUNT_COLLECTIVE_EVENT_MYCLASSES,
                                                    f"{event_text}\n\nУспешно уменьшено!\n\n"
                                                    f"Впиши количество, на которое ты хочешь уменьшить собранное:")
                    else:
                        await self.state_transition(user_id, States.S_DECREASE_COUNT_COLLECTIVE_EVENT_MYCLASSES,
                                                    "Введено число, большее текущего количества\n\n"
                                                    "Впиши количество, на которое ты хочешь уменьшить собранное:")
                else:
                    await self.state_transition(user_id, States.S_DECREASE_COUNT_COLLECTIVE_EVENT_MYCLASSES,
                                                "Введено слишком большое число или 0\n\n"
                                                "пиши количество, на которое ты хочешь уменьшить собранное:")
            else:
                await self.state_transition(user_id, States.S_DECREASE_COUNT_COLLECTIVE_EVENT_MYCLASSES,
                                            "Введено не число\n\n"
                                            "Впиши количество, на которое ты хочешь уменьшить собранное:")

        elif payload["text"] == "Назад":
            event_id = self.event_db.get_customizing_event_id(user_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_EDIT_EVENT_MYCLASSES, f"{event_text}\n\nПодробности события")

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_event_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EVENT_SETTINGS_MYCLASSES"""
        if payload is None:
            await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Начало":
            if payload["collective"]:
                trans_message = "Впиши новую дату начала события в следующем формате: YYYY-MM-DD\nНапример, 2022-09-05"
            else:
                trans_message = "Впиши новую дату и время начала события в следующем формате: YYYY-MM-DD hh:mm\n" \
                                "Например, 2022-09-05 13:05"
            await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_START_TIME, trans_message)

        elif payload["text"] == "Конец":
            if payload["collective"]:
                trans_message = "Впиши новую дату конца события в следующем формате: YYYY-MM-DD\nНапример, 2022-09-05"
            else:
                trans_message = "Впиши новое время конца события в следующем формате: hh:mm\nНапример, 13:05"
            await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_END_TIME, trans_message)

        elif payload["text"] == "Кол-во собрать":
            await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_REQUIRED_COUNT,
                                        "Впиши новое требуемое кол-во того, что нужно собрать:")

        elif payload["text"] == "Кол-во участников":
            await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_REQUIRED_STUDENTS_COUNT,
                                        "Впиши новое требуемое кол-во участников:")

        elif payload["text"] == "Название":
            await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_NAME_MYCLASSES,
                                        "Впиши новое описание события (макс. 200 символов)")

        elif payload["text"] == "Назад":
            event_id = self.event_db.get_customizing_event_id(user_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_EDIT_EVENT_MYCLASSES, f"{event_text}\n\nПодробности события")

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_enter_new_event_name_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_NEW_EVENT_NAME_MYCLASSES"""
        if payload is None:
            if len(message) < 200:
                event_id = self.event_db.get_customizing_event_id(user_id)
                self.event_db.update_event_label(event_id, message)

                event = self.event_db.get_classroom_event(event_id)
                event_text = self.get_event_diary_text([event])

                await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                            f"{event_text}\n\nТекст события изменён!")
            else:
                await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_NAME_MYCLASSES,
                                            "Длина текста события превышает 200 символов.\n"
                                            "Впиши новое описание события (макс. 200 символов)")

        elif payload["text"] == "Назад":
            event_id = self.event_db.get_customizing_event_id(user_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                        f"{event_text}\n\nНастройки события:")

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_enter_new_event_required_count_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_NEW_EVENT_REQUIRED_COUNT"""
        if payload is None:
            ask_message = "Впиши новое требуемое кол-во того, что нужно собрать:"
            if message.isdigit():
                count = int(message)

                if 0 < count < 2000000000:
                    event_id = self.event_db.get_customizing_event_id(user_id)
                    self.event_db.update_event_required_count(event_id, count)

                    event = self.event_db.get_classroom_event(event_id)
                    event_text = self.get_event_diary_text([event])

                    await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                                f"{event_text}\n\nТребуемое количество собрать изменёно!")
                else:
                    await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_REQUIRED_COUNT,
                                                f"Введено слишком большое число или ноль\n{ask_message}:")
            else:
                await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_REQUIRED_COUNT,
                                            f"Введено не число\n{ask_message}")

        elif payload["text"] == "Назад":
            event_id = self.event_db.get_customizing_event_id(user_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                        f"{event_text}\n\nНастройки события:")

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_enter_new_event_required_students_count_handler(self, user_id: int, message: str, payload: dict
                                                                ) -> None:
        """Handling States.S_ENTER_NEW_EVENT_REQUIRED_STUDENTS_COUNT"""
        if payload is None:
            ask_message = "Впиши новое требуемое кол-во участников:"
            if message.isdigit():
                count = int(message)

                if 0 < count < 10000:
                    event_id = self.event_db.get_customizing_event_id(user_id)
                    self.event_db.update_event_required_students_count(event_id, count)

                    event = self.event_db.get_classroom_event(event_id)
                    event_text = self.get_event_diary_text([event])

                    await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                                f"{event_text}\n\nТребуемое количество участников изменёно!")
                else:
                    await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_REQUIRED_STUDENTS_COUNT,
                                                f"Введено слишком большое число или 0\n{ask_message}")
            else:
                await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_REQUIRED_STUDENTS_COUNT,
                                            f"Введено не число\n{ask_message}")

        elif payload["text"] == "Назад":
            event_id = self.event_db.get_customizing_event_id(user_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                        f"{event_text}\n\nНастройки события:")

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_enter_new_event_start_time_handler(self, user_id: int, message: str, payload: dict
                                                   ) -> None:
        """Handling States.S_ENTER_NEW_EVENT_START_TIME"""
        if payload is None:
            event_id = self.event_db.get_customizing_event_id(user_id)
            collective = self.event_db.get_event_collective(event_id)

            if collective:
                pattern = "%Y-%m-%d"
                ask_message = "Впиши новую дату начала события в следующем формате: YYYY-MM-DD\nНапример, 2022-09-05"
            else:
                pattern = "%Y-%m-%d %H:%M"
                ask_message = "Впиши новую дату и время начала события в следующем формате: YYYY-MM-DD hh:mm\n" \
                              "Например, 2022-09-05 13:05"

            try:
                event_start_time = datetime.strptime(message, pattern)
                event_end_time = self.event_db.get_event_end_time(event_id)

                if event_end_time and event_start_time < event_end_time or not event_end_time:
                    self.event_db.update_event_start_time(event_id, event_start_time)

                    event = self.event_db.get_classroom_event(event_id)
                    event_text = self.get_event_diary_text([event])

                    await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                                f"{event_text}\n\nНастройки события:")
                else:
                    await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_START_TIME,
                                                f"Время начала не может быть позже или равным времени конца\n"
                                                f"{ask_message}")
            except ValueError:
                await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_START_TIME,
                                            f"Введенная запись не соответствует формату.\n{ask_message}")

        elif payload["text"] == "Назад":
            event_id = self.event_db.get_customizing_event_id(user_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                        f"{event_text}\n\nНастройки события:")

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_enter_new_event_end_time_handler(self, user_id: int, message: str, payload: dict
                                                 ) -> None:
        """Handling States.S_ENTER_NEW_EVENT_END_TIME"""
        if payload is None:
            event_id = self.event_db.get_customizing_event_id(user_id)
            collective = self.event_db.get_event_collective(event_id)

            if collective:
                pattern = "%Y-%m-%d"
                ask_message = "Впиши новую дату конца события в следующем формате: YYYY-MM-DD\nНапример, 2022-09-05"
            else:
                pattern = "%H:%M"
                ask_message = "Впиши новое время конца события в следующем формате: hh:mm\n" \
                              "Например, 13:05"

            try:
                event_start_time = self.event_db.get_event_start_time(event_id)
                if collective:
                    event_end_time = datetime.strptime(message, pattern)
                else:
                    event_end_time_hour_minute = datetime.strptime(message, pattern)
                    event_end_time = event_start_time.replace(hour=event_end_time_hour_minute.hour,
                                                              minute=event_end_time_hour_minute.minute)

                if event_end_time > event_start_time:
                    self.event_db.update_event_end_time(event_id, event_end_time)

                    event = self.event_db.get_classroom_event(event_id)
                    event_text = self.get_event_diary_text([event])

                    await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                                f"{event_text}\n\nНастройки события:")
                else:
                    await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_END_TIME,
                                                f"Время конца не может быть раньше или равным времени начала\n"
                                                f"{ask_message}")
            except ValueError:
                await self.state_transition(user_id, States.S_ENTER_NEW_EVENT_END_TIME,
                                            f"Введенная запись не соответствует формату.\n{ask_message}")

        elif payload["text"] == "Назад":
            event_id = self.event_db.get_customizing_event_id(user_id)

            event = self.event_db.get_classroom_event(event_id)
            event_text = self.get_event_diary_text([event])

            await self.state_transition(user_id, States.S_EVENT_SETTINGS_MYCLASSES,
                                        f"{event_text}\n\nНастройки события:")

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def cancel_creating_event(self, user_id: int, to_main_menu: bool) -> None:
        event_id = self.event_db.get_customizing_event_id(user_id)
        self.event_db.delete_event(event_id)
        if to_main_menu:
            await self.trans_to_main_menu(user_id)
        else:
            await self.state_transition(user_id, States.S_CHOOSE_EVENT_MYCLASSES,
                                        "Выбери номер события, рассмотреть который ты хочешь!")
