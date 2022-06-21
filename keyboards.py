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
    KEYBOARD_MY_CLASS_MENU.add_button(label="Дз текущее", payload=get_payload("Дз текущее"))
    KEYBOARD_MY_CLASS_MENU.add_button(label="Дз будущее", payload=get_payload("Дз будущее"))
    KEYBOARD_MY_CLASS_MENU.add_line()
    KEYBOARD_MY_CLASS_MENU.add_button(label="Расписание текущее", payload=get_payload("Расписание текущее"))
    KEYBOARD_MY_CLASS_MENU.add_button(label="Расписание будущее", payload=get_payload("Расписание будущее"))
    KEYBOARD_MY_CLASS_MENU.add_line()
    KEYBOARD_MY_CLASS_MENU.add_button(label="Расписание эталонное", payload=get_payload("Расписание эталонное"))
    KEYBOARD_MY_CLASS_MENU.add_line()
    KEYBOARD_MY_CLASS_MENU.add_button(label="Участники", payload=get_payload("Участники"))
    KEYBOARD_MY_CLASS_MENU.add_button(label="Настройки", payload=get_payload("Настройки"))
    KEYBOARD_MY_CLASS_MENU.add_button(label="Доп. инфа", payload=get_payload("Доп. инфа"))
    KEYBOARD_MY_CLASS_MENU.add_line()
    KEYBOARD_MY_CLASS_MENU.add_button(label="Главное меню", payload=get_payload("Главное меню"))

    # EDIT_STANDARD_WEEK KEYBOARD
    EDIT_STANDARD_WEEK_KEYBOARD = VkKeyboard()
    EDIT_STANDARD_WEEK_KEYBOARD.add_button("ПН", payload=get_payload("ПН"))
    EDIT_STANDARD_WEEK_KEYBOARD.add_button("ВТ", payload=get_payload("ВТ"))
    EDIT_STANDARD_WEEK_KEYBOARD.add_button("СР", payload=get_payload("СР"))
    EDIT_STANDARD_WEEK_KEYBOARD.add_button("ЧТ", payload=get_payload("ЧТ"))
    EDIT_STANDARD_WEEK_KEYBOARD.add_button("ПТ", payload=get_payload("ПТ"))
    EDIT_STANDARD_WEEK_KEYBOARD.add_line()
    EDIT_STANDARD_WEEK_KEYBOARD.add_button("СБ", payload=get_payload("СБ"))
    EDIT_STANDARD_WEEK_KEYBOARD.add_button("ВС", payload=get_payload("ВС"))
    EDIT_STANDARD_WEEK_KEYBOARD.add_line()
    EDIT_STANDARD_WEEK_KEYBOARD.add_button("Назад", payload=get_payload("Назад"))
    EDIT_STANDARD_WEEK_KEYBOARD.add_button("Главное меню", payload=get_payload("Главное меню"))

    # CANCEL_SEND KEYBOARD
    KEYBOARD_CANCEL_SEND = VkKeyboard()
    KEYBOARD_CANCEL_SEND.add_button(label="Отменить", payload=get_payload("Отменить"))
    KEYBOARD_CANCEL_SEND.add_button(label="Отправить", payload=get_payload("Отправить"))

    # EDIT_STANDARD_WEEKDAY KEYBOARD
    EDIT_STANDARD_WEEKDAY_KEYBOARD = VkKeyboard()
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_button("Добавить урок", payload=get_payload("Добавить урок"))
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_button("Удалить урок", payload=get_payload("Удалить урок"))
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_button("Редактировать урок", payload=get_payload("Редактировать урок"))
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_line()
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_button("Удалить всё", payload=get_payload("Удалить всё"))
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_line()
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_button("Отменить", payload=get_payload("Отменить"))
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_button("Сохранить", payload=get_payload("Сохранить"))
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_line()
    EDIT_STANDARD_WEEKDAY_KEYBOARD.add_button("Главное меню", payload=get_payload("Главное меню"))

    # CANCEL_MENU KEYBOARD
    KEYBOARD_CANCEL_MENU = VkKeyboard()
    KEYBOARD_CANCEL_MENU.add_button("Отменить", payload=get_payload("Отменить"))
    KEYBOARD_CANCEL_MENU.add_button("Главное меню", payload=get_payload("Главное меню"))
