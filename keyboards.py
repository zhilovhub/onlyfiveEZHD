from config import *


class KeyBoards:
    """All keyboards"""

    @staticmethod
    def get_payload(text: str, **kwargs) -> dict:
        payload = {"text": text}
        for key, value in kwargs.items():
            payload[key] = value

        return payload

    # EMPTY KEYBOARD
    KEYBOARD_EMPTY = VkKeyboard()

    # MENU KEYBOARD
    KEYBOARD_MENU = VkKeyboard()
    KEYBOARD_MENU.add_button(label="Найти класс", payload=get_payload("Найти класс"))
    KEYBOARD_MENU.add_button(label="Создать класс", payload=get_payload("Создать класс"))
    KEYBOARD_MENU.add_button(label="Мои классы", payload=get_payload("Мои классы"))
    KEYBOARD_MENU.add_line()
    KEYBOARD_MENU.add_button(label="Создать беседу класса", payload=get_payload("Создать беседу класса"))
    KEYBOARD_MENU.add_button(label="Настройка беседы класса", payload=get_payload("Настройка беседы класса"))
    KEYBOARD_MENU.add_line()
    KEYBOARD_MENU.add_button(label="Обращение в тех. поддержку", payload=get_payload("Обращение в тех. поддержку"))

    # CANCEL_BACK KEYBOARD
    KEYBOARD_CANCEL_BACK = VkKeyboard()
    KEYBOARD_CANCEL_BACK.add_button(label="Отменить", payload=get_payload("Отменить"))
    KEYBOARD_CANCEL_BACK.add_button(label="На шаг назад", payload=get_payload("На шаг назад"))

    # CANCEL KEYBOARD
    KEYBOARD_CANCEL = VkKeyboard()
    KEYBOARD_CANCEL.add_button(label="Отменить", payload=get_payload("Отменить"))

    # YES_NO_CANCEL_BACK KEYBOARD
    KEYBOARD_YES_NO_CANCEL_BACK = VkKeyboard()
    KEYBOARD_YES_NO_CANCEL_BACK.add_button(label="Нет", payload=get_payload("Нет"))
    KEYBOARD_YES_NO_CANCEL_BACK.add_button(label="Да", payload=get_payload("Да"))
    KEYBOARD_YES_NO_CANCEL_BACK.add_line()
    KEYBOARD_YES_NO_CANCEL_BACK.add_button(label="Отменить", payload=get_payload("Отменить"))
    KEYBOARD_YES_NO_CANCEL_BACK.add_button(label="На шаг назад", payload=get_payload("На шаг назад"))
    
    # SUBMIT_BACK KEYBOARD
    KEYBOARD_SUBMIT_BACK = VkKeyboard()
    KEYBOARD_SUBMIT_BACK.add_button(label="Отклонить", payload=get_payload("Отклонить"))
    KEYBOARD_SUBMIT_BACK.add_button(label="Принять", payload=get_payload("Принять"))

    # MY_CLASS_MENU KEYBOARD
    KEYBOARD_MY_CLASS_MENU = VkKeyboard()
    KEYBOARD_MY_CLASS_MENU.add_button(label="Участники", payload=get_payload("Участники"))
    KEYBOARD_MY_CLASS_MENU.add_button(label="Расписание", payload=get_payload("Расписание"))
    KEYBOARD_MY_CLASS_MENU.add_button(label="Настройки", payload=get_payload("Настройки"))
    KEYBOARD_MY_CLASS_MENU.add_line()
    KEYBOARD_MY_CLASS_MENU.add_button(label="Главное меню", payload=get_payload("Главное меню"))

    # TIMETABLE_MENU KEYBOARD
    TIMETABLE_MENU_KEYBOARD = VkKeyboard()
    TIMETABLE_MENU_KEYBOARD.add_button(label="Список уроков", payload=get_payload("Список уроков"))
    TIMETABLE_MENU_KEYBOARD.add_button(label="Дз", payload=get_payload("Дз"))
    TIMETABLE_MENU_KEYBOARD.add_line()
    TIMETABLE_MENU_KEYBOARD.add_button(label="Мероприятия", payload=get_payload("Мероприятия"))
    TIMETABLE_MENU_KEYBOARD.add_button(label="Важные сообщения", payload=get_payload("Важные сообщения"))
    TIMETABLE_MENU_KEYBOARD.add_line()
    TIMETABLE_MENU_KEYBOARD.add_button(label="Назад", payload=get_payload("Назад"))
    TIMETABLE_MENU_KEYBOARD.add_line()
    TIMETABLE_MENU_KEYBOARD.add_button(label="Главное меню", payload=get_payload("Главное меню"))

    # TIMETABLE KEYBOARD
    TIMETABLE_KEYBOARD = VkKeyboard()
    TIMETABLE_KEYBOARD.add_button("Текущая неделя", payload=get_payload("Текущая неделя"))
    TIMETABLE_KEYBOARD.add_button("Следующая неделя", payload=get_payload("Следующая неделя"))
    TIMETABLE_KEYBOARD.add_line()
    TIMETABLE_KEYBOARD.add_button("Эталонная неделя", payload=get_payload("Эталонная неделя"))
    TIMETABLE_KEYBOARD.add_line()
    TIMETABLE_KEYBOARD.add_button("Назад", payload=get_payload("Назад"))
    TIMETABLE_KEYBOARD.add_button("Главное меню", payload=get_payload("Главное меню"))
