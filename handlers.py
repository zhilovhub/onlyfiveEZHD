from supporting_functions import *

from classroom import ClassroomCommands
from users import UserDataCommands
from technical_support import TechnicalSupportCommands
from diary_homework import DiaryHomeworkCommands
from states import States


class StateHandlers(SupportingFunctions):
    """Handles states"""

    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id)
        self.user_db = user_db
        self.classroom_db = classroom_db
        self.technical_support_db = technical_support_db
        self.diary_homework_db = diary_homework_db

    def s_nothing_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_NOTHING"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("menu"))

        elif payload["text"] == "Найти класс":
            self.send_message(user_id, "Отправьте ссылку-приглашение или id класса в "
                                       "формате #id (например, #1223)", self.get_keyboard("just_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_FIND_CLASS.value)

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
                    self.classroom_db.get_information_of_classroom(classroom_id)

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
            self.send_message(user_id, "Опишите свой вопрос...",
                              self.get_keyboard("cancel_send"))
            self.user_db.set_user_dialog_state(user_id, States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE.value)

        elif payload["text"] == "enter_the_classroom":
            classroom_id = payload["classroom_id"]
            classroom_name = self.classroom_db.get_classroom_name(classroom_id)
            self.classroom_db.update_user_customize_classroom(user_id, classroom_id)

            self.send_message(user_id, f"Ты в классе {classroom_name}", self.get_keyboard("my_class_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES.value)

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
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("yes_no_cancel_back"))

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
                    self.classroom_db.get_information_of_classroom(classroom_id)

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
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("submit_back"))

        elif payload["text"] == "Принять":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            self.classroom_db.update_user_customize_classroom(user_id, "null")
            self.classroom_db.update_classroom_created(classroom_id, True)
            self.diary_homework_db.insert_classroom_id(classroom_id)

            next_state, keyboard_type, messages = States.get_next_state_config(States.S_SUBMIT_CLASSCREATE)
            self.send_message(user_id, "Поздравляю! Класс создан", self.get_keyboard("menu"))

            self.state_transition(user_id, next_state, keyboard_type, messages)

        elif payload["text"] == "Отклонить":
            next_state, keyboard_type, messages = States.get_next_state_config(States.S_ENTER_ACCESS_CLASSCREATE)
            self.state_transition(user_id, next_state, keyboard_type, messages)

    def s_enter_technical_support_message_handler(self, user_id: int, message: str) -> None:
        """Handling States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE"""
        if message == "Отменить":
            self.cancel_entering_technical_support_message(user_id)

        elif message == "Отправить":
            next_state, keyboard_type, messages = States.get_next_state_config(States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE)
            self.state_transition(user_id, next_state, keyboard_type, messages)

        else:
            user_message = self.technical_support_db.get_message(user_id) + "\n"
            user_message += message
            self.technical_support_db.insert_message(user_id, user_message)

    def s_in_class_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_IN_CLASS_MYCLASSES"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("my_class_menu"))

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

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

    def s_edit_week_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_WEEK_MYCLASSES"""
        if payload is None:
            week_type = self.diary_homework_db.get_week_type_from_temp_table(user_id)
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard(f"edit_{week_type}_week"))

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
            self.classroom_db.update_user_customize_classroom(user_id, "null")
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
            self.classroom_db.update_user_customize_classroom(user_id, "null")
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

    def s_find_class_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_FIND_CLASS"""
        if payload is None:
            classroom_id = None
            stripped_message = message.strip()

            if fullmatch(r"#\d+", stripped_message):
                classroom_id = int(stripped_message[1:])

            elif search(r"onlyfiveEZHD/invite_link/\d+", stripped_message):
                result = search(r"onlyfiveEZHD/invite_link/\d+", stripped_message)
                classroom_id = int(stripped_message[result.start():result.end()].split("/")[-1])

            if classroom_id:
                existing_classroom_ids = self.classroom_db.get_list_of_classroom_ids()

                if classroom_id in existing_classroom_ids:
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_callback_button("Посмотреть", payload={
                        "text": "look_at_the_classroom", "classroom_id": classroom_id
                    })

                    classroom_name, school_name, access, description = \
                        self.classroom_db.get_information_of_classroom(classroom_id)
                    members_dictionary = self.classroom_db.get_list_of_classroom_users(classroom_id)

                    for member_user_id in members_dictionary.keys():
                        if user_id == member_user_id:
                            user_in_classroom_text = "Вы состоите в этом классе ✔"
                            break
                    else:
                        user_in_classroom_text = "Вы не состоите в этом классе ❌"

                    self.send_message(user_id, f"#{classroom_id}\n"
                                               f"Класс: {classroom_name}\n"
                                               f"Школа: {school_name}\n"
                                               f"Описание: {description}\n"
                                               f"Могут ли все участники приглашать: {'Да' if access else 'Нет'}\n"
                                               f"Участники: {len(members_dictionary)}\n\n"
                                               f"{user_in_classroom_text}", keyboard.get_keyboard())
                else:
                    self.send_message(user_id, f"Класса с id {classroom_id} не существует!",
                                      self.get_keyboard("just_menu"))

            else:
                self.send_message(user_id, "Неверный формат записи\n\nОтправьте ссылку-приглашение или id класса в "
                                           "формате #id (например, #1223)", self.get_keyboard("just_menu"))

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
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

    def cancel_entering_technical_support_message(self, user_id: int) -> None:
        """Cancel creating technical support message and set state to States.S_NOTHING"""
        self.send_message(user_id, "Отправка обращения в тех. поддержку отменена", self.get_keyboard("menu"))
        self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

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


class CallbackPayloadHandlers(StateHandlers):
    """Handles callback payloads"""

    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db,
                         classroom_db=classroom_db, technical_support_db=technical_support_db,
                         diary_homework_db=diary_homework_db)

    def p_enter_the_classroom_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with text: enter_the_classroom"""
        if current_dialog_state == States.S_NOTHING.value:
            self.s_nothing_handler(user_id, payload)
        else:
            self.send_message(user_id, "Закончи текущее действие или выйди в главное меню")

    def p_edit_week_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payloads with text: standard | current | next"""
        if current_dialog_state == States.S_IN_CLASS_MYCLASSES.value:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            if classroom_id == payload["classroom_id"]:
                self.s_in_class_my_classes_handler(user_id, payload)
            else:
                self.send_message(user_id, "Это расписание не того класса, в котором ты находишься!")
        else:
            self.send_message(user_id, "Ты должен находиться в меню класса, расписание которого собираешься изменить!")
