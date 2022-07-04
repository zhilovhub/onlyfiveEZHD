from supporting_functions import *


class MyClassesHandlers(SupportingFunctions):
    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db)

    def s_in_class_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_IN_CLASS_MYCLASSES"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("my_class_menu"))

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

        elif payload["text"] == "Ещё":
            self.send_message(user_id, "Другое меню класса", self.get_keyboard("my_class_menu2"))
            self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES2.value)

        elif payload["text"] == "Настройки":
            self.send_message(user_id, "Настройки класса\n\nКоличество настроек зависит от твоей роли в этом классе!",
                              self.get_keyboard("classroom_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_CLASSROOM_SETTINGS.value)

        elif payload["text"] == "Участники":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
            members_text = self.get_members_text(roles_dictionary)

            keyboard = VkKeyboard(inline=True)
            keyboard.add_callback_button("Настройки",
                                         payload={
                                             "text": "enter_members_settings",
                                             "classroom_id": classroom_id
                                         })

            self.send_message(user_id, members_text, keyboard.get_keyboard())

        elif payload["text"] in ["Расписание эталонное", "Расписание текущее", "Расписание будущее"]:
            payload_meanings_dict = {
                "Расписание эталонное": ("edit_standard", "standard", "Эталонное расписание\n\nМожно копировать в "
                                                                      "текущее и будущее расписание.\nБудет "
                                                                      "автоматически устанавливаться в будущее "
                                                                      "расписание каждую неделю\n\n"),
                "Расписание текущее": ("edit_current", "current", "Расписание на текущую неделю\n\n"),
                "Расписание будущее": ("edit_next", "next", "Расписание на следующую неделю\n\n")
            }
            callback_payload_text = payload_meanings_dict[payload["text"]][0]
            week_type = payload_meanings_dict[payload["text"]][1]
            help_text = payload_meanings_dict[payload["text"]][2]

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, week_type)
            diary_text = self.get_week_diary_text(formatted_week_lessons)

            keyboard = VkKeyboard(inline=True)
            keyboard.add_callback_button("Изменить",
                                         payload={
                                             "text": callback_payload_text,
                                             "classroom_id": classroom_id
                                         })

            self.send_message(user_id, help_text + diary_text, keyboard.get_keyboard())

        elif payload["text"] in ("edit_standard", "edit_current", "edit_next"):
            payload_meanings_dict = {
                "edit_standard": ("standard", "эталонного"),
                "edit_current": ("current", "текущего"),
                "edit_next": ("next", "будущего")
            }
            week_type = payload_meanings_dict[payload["text"]][0]
            week_type_russian = payload_meanings_dict[payload["text"]][1]

            self.diary_homework_db.insert_row_into_temp_weekday_table(user_id, week_type)
            self.send_message(user_id, f"Редактирование {week_type_russian} расписания\n\nИзменения "
                                       f"увидят ВСЕ участники класса!",
                              self.get_keyboard(f"edit_{week_type}_week"))
            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_WEEK_MYCLASSES.value)

        elif payload["text"] == "enter_members_settings":
            self.send_message(user_id, "Настройки участников класса\n\n"
                                       "Здесь можно создавать и настраивать роли, удалять и приглашать участников!",
                              self.get_keyboard("members_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MEMBERS_SETTINGS.value)

    def s_in_class_my_classes2_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_IN_CLASS_MYCLASSES2"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("my_class_menu2"))

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Назад...", self.get_keyboard("my_class_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_edit_week_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_WEEK_MYCLASSES"""
        if payload is None:
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻",
                              self.get_keyboard(f"edit_{week_type}_week"))

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

            if None in formatted_day_lessons:
                formatted_day_lessons = formatted_day_lessons[:formatted_day_lessons.index(None)]

            weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, english_weekday)

            self.diary_homework_db.update_all_lessons_in_temp_weekday_table(user_id, english_weekday,
                                                                            formatted_day_lessons)
            self.send_message(user_id, weekday_diary_text, self.get_keyboard(f"edit_weekday_default"))
            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_WEEKDAY_MYCLASSES.value)

        elif payload["text"] == "Скопировать с эталонного":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, "standard")
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            self.diary_homework_db.update_copy_diary_from_week_into_another_week(classroom_id, week_type,
                                                                                 formatted_week_lessons)

            new_formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, week_type)
            week_diary_text = self.get_week_diary_text(new_formatted_week_lessons)

            self.send_message(user_id, f"Расписание скопировано с эталонного!\n\n{week_diary_text}",
                              self.get_keyboard(f"edit_{week_type}_week"))

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в меню класса", self.get_keyboard("my_class_menu"))
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES.value)

    def s_edit_weekday_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_WEEKDAY_MYCLASSES"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("edit_weekday_default"))

        elif payload["text"] == "Добавить":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday)

            if all(formatted_day_lessons):
                self.send_message(user_id, f"Максимальное число (12) уроков уже записано!\n\n{weekday_diary_text}",
                                  self.get_keyboard(f"edit_weekday_default"))
            else:
                new_lesson_index = formatted_day_lessons.index(None) + 1

                self.send_message(user_id, f"{weekday_diary_text}\n\nНапишите название {new_lesson_index}-го урока"
                                           f" (макс 70 символов):",
                                  self.get_keyboard(f"edit_weekday_add"))
                self.user_db.set_user_dialog_state(user_id, States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES.value)

        elif payload["text"] == "Изменить":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
            weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday)

            if not any(formatted_day_lessons):
                self.send_message(user_id, f"Расписание пустое, нечего редактировать\n\n{weekday_diary_text}",
                                  self.get_keyboard(f"edit_weekday_default"))
            else:
                self.send_message(user_id, f"{weekday_diary_text}\n\nВпишите номер урока и его новое название в "
                                           f"следующем формате: номер_урока. новое_название (например,\n7. Алгебра)",
                                  self.get_keyboard(f"edit_weekday_redact"))
                self.user_db.set_user_dialog_state(user_id, States.S_EDIT_LESSON_WEEKDAY_MYCLASSES.value)

        elif payload["text"] == "Удалить урок":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)

            if not any(formatted_day_lessons):
                weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday)
                self.send_message(user_id, f"Расписание на этот день и так пустое\n\n{weekday_diary_text}",
                                  self.get_keyboard(f"edit_weekday_default"))

            else:
                last_lesson_index = formatted_day_lessons.index(None) if None in formatted_day_lessons else 12
                deleted_lesson = formatted_day_lessons[last_lesson_index - 1]
                self.diary_homework_db.update_delete_lesson_from_temp_table(user_id, last_lesson_index)

                new_formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday)

                self.send_message(user_id, f"Удалён {last_lesson_index}. {deleted_lesson}\n\n{weekday_diary_text}",
                                  self.get_keyboard(f"edit_weekday_default"))

            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_WEEKDAY_MYCLASSES.value)

        elif payload["text"] == "Удалить всё":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)

            if not any(formatted_day_lessons):
                weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday)
                self.send_message(user_id, f"Расписание на этот день и так пустое\n\n{weekday_diary_text}",
                                  self.get_keyboard(f"edit_weekday_default"))

            else:
                self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)
                new_formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday)

                self.send_message(user_id, f"Все уроки удалены!\n\n{weekday_diary_text}",
                                  self.get_keyboard(f"edit_weekday_default"))

        elif payload["text"] == "Сохранить":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)

            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            self.diary_homework_db.update_weekday_in_week(classroom_id, formatted_day_lessons, week_type, weekday)
            self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)
            self.diary_homework_db.update_delete_weekday_from_temp_table(user_id)

            formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, week_type)
            diary_text = self.get_week_diary_text(formatted_week_lessons)

            self.send_message(user_id, f"{diary_text}\n\nВсе изменения сохранены!",
                              self.get_keyboard(f"edit_{week_type}_week"))
            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_WEEK_MYCLASSES.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

        elif payload["text"] == "Отменить":
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_week_lessons = self.diary_homework_db.get_all_days_lessons_from_week(classroom_id, week_type)
            diary_text = self.get_week_diary_text(formatted_week_lessons)

            self.send_message(user_id, f"{diary_text}\n\nВсе изменения отменены!",
                              self.get_keyboard(f"edit_{week_type}_week"))
            self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)
            self.diary_homework_db.update_delete_weekday_from_temp_table(user_id)
            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_WEEK_MYCLASSES.value)

    def s_add_new_lesson_weekday_my_classes_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES"""
        if payload is None:
            if len(message) > 70:
                self.send_message(user_id, "Длина названия превышает 70 символов!",
                                  self.get_keyboard("edit_weekday_add"))
            else:
                formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                new_lesson_index = formatted_day_lessons.index(None) + 1
                self.diary_homework_db.update_add_new_lesson_into_temp_table(user_id, message, new_lesson_index)

                new_formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
                new_weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday)

                if new_lesson_index <= 11:
                    self.send_message(user_id, f"Урок добавлен!\n\n{new_weekday_diary_text}\n\n"
                                               f"Напишите название {new_lesson_index + 1}-го урока (макс 70 символов):",
                                      self.get_keyboard("edit_weekday_add"))
                else:
                    self.send_message(user_id, f"Урок добавлен!\n\n{new_weekday_diary_text}.\n\nДостигнут лимит!",
                                      self.get_keyboard(f"edit_weekday_default"))
                    self.user_db.set_user_dialog_state(user_id, States.S_EDIT_WEEKDAY_MYCLASSES.value)

        elif payload["text"] == "Добавить":
            self.send_message(user_id, "Ты уже в режиме добавления уроков",
                              self.get_keyboard(f"edit_weekday_add"))

        elif payload["text"]:
            self.s_edit_weekday_my_classes_handler(user_id, payload)

    def s_edit_lesson_weekday_my_classes_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_EDIT_LESSON_WEEKDAY_MYCLASSES"""
        if payload is None:
            ask_message = "Впишите номер урока и его новое название в следующем формате: " \
                          "номер_урока. новое_название (например,\n7. Алгебра)"

            if ". " in message:
                lesson_index, lesson_name = message.split(". ")

                formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                max_lesson_index = formatted_day_lessons.index(None) if None in formatted_day_lessons else 12

                if lesson_index.isdigit():
                    if 0 < int(lesson_index) <= max_lesson_index:
                        if 0 < len(lesson_name) <= 70:
                            self.diary_homework_db.update_lesson_in_temp_table(user_id, lesson_name, lesson_index)

                            new_formatted_day_lessons = \
                                self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                            weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
                            weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday)

                            self.send_message(user_id, f"Название урока изменено!\n\n{weekday_diary_text}\n\n"
                                                       f"{ask_message}",
                                              self.get_keyboard("edit_weekday_redact"))
                        else:
                            self.send_message(user_id, f"Название урока не может быть пустым или быть длиннее "
                                                       f"70 символов\n\n{ask_message}",
                                              self.get_keyboard("edit_weekday_redact"))
                    else:
                        self.send_message(user_id, f"Урока с таким номером нет.\n\n{ask_message}",
                                          self.get_keyboard("edit_weekday_redact"))
                else:
                    self.send_message(user_id,
                                      f"Неверный формат записи\n\n{ask_message}",
                                      self.get_keyboard("edit_weekday_redact"))
            else:
                self.send_message(user_id, f"Неверный формат записи\n\n{ask_message}",
                                  self.get_keyboard("edit_weekday_redact"))

        elif payload["text"] == "Изменить":
            self.send_message(user_id, "Ты уже в режиме редактирования уроков",
                              self.get_keyboard("edit_weekday_redact"))

        elif payload["text"]:
            self.s_edit_weekday_my_classes_handler(user_id, payload)

    @staticmethod
    def get_week_diary_text(formatted_week: list) -> str:
        """Returns text of week's diary"""
        week_diary = []

        weekdays = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        for weekday_name, weekday_tuple in zip(weekdays, formatted_week):
            if not any(weekday_tuple):
                week_diary.append(weekday_name + "\n" + "1. ПУСТО")
            else:
                if None in weekday_tuple:
                    weekday_tuple_without_empty = weekday_tuple[:weekday_tuple.index(None)]
                else:
                    weekday_tuple_without_empty = weekday_tuple

                day_lessons = [f"{i}. {weekday_tuple_without_empty[i - 1]}"
                               for i in range(1, len(weekday_tuple_without_empty) + 1)]
                week_diary.append(weekday_name + "\n" + "\n".join(day_lessons))

        return "\n\n".join(week_diary)

    @staticmethod
    def get_weekday_diary_text(formatted_days: tuple, weekday: str) -> str:
        """Returns text of weekday's diary"""
        weekday_meanings_dict = {
            "monday": "Понедельник",
            "tuesday": "Вторник",
            "wednesday": "Среда",
            "thursday": "Четверг",
            "friday": "Пятница",
            "saturday": "Суббота",
            "sunday": "Воскресение"
        }
        weekday_russian = weekday_meanings_dict[weekday]

        if not any(formatted_days):
            weekday_diary = ["1. ПУСТО"]
        else:
            if None in formatted_days:
                weekday_without_empty = formatted_days[:formatted_days.index(None)]
            else:
                weekday_without_empty = formatted_days
            weekday_diary = [f"{i}. {weekday_without_empty[i - 1]}" for i in range(1, len(weekday_without_empty) + 1)]

        return weekday_russian + "\n" + "\n".join(weekday_diary)
