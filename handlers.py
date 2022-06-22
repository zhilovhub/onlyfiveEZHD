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

        elif payload["text"] == "Расписание эталонное":
            keyboard = VkKeyboard(inline=True)
            keyboard.add_callback_button("Изменить", payload={"text": "Изменить эталонное расписание",
                                                     "classroom_id": self.classroom_db.get_customizing_classroom_id(user_id)})

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            raw_week_lessons = self.diary_homework_db.get_all_days_lessons_from_standard_week(classroom_id)
            formatted_week_lessons = []

            for i in range(0, len(raw_week_lessons), 12):
                formatted_week_lessons.append(raw_week_lessons[i:i+12])
            diary = self.get_week_diary_text(formatted_week_lessons)

            self.send_message(user_id, "Эталонное расписание\n\nМожно копировать в текущее "
                                       "и будущее расписание.\nБудет автоматически устанавливаться в будущее "
                                       "расписание каждую неделю\n\n" + diary, keyboard.get_keyboard())

        elif payload["text"] == "Изменить эталонное расписание":
            self.send_message(user_id, "Редактирование эталонного расписания\n\nИзменения увидят ВСЕ участники класса!",
                              self.get_keyboard("edit_standard_week"))
            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_STANDARD_WEEK_MYCLASSES.value)

    def s_edit_standard_week_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_STANDARD_WEEK_MYCLASSES"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("edit_standard_week"))

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

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_standard_week(classroom_id, english_weekday)

            if None in formatted_day_lessons:
                formatted_day_lessons = formatted_day_lessons[:formatted_day_lessons.index(None)]

            weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, english_weekday)

            self.diary_homework_db.insert_lessons_into_temp_weekday_table(user_id, english_weekday, formatted_day_lessons)
            self.send_message(user_id, weekday_diary_text, self.get_keyboard("edit_standard_weekday"))
            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_STANDARD_WEEKDAY_MYCLASSES.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в меню класса", self.get_keyboard("my_class_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES.value)

    def s_edit_standard_weekday_my_classes_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_STANDARD_WEEKDAY_MYCLASSES"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("edit_standard_weekday"))

        elif payload["text"] == "Добавить урок":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)

            if all(formatted_day_lessons):
                self.send_message(user_id, "Максимальное число (12) уроков уже записано!", self.get_keyboard("edit_standard_weekday"))
            else:
                new_lesson_index = formatted_day_lessons.index(None) + 1

                self.send_message(user_id, f"Напишите название {new_lesson_index}-го урока (макс 70 символов):", self.get_keyboard("cancel_menu"))
                self.user_db.set_user_dialog_state(user_id, States.S_ADD_NEW_LESSON_MYCLASSES.value)

        elif payload["text"] == "Удалить всё":
            formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)

            if not any(formatted_day_lessons):
                weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
                formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                weekday_diary_text = self.get_weekday_diary_text(formatted_day_lessons, weekday)

                self.send_message(user_id, f"Расписание на этот день и так пусто\n\n{weekday_diary_text}", self.get_keyboard("edit_standard_weekday"))

            else:
                self.diary_homework_db.update_delete_all_lessons_from_temp_table(user_id)
                weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
                new_formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                new_weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday)

                self.send_message(user_id, f"Все уроки удалены!\n\n{new_weekday_diary_text}", self.get_keyboard("edit_standard_weekday"))

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            self.classroom_db.update_user_customize_classroom(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

        elif payload["text"] == "Отменить":
            self.send_message(user_id, "Все изменения отменены!", self.get_keyboard("edit_standard_week"))
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_STANDARD_WEEK_MYCLASSES.value)

    def s_add_new_lesson_my_classes_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ADD_NEW_LESSON_MYCLASSES"""
        if payload is None:
            if len(message) > 70:
                self.send_message(user_id, "Длина названия превышает 70 символов!", self.get_keyboard("cancel_menu"))
            else:
                formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                new_lesson_index = formatted_day_lessons.index(None) + 1
                self.diary_homework_db.update_add_new_lesson_into_temp_table(user_id, message, new_lesson_index)

                new_formatted_day_lessons = self.diary_homework_db.get_weekday_lessons_from_temp_table(user_id)
                weekday = self.diary_homework_db.get_weekday_name_from_temp_table(user_id)
                new_weekday_diary_text = self.get_weekday_diary_text(new_formatted_day_lessons, weekday)

                self.send_message(user_id, f"Урок добавлен!\n\n{new_weekday_diary_text}", self.get_keyboard("edit_standard_weekday"))
                self.user_db.set_user_dialog_state(user_id, States.S_EDIT_STANDARD_WEEKDAY_MYCLASSES.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.diary_homework_db.delete_row_from_temp_weekday_table(user_id)
            self.classroom_db.update_user_customize_classroom(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

        elif payload["text"] == "Отменить":
            self.send_message(user_id, "Добавление урока отменено", self.get_keyboard("edit_standard_weekday"))
            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_STANDARD_WEEKDAY_MYCLASSES.value)

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
    def get_weekday_diary_text(formatted_days: list, weekday: str) -> str:
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
                weekday_without_empty = formatted_days.copy()
            weekday_diary = [f"{i}. {weekday_without_empty[i - 1]}" for i in range(1, len(weekday_without_empty) + 1)]

        return weekday_russian + "\n" + "\n".join(weekday_diary)

    @staticmethod
    def get_week_diary_text(formatted_week: list) -> str:
        """Returns text of week's diary"""
        week_diary = []

        weekdays = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        for weekday_name, weekday_list in zip(weekdays, formatted_week):
            if not any(weekday_list):
                week_diary.append(weekday_name + "\n" + "1. ПУСТО")
            else:
                if None in weekday_list:
                    weekday_list_without_empty = weekday_list[:weekday_list.index(None)]
                else:
                    weekday_list_without_empty = weekday_list.copy()

                day_lessons = [f"{i}. {weekday_list_without_empty[i - 1]}" for i in range(1, len(weekday_list_without_empty) + 1)]
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

    def p_edit_standard_week_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with text: Изменить эталонное расписание"""
        if current_dialog_state == States.S_IN_CLASS_MYCLASSES.value:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            if classroom_id == payload["classroom_id"]:
                self.s_in_class_my_classes_handler(user_id, payload)
            else:
                self.send_message(user_id, "Это расписание не того класса, в котором ты находишься!")
        else:
            self.send_message(user_id, "Ты должен находиться в меню класса, расписание которого собираешься изменить!")
