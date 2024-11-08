from supporting_functions import *


class MyClassesHandlers(SupportingFunctions):
    def __init__(self, bot: Bot, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands, event_db: EventCommands, admin_panel_db: AdminCommands) -> None:
        """Initialization"""
        super().__init__(bot=bot, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db, notification_db=notification_db, event_db=event_db,
                         admin_panel_db=admin_panel_db)

    async def s_in_class_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_IN_CLASS_MYCLASSES"""
        if payload is None:
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES, "Для навигации используй кнопки!👇🏻",
                                        sign=self.get_sign(user_id))

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

        elif payload["text"] == "Ещё":
            trans_message = "Другое меню класса"
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES2, trans_message,
                                        sign=self.get_sign(user_id))

        elif payload["text"] == "Настройки":
            trans_message = "Настройки класса\n\nКоличество настроек зависит от твоей роли в этом классе!"
            await self.state_transition(user_id, States.S_CLASSROOM_SETTINGS, trans_message)

        elif payload["text"] == "Участники":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
            members_text = self.get_members_text(roles_dictionary)

            keyboard = Keyboard(inline=True)
            keyboard.add(Callback("Настройки",
                                  payload={
                                      "text": "enter_members_settings",
                                      "classroom_id": classroom_id
                                  }))

            await self.send_message(user_id, members_text, keyboard.get_json())

        elif payload["text"] in ["Дз текущее", "Дз будущее"]:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
            diary_role_properties_dictionary = self.role_db.get_diary_role_properties_dict(role_id)
            change_current_homework = diary_role_properties_dictionary["change_current_homework"]
            change_next_homework = diary_role_properties_dictionary["change_next_homework"]

            payload_meanings_dict = {
                "Дз текущее": ("edit_current_homework", "current", "Домашнее задание на текущую неделю\n\n",
                               change_current_homework),
                "Дз будущее": ("edit_next_homework", "next", "Домашнее задание на следующую неделю\n\n",
                               change_next_homework)
            }
            callback_payload_text = payload_meanings_dict[payload["text"]][0]
            week_type = payload_meanings_dict[payload["text"]][1]
            help_text = payload_meanings_dict[payload["text"]][2]
            can = payload_meanings_dict[payload["text"]][3]

            formatted_week_lessons_diary = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id,
                                                                                                 week_type)
            formatted_week_lessons_homework = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id,
                                                                                                    week_type,
                                                                                                    homework=True)
            diary_homework_text = self.get_week_diary_text(formatted_week_lessons_diary, week_type,
                                                           formatted_week_lessons_homework)

            keyboard = Keyboard(inline=True)
            keyboard.add(Callback("Изменить" if can else "Изменить❌",
                                  payload={
                                      "text": callback_payload_text,
                                      "classroom_id": classroom_id,
                                      "can": can
                                  }))

            await self.send_message(user_id, help_text + diary_homework_text, keyboard.get_json())

        elif payload["text"] in ["Расписание эталонное", "Расписание текущее", "Расписание будущее"]:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
            diary_role_properties_dictionary = self.role_db.get_diary_role_properties_dict(role_id)
            change_standard_week = diary_role_properties_dictionary["change_standard_week"]
            change_current_week = diary_role_properties_dictionary["change_current_week"]
            change_next_week = diary_role_properties_dictionary["change_next_week"]

            payload_meanings_dict = {
                "Расписание эталонное": ("edit_standard", "standard", "Эталонное расписание\n\nМожно копировать в "
                                                                      "текущее и будущее расписание.\nБудет "
                                                                      "автоматически устанавливаться в будущее "
                                                                      "расписание каждую неделю\n\n",
                                         change_standard_week),
                "Расписание текущее": ("edit_current", "current", "Расписание на текущую неделю\n\n",
                                       change_current_week),
                "Расписание будущее": ("edit_next", "next", "Расписание на следующую неделю\n\n",
                                       change_next_week)
            }
            callback_payload_text = payload_meanings_dict[payload["text"]][0]
            week_type = payload_meanings_dict[payload["text"]][1]
            help_text = payload_meanings_dict[payload["text"]][2]
            can = payload_meanings_dict[payload["text"]][3]

            formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, week_type)
            diary_text = self.get_week_diary_text(formatted_week_lessons, week_type)

            keyboard = Keyboard(inline=True)
            keyboard.add(Callback("Изменить" if can else "Изменить❌",
                                  payload={
                                      "text": callback_payload_text,
                                      "classroom_id": classroom_id,
                                      "can": can
                                  }))

            await self.send_message(user_id, help_text + diary_text, keyboard.get_json())

        elif payload["text"] in ("edit_standard", "edit_current", "edit_next",
                                 "edit_current_homework", "edit_next_homework"):
            if payload["can"]:
                payload_meanings_dict = {
                    "edit_standard": ("standard", "эталонного расписания", States.S_EDIT_WEEK_MYCLASSES),
                    "edit_current": ("current", "текущего расписания", States.S_EDIT_WEEK_MYCLASSES),
                    "edit_next": ("next", "будущего расписания", States.S_EDIT_WEEK_MYCLASSES),
                    "edit_current_homework": ("current", "дз текущей недели", States.S_EDIT_HOMEWORK_MYCLASSES),
                    "edit_next_homework": ("next", "дз будущей недели", States.S_EDIT_HOMEWORK_MYCLASSES),
                }
                week_type = payload_meanings_dict[payload["text"]][0]
                russian_comments = payload_meanings_dict[payload["text"]][1]
                next_state = payload_meanings_dict[payload["text"]][2]

                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                student_id = self.classroom_db.get_student_id(user_id, classroom_id)
                self.diary_homework_db.insert_row_into_temp_weekday_table(student_id, user_id, week_type)

                trans_message = f"Редактирование {russian_comments}\n\nИзменения увидят ВСЕ участники класса!"
                await self.state_transition(user_id, next_state, trans_message, week_type=week_type)
            else:
                await self.send_message(user_id, "Ты не можешь редактировать это из-за своей роли")

        elif payload["text"] == "enter_members_settings":
            trans_message = "Настройки участников класса\n\n" \
                            "Здесь можно создавать и настраивать роли, удалять и приглашать участников!"
            await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "accept_request":
            classroom_id = payload["classroom_id"]
            members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)
            members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)

            request_user_id = payload["user_id"]
            first_name, last_name = self.user_db.get_user_first_and_last_name(request_user_id)

            if request_user_id in members_dictionary.keys():
                self.classroom_db.delete_request(request_user_id, classroom_id)

                await self.s_in_class_my_classes2_handler(user_id, {"text": "Заявки", "can": 1},
                                                          info_message=f"[id{request_user_id}|{first_name} {last_name}]"
                                                                       f" уже в классе!")
            elif len(members_dictionary) < members_limit:
                default_role_id = self.role_db.get_default_role_id(classroom_id)
                self.insert_new_student(request_user_id, classroom_id, default_role_id)
                self.classroom_db.delete_request(request_user_id, classroom_id)

                await self.s_in_class_my_classes2_handler(user_id, {"text": "Заявки", "can": 1},
                                                          info_message=f"[id{request_user_id}|{first_name} {last_name}]"
                                                                       f" принят в класс")
                await self.notify_about_accept_to_classroom(request_user_id, classroom_id)
                await self.notify_new_classmate(request_user_id, classroom_id,
                                                without_user_ids=[user_id, request_user_id])
            else:
                await self.send_message(user_id,
                                        f"В классе уже максимальное количество людей! ({len(members_dictionary)}"
                                        f"/{members_limit})")

        elif payload["text"] == "cancel_request":
            classroom_id = payload["classroom_id"]
            members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)

            request_user_id = payload["user_id"]

            self.classroom_db.delete_request(request_user_id, classroom_id)
            first_name, last_name = self.user_db.get_user_first_and_last_name(request_user_id)

            if request_user_id in members_dictionary.keys():
                await self.s_in_class_my_classes2_handler(user_id, {"text": "Заявки", "can": 1},
                                                          info_message=f"[id{request_user_id}|{first_name} {last_name}]"
                                                                       f" уже в классе!")
            else:
                await self.s_in_class_my_classes2_handler(user_id, {"text": "Заявки", "can": 1},
                                                          info_message=f"Заявка [id{request_user_id}|{first_name} "
                                                                       f"{last_name}] отклонена")

        elif payload["text"] == "event_settings":
            trans_message = "Выбери номер события, рассмотреть который ты хочешь!"
            await self.state_transition(user_id, States.S_CHOOSE_EVENT_MYCLASSES, trans_message)

    async def s_in_class_my_classes2_handler(self, user_id: int, payload: dict, info_message="") -> None:
        """Handling States.S_IN_CLASS_MYCLASSES2"""
        if payload is None:
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES2, "Для навигации используй кнопки!👇🏻",
                                        sign=self.get_sign(user_id))

        elif payload["text"] == "Уведомить":
            if payload["can"]:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                members_text = self.get_members_text(roles_dictionary)

                self.notification_db.insert_new_notification_into_diary(user_id, classroom_id)

                await self.state_transition(user_id, States.S_CHOOSE_USER_FOR_NOTIFICATION_MYCLASSES,
                                            f"{members_text}\n\nВыбери, кого уведомить\n(впиши их номера через пробел,"
                                            f" например, 1 2 21 23):")
            else:
                await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES2,
                                            "Ты не можешь уведомлять из-за своей роли!",
                                            sign=self.get_sign(user_id))

        elif payload["text"] == "Заявки":
            if payload["can"]:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                request_list = self.classroom_db.get_list_of_request_information(classroom_id)

                if not request_list:
                    trans_message = info_message + "\n\nЗаявок в этом классе нет"
                    await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES2, trans_message,
                                                sign=self.get_sign(user_id))
                else:
                    elements = []
                    for request in request_list:
                        request_user_id = request["user_id"]
                        request_classroom_id = request["classroom_id"]
                        request_text = request["request_text"]
                        request_datetime = request["datetime"]

                        first_name, last_name = self.user_db.get_user_first_and_last_name(request_user_id)

                        buttons = [
                            {
                                "action": {
                                    "type": "callback",
                                    "label": "Принять",
                                    "payload": {
                                        "text": "accept_request",
                                        "user_id": request_user_id,
                                        "classroom_id": request_classroom_id
                                    }
                                },
                                "color": "positive"
                            },
                            {
                                "action": {
                                    "type": "callback",
                                    "label": "Отклонить",
                                    "payload": {
                                        "text": "cancel_request",
                                        "user_id": request_user_id,
                                        "classroom_id": request_classroom_id
                                    }
                                },
                                "color": "negative"
                            }
                        ]

                        elements.append(
                            {
                                "title": f"{first_name} {last_name}",
                                "description": f"{request_text}\n{request_datetime}",
                                "buttons": buttons
                            }
                        )

                    trans_message = info_message if info_message else "Заявки в этот класс"
                    await self.send_message(user_id, trans_message, template=dumps({
                        "type": "carousel",
                        "elements": elements
                    }))
            else:
                await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES2,
                                            "Ты не можешь принимать заявку из-за "
                                            "своей роли", sign=False)

        elif payload["text"] == "События":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            events = self.event_db.get_all_classroom_events(classroom_id)

            keyboard = Keyboard(inline=True)
            keyboard.add(Callback("Подробнее", payload={
                "text": "event_settings",
                "classroom_id": classroom_id
            }))

            if events:
                event_diary_text = self.get_event_diary_text(events)

                await self.send_message(user_id, event_diary_text, keyboard=keyboard)
            else:
                await self.send_message(user_id, "Пока никаких событий в этом классе не запланировано",
                                        keyboard=keyboard)

        elif payload["text"] == "Назад":
            trans_message = "Назад..."
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES, trans_message,
                                        sign=self.get_sign(user_id))

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_edit_week_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_WEEK_MYCLASSES"""
        if payload is None:
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
            await self.state_transition(user_id, States.S_EDIT_WEEK_MYCLASSES, "Для навигации используй кнопки!👇🏻",
                                        week_type=week_type)

        elif payload["text"] in ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]:
            weekday_meanings_dict = {
                "ПН": "monday",
                "ВТ": "tuesday",
                "СР": "wednesday",
                "ЧТ": "thursday",
                "ПТ": "friday",
                "СБ": "saturday",
                "ВС": "sunday"
            }
            english_weekday = weekday_meanings_dict[payload["text"]]

            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_week(classroom_id, week_type,
                                                                                         english_weekday)

            self.diary_homework_db.update_all_lessons_in_temp_weekday_table(user_id, english_weekday,
                                                                            formatted_day_lessons)

            weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, english_weekday, week_type)
            await self.state_transition(user_id, States.S_EDIT_WEEKDAY_MYCLASSES, weekday_diary_text)

        elif payload["text"] == "Скопировать с эталонного":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, "standard")
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            self.diary_homework_db.update_copy_diary_from_week_into_another_week(classroom_id, week_type,
                                                                                 formatted_week_lessons)

            new_formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, week_type)

            week_diary_text = self.get_week_diary_text(new_formatted_week_lessons, week_type)
            await self.state_transition(user_id, States.S_EDIT_WEEK_MYCLASSES, week_diary_text, week_type=week_type)

        elif payload["text"] == "Главное меню":
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            await self.trans_to_main_menu(user_id)

        elif payload["text"] == "Назад":
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)

            trans_message = "Возвращаемся в меню класса"
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES, trans_message,
                                        sign=self.get_sign(user_id))

    async def s_edit_weekday_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_WEEKDAY_MYCLASSES"""
        if payload is None:
            await self.state_transition(user_id, States.S_EDIT_WEEKDAY_MYCLASSES, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Добавить":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
            weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday, week_type)

            if all(formatted_day_lessons):
                trans_message = f"Максимальное число (12) уроков уже записано!\n\n{weekday_diary_text}"
                await self.state_transition(user_id, States.S_EDIT_WEEKDAY_MYCLASSES, trans_message)
            else:
                new_lesson_index = formatted_day_lessons.index(None) + 1

                trans_message = f"{weekday_diary_text}\n\nНапишите название {new_lesson_index}-го урока" \
                                f" (макс 70 символов):"
                await self.state_transition(user_id, States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES, trans_message)

        elif payload["text"] == "Изменить":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
            weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday, week_type)

            if not any(formatted_day_lessons):
                trans_message = f"Расписание пустое, нечего редактировать\n\n{weekday_diary_text}"
                await self.state_transition(user_id, States.S_EDIT_WEEKDAY_MYCLASSES, trans_message)
            else:
                trans_message = f"{weekday_diary_text}\n\nВпишите номер урока и его новое название в " \
                                f"следующем формате: номер_урока. новое_название (например,\n7. Алгебра)"
                await self.state_transition(user_id, States.S_EDIT_LESSON_WEEKDAY_MYCLASSES, trans_message)

        elif payload["text"] == "Удалить урок":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            if not any(formatted_day_lessons):
                weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday, week_type)

                trans_message = f"Расписание на этот день и так пустое\n\n{weekday_diary_text}"
            else:
                last_lesson_index = formatted_day_lessons.index(None) if None in formatted_day_lessons else 12
                deleted_lesson = formatted_day_lessons[last_lesson_index - 1]
                self.diary_homework_db.update_delete_lesson_from_temp_table(user_id, last_lesson_index)

                new_formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday, week_type)

                trans_message = f"Удалён {last_lesson_index}. {deleted_lesson}\n\n{weekday_diary_text}"

            await self.state_transition(user_id, States.S_EDIT_WEEKDAY_MYCLASSES, trans_message)

        elif payload["text"] == "Удалить всё":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            if not any(formatted_day_lessons):
                weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday, week_type)

                trans_message = f"Расписание на этот день и так пустое\n\n{weekday_diary_text}"
                await self.state_transition(user_id, States.S_EDIT_WEEKDAY_MYCLASSES, trans_message)
            else:
                self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)
                new_formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday, week_type)

                trans_message = f"Все уроки удалены!\n\n{weekday_diary_text}"
                await self.state_transition(user_id, States.S_EDIT_WEEKDAY_MYCLASSES, trans_message)

        elif payload["text"] == "Сохранить":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            self.diary_homework_db.update_weekday_in_week(classroom_id, formatted_day_lessons, week_type, weekday)
            self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)
            self.diary_homework_db.update_delete_weekday_from_temp_table(user_id)

            formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, week_type)
            diary_text = self.get_week_diary_text(formatted_week_lessons, week_type)
            weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday, week_type)

            await self.notify_change_diary(classroom_id, weekday_diary_text, homework=False, without_user_ids=[user_id])
            trans_message = f"{diary_text}\n\nВсе изменения сохранены!"
            await self.state_transition(user_id, States.S_EDIT_WEEK_MYCLASSES, trans_message, week_type=week_type)

        elif payload["text"] == "Главное меню":
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            await self.trans_to_main_menu(user_id)

        elif payload["text"] == "Отменить":
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, week_type)
            diary_text = self.get_week_diary_text(formatted_week_lessons, week_type)

            self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)
            self.diary_homework_db.update_delete_weekday_from_temp_table(user_id)

            trans_message = f"{diary_text}\n\nВсе изменения отменены!"
            await self.state_transition(user_id, States.S_EDIT_WEEK_MYCLASSES, trans_message, week_type=week_type)

    async def s_add_new_lesson_weekday_my_classes_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES"""
        if payload is None:
            if len(message) > 70:
                trans_message = "Длина названия превышает 70 символов!"
                await self.state_transition(user_id, States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES, trans_message)
            else:
                formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                new_lesson_index = formatted_day_lessons.index(None) + 1
                self.diary_homework_db.update_add_new_lesson_into_temp_table(user_id, message, new_lesson_index)

                new_formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
                week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
                new_weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday, week_type)

                if new_lesson_index <= 11:
                    trans_message = f"Урок добавлен!\n\n{new_weekday_diary_text}\n\n" \
                                    f"Напишите название {new_lesson_index + 1}-го урока (макс 70 символов):"
                    await self.state_transition(user_id, States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES, trans_message)
                else:
                    trans_message = f"Урок добавлен!\n\n{new_weekday_diary_text}.\n\nДостигнут лимит!"
                    await self.state_transition(user_id, States.S_EDIT_WEEKDAY_MYCLASSES, trans_message)

        elif payload["text"] == "Добавить":
            trans_message = "Ты уже в режиме добавления уроков"
            await self.state_transition(user_id, States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES, trans_message)

        elif payload["text"]:
            await self.s_edit_weekday_my_classes_handler(user_id, payload)

    async def s_edit_lesson_weekday_my_classes_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_EDIT_LESSON_WEEKDAY_MYCLASSES"""
        if payload is None:
            ask_message = "Впишите номер урока и его новое название в следующем формате: " \
                          "номер_урока. новое_название (например,\n7. Алгебра)"

            if ". " in message:
                lesson_index, lesson_name = message.split(". ", 1)

                formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                max_lesson_index = formatted_day_lessons.index(None) if None in formatted_day_lessons else 12

                if lesson_index.isdigit():
                    if 0 < int(lesson_index) <= max_lesson_index:
                        if 0 < len(lesson_name) <= 70:
                            self.diary_homework_db.update_lesson_in_temp_table(user_id, lesson_name, lesson_index)

                            new_formatted_day_lessons = \
                                self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
                            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
                            weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday,
                                                                             week_type)

                            trans_message = f"Название урока изменено!\n\n{weekday_diary_text}\n\n{ask_message}"
                            await self.state_transition(user_id, States.S_EDIT_LESSON_WEEKDAY_MYCLASSES, trans_message)
                        else:
                            trans_message = f"Название урока не может быть пустым или быть длиннее " \
                                            f"70 символов\n\n{ask_message}"
                            await self.state_transition(user_id, States.S_EDIT_LESSON_WEEKDAY_MYCLASSES, trans_message)
                    else:
                        trans_message = f"Урока с таким номером нет.\n\n{ask_message}"
                        await self.state_transition(user_id, States.S_EDIT_LESSON_WEEKDAY_MYCLASSES, trans_message)
                else:
                    trans_message = f"Неверный формат записи\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_EDIT_LESSON_WEEKDAY_MYCLASSES, trans_message)
            else:
                trans_message = f"Неверный формат записи\n\n{ask_message}"
                await self.state_transition(user_id, States.S_EDIT_LESSON_WEEKDAY_MYCLASSES, trans_message)

        elif payload["text"] == "Изменить":
            trans_message = "Ты уже в режиме редактирования уроков"
            await self.state_transition(user_id, States.S_EDIT_LESSON_WEEKDAY_MYCLASSES, trans_message)

        elif payload["text"]:
            await self.s_edit_weekday_my_classes_handler(user_id, payload)

    async def s_edit_homework_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_HOMEWORK_MYCLASSES"""
        if payload is None:
            await self.state_transition(user_id, States.S_EDIT_HOMEWORK_MYCLASSES,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] in ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]:
            weekday_meanings_dict = {
                "ПН": "monday",
                "ВТ": "tuesday",
                "СР": "wednesday",
                "ЧТ": "thursday",
                "ПТ": "friday",
                "СБ": "saturday",
                "ВС": "sunday"
            }
            english_weekday = weekday_meanings_dict[payload["text"]]

            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_day_lessons_diary = self.diary_homework_db.get_weekday_lessons_from_week(classroom_id,
                                                                                               week_type,
                                                                                               english_weekday)
            if any(formatted_day_lessons_diary):
                formatted_day_lessons_homework = self.diary_homework_db.get_weekday_lessons_from_week(classroom_id,
                                                                                                      week_type,
                                                                                                      english_weekday,
                                                                                                      homework=True)
                self.diary_homework_db.update_all_lessons_in_temp_weekday_table(user_id, english_weekday,
                                                                                formatted_day_lessons_homework)
                weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons_diary, english_weekday,
                                                                 week_type,
                                                                 formatted_day_lessons_homework)

                help_text = "\n\nВпиши новое домашнее задание в формате: номер_урока. дз\n(Например,\n2. " \
                            "Упр 23, стр 6)\n\nЕсли нужно удалить дз с урока, то просто впиши одно число - номер урока"
                await self.state_transition(user_id, States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES,
                                            weekday_diary_text + help_text)
            else:
                trans_message = "Расписание на этот день пустое (сначала отредактируй расписание)"
                await self.state_transition(user_id, States.S_EDIT_HOMEWORK_MYCLASSES, trans_message)

        elif payload["text"] == "Назад":
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)

            trans_message = "Возвращение в меню класса"
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES, trans_message,
                                        sign=self.get_sign(user_id))

        elif payload["text"] == "Главное меню":
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            await self.trans_to_main_menu(user_id)

    async def s_edit_homework_weekday_my_classes_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES"""
        ask_message = "\n\nВпиши новое домашнее задание в формате: номер_урока. дз\n(Например,\n2. Упр 23, стр 6)" \
                      "\n\nЕсли нужно удалить дз с урока, то просто впиши одно число - номер урока"

        if payload is None:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
            formatted_day_lessons_diary = self.diary_homework_db.get_weekday_lessons_from_week(classroom_id,
                                                                                               week_type,
                                                                                               weekday)
            if message.isdigit():
                lesson_index = int(message)

                max_lessons_index = formatted_day_lessons_diary.index(None) \
                    if None in formatted_day_lessons_diary else 12

                if 0 < lesson_index <= max_lessons_index:
                    self.diary_homework_db.update_lesson_in_temp_table(user_id, "", lesson_index)
                    formatted_day_lessons_homework = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)

                    weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons_diary, weekday, week_type,
                                                                     formatted_day_lessons_homework)
                    await self.state_transition(user_id, States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES,
                                                f"Дз с {lesson_index}-го "
                                                f"урока удалено!\n\n"
                                                f"{weekday_diary_text}\n\n"
                                                f"{ask_message}")
                else:
                    trans_message = f"Урока с таким номером нет\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES, trans_message)
            elif ". " in message:
                lesson_index, homework_text = message.split(". ", 1)

                max_lesson_index = formatted_day_lessons_diary.index(None) \
                    if None in formatted_day_lessons_diary else 12

                if lesson_index.isdigit():
                    if 0 < int(lesson_index) <= max_lesson_index:
                        if 0 < len(homework_text) <= 200:
                            self.diary_homework_db.update_lesson_in_temp_table(user_id, homework_text, lesson_index)

                            new_formatted_day_homework = \
                                self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                            weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons_diary, weekday,
                                                                             week_type,
                                                                             new_formatted_day_homework)

                            trans_message = f"Дз обновлено!\n\n{weekday_diary_text}\n\n{ask_message}"
                            await self.state_transition(user_id, States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES,
                                                        trans_message)
                        else:
                            trans_message = f"Текст дз не может быть пустым или быть длиннее " \
                                            f"200 символов\n\n{ask_message}"
                            await self.state_transition(user_id, States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES,
                                                        trans_message)
                    else:
                        trans_message = f"Урока с таким номером нет.\n\n{ask_message}"
                        await self.state_transition(user_id, States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES, trans_message)
                else:
                    trans_message = f"Неверный формат записи\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES, trans_message)
            else:
                trans_message = f"Неверный формат записи\n\n{ask_message}"
                await self.state_transition(user_id, States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES, trans_message)

        elif payload["text"] == "Очистить всё дз":
            self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
            formatted_day_lessons_diary = self.diary_homework_db.get_weekday_lessons_from_week(classroom_id,
                                                                                               week_type,
                                                                                               weekday)
            formatted_day_lessons_homework = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)

            dairy_homework_text = self.get_weekday_diary_text(formatted_day_lessons_diary, weekday, week_type,
                                                              formatted_day_lessons_homework)
            await self.state_transition(user_id, States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES,
                                        f"Всё дз с этого дня удалено!\n\n"
                                        f"{dairy_homework_text}\n\n"
                                        f"{ask_message}")

        elif payload["text"] == "Сохранить":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_day_lessons_homework = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            self.diary_homework_db.update_weekday_in_week(classroom_id, formatted_day_lessons_homework, week_type,
                                                          weekday, homework=True)
            self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)
            self.diary_homework_db.update_delete_weekday_from_temp_table(user_id)

            formatted_day_lessons_diary = self.diary_homework_db.get_weekday_lessons_from_week(classroom_id, week_type,
                                                                                               weekday)
            formatted_week_lessons_diary = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id,
                                                                                                 week_type)
            formatted_week_lessons_homework = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id,
                                                                                                    week_type,
                                                                                                    homework=True)
            weekday_diary_homework_text = self.get_weekday_diary_text(formatted_day_lessons_diary, weekday, week_type,
                                                                      formatted_day_lessons_homework, is_edit=False)
            diary_homework_text = self.get_week_diary_text(formatted_week_lessons_diary, week_type,
                                                           formatted_week_lessons_homework)

            await self.notify_change_diary(classroom_id, weekday_diary_homework_text, homework=True,
                                           without_user_ids=[user_id])
            trans_message = f"{diary_homework_text}\n\nДомашнее задание изменено!"
            await self.state_transition(user_id, States.S_EDIT_HOMEWORK_MYCLASSES, trans_message)

        elif payload["text"] == "Отменить":
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_week_lessons_diary = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id,
                                                                                                 week_type)
            formatted_week_lessons_homework = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id,
                                                                                                    week_type,
                                                                                                    homework=True)
            diary_homework_text = self.get_week_diary_text(formatted_week_lessons_diary, week_type,
                                                           formatted_week_lessons_homework)

            self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)
            self.diary_homework_db.update_delete_weekday_from_temp_table(user_id)

            trans_message = f"{diary_homework_text}\n\nВсе изменения отменены!"
            await self.state_transition(user_id, States.S_EDIT_HOMEWORK_MYCLASSES, trans_message)

        elif payload["text"] == "Главное меню":
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            await self.trans_to_main_menu(user_id)

    @staticmethod
    def get_week_diary_text(formatted_week_lessons_diary: list, week_type: str,
                            formatted_week_lessons_homework=None) -> str:
        """Returns text of week's diary"""
        week_diary = []

        weekdays = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА", "ВОСКРЕСЕНЬЕ"]
        if week_type in ("current", "next"):
            month_dict = {
                1: "Янв",
                2: "Фев",
                3: "Мар",
                4: "Апр",
                5: "Май",
                6: "Июн",
                7: "Июл",
                8: "Авг",
                9: "Сен",
                10: "Окт",
                11: "Ноя",
                12: "Дек",
            }

            datetime_now = datetime.now()

            if week_type == "next":
                datetime_now = datetime_now + timedelta(days=7)
            weekday_number_now = datetime_now.weekday()

            for day_count in range(7):
                replaced_datetime = datetime_now + timedelta(days=-weekday_number_now + day_count)
                str_date = f"{replaced_datetime.day} {month_dict[replaced_datetime.month]}"
                weekdays[day_count] = f"{weekdays[day_count]}, {str_date}"

        if formatted_week_lessons_homework is None:
            for weekday_name, weekday_diary_tuple in zip(weekdays, formatted_week_lessons_diary):
                if not any(weekday_diary_tuple):
                    week_diary.append(weekday_name + "\n" + "1. ПУСТО")
                else:
                    if None in weekday_diary_tuple:
                        weekday_diary_tuple_without_empty = weekday_diary_tuple[:weekday_diary_tuple.index(None)]
                    else:
                        weekday_diary_tuple_without_empty = weekday_diary_tuple

                    day_lessons = [f"{i}. {weekday_diary_tuple_without_empty[i - 1]}"
                                   for i in range(1, len(weekday_diary_tuple_without_empty) + 1)]
                    week_diary.append(weekday_name + "\n" + "\n".join(day_lessons))
        else:
            for weekday_name, weekday_diary_tuple, weekday_homework_tuple in zip(weekdays, formatted_week_lessons_diary,
                                                                                 formatted_week_lessons_homework):
                if not any(weekday_homework_tuple):
                    week_diary.append(weekday_name + "\n" + "1. ПУСТО")
                else:
                    day_lessons = []
                    for i in range(len(weekday_homework_tuple)):
                        if weekday_homework_tuple[i] is not None:
                            lesson_text = f"✏{weekday_diary_tuple[i]}: {weekday_homework_tuple[i]}"
                            day_lessons.append(lesson_text)

                    week_diary.append(weekday_name + "\n" + "\n".join(day_lessons))

        return "\n\n".join(week_diary)

    @staticmethod
    def get_weekday_diary_text(formatted_days_diary: tuple, weekday: str, week_type: str,
                               formatted_days_homework=None, is_edit=True) -> str:
        """Returns text of weekday's diary"""
        weekday_meanings_dict = {
            "monday": ("Понедельник", 0),
            "tuesday": ("Вторник", 1),
            "wednesday": ("Среда", 2),
            "thursday": ("Четверг", 3),
            "friday": ("Пятница", 4),
            "saturday": ("Суббота", 5),
            "sunday": ("Воскресение", 6),
        }
        weekday_russian = weekday_meanings_dict[weekday][0]
        weekday_index = weekday_meanings_dict[weekday][1]

        if week_type in ("current", "next"):
            month_dict = {
                1: "Янв",
                2: "Фев",
                3: "Мар",
                4: "Апр",
                5: "Май",
                6: "Июн",
                7: "Июл",
                8: "Авг",
                9: "Сен",
                10: "Окт",
                11: "Ноя",
                12: "Дек",
            }

            datetime_now = datetime.now()
            if week_type == "next":
                datetime_now = datetime_now + timedelta(days=7)
            weekday_number_now = datetime_now.weekday()
            weekday_date = datetime_now + timedelta(days=-weekday_number_now + weekday_index)
            weekday_russian = f"{weekday_russian}, {weekday_date.day} {month_dict[weekday_date.month]}"

        if None in formatted_days_diary:
            weekday_without_empty = formatted_days_diary[:formatted_days_diary.index(None)]
        else:
            weekday_without_empty = formatted_days_diary

        if formatted_days_homework is None:
            if not any(formatted_days_diary):
                weekday_diary = ["1. ПУСТО"]
            else:
                weekday_diary = [f"{i}. {weekday_without_empty[i - 1]}"
                                 for i in range(1, len(weekday_without_empty) + 1)]
        else:
            weekday_diary = []
            if not any(formatted_days_homework) and not is_edit:
                weekday_diary.append("1. ПУСТО")
            elif is_edit:
                for i in range(1, len(weekday_without_empty) + 1):
                    lesson_text = f"{i}. {weekday_without_empty[i - 1]}"
                    if formatted_days_homework[i - 1] is not None:
                        lesson_text += f": {formatted_days_homework[i - 1]}"
                    weekday_diary.append(lesson_text)
            else:
                for i in range(len(formatted_days_homework)):
                    if formatted_days_homework[i] is not None:
                        lesson_text = f"✏{weekday_without_empty[i]}: {formatted_days_homework[i]}"
                        weekday_diary.append(lesson_text)

        return weekday_russian + "\n" + "\n".join(weekday_diary)
