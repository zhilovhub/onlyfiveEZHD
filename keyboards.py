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
    KEYBOARD_EDIT_STANDARD_WEEK = VkKeyboard()
    KEYBOARD_EDIT_STANDARD_WEEK.add_button("ПН", payload=get_payload("ПН", weektype="standard"))
    KEYBOARD_EDIT_STANDARD_WEEK.add_button("ВТ", payload=get_payload("ВТ", weektype="standard"))
    KEYBOARD_EDIT_STANDARD_WEEK.add_button("СР", payload=get_payload("СР", weektype="standard"))
    KEYBOARD_EDIT_STANDARD_WEEK.add_button("ЧТ", payload=get_payload("ЧТ", weektype="standard"))
    KEYBOARD_EDIT_STANDARD_WEEK.add_button("ПТ", payload=get_payload("ПТ", weektype="standard"))
    KEYBOARD_EDIT_STANDARD_WEEK.add_line()
    KEYBOARD_EDIT_STANDARD_WEEK.add_button("СБ", payload=get_payload("СБ", weektype="standard"))
    KEYBOARD_EDIT_STANDARD_WEEK.add_button("ВС", payload=get_payload("ВС", weektype="standard"))
    KEYBOARD_EDIT_STANDARD_WEEK.add_line()
    KEYBOARD_EDIT_STANDARD_WEEK.add_button("Назад", payload=get_payload("Назад"))
    KEYBOARD_EDIT_STANDARD_WEEK.add_button("Главное меню", payload=get_payload("Главное меню"))

    # EDIT_CURRENT_NEXT_WEEK KEYBOARD
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK = VkKeyboard()
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("ПН", payload=get_payload("ПН"))
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("ВТ", payload=get_payload("ВТ"))
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("СР", payload=get_payload("СР"))
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("ЧТ", payload=get_payload("ЧТ"))
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("ПТ", payload=get_payload("ПТ"))
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_line()
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("СБ", payload=get_payload("СБ"))
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("ВС", payload=get_payload("ВС"))
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_line()
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("Скопировать с эталонного", payload=get_payload("Скопировать с эталонного"))
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_line()
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("Назад", payload=get_payload("Назад"))
    KEYBOARD_EDIT_CURRENT_NEXT_WEEK.add_button("Главное меню", payload=get_payload("Главное меню"))

    # CANCEL_SEND KEYBOARD
    KEYBOARD_CANCEL_SEND = VkKeyboard()
    KEYBOARD_CANCEL_SEND.add_button(label="Отменить", payload=get_payload("Отменить"))
    KEYBOARD_CANCEL_SEND.add_button(label="Отправить", payload=get_payload("Отправить"))

    # BACK_MENU KEYBOARD
    KEYBOARD_BACK_MENU = VkKeyboard()
    KEYBOARD_BACK_MENU.add_button("Назад", payload=get_payload("Назад"))
    KEYBOARD_BACK_MENU.add_button("Главное меню", payload=get_payload("Главное меню"))

    # JUST_MENU KEYBOARD
    KEYBOARD_JUST_MENU = VkKeyboard()
    KEYBOARD_JUST_MENU.add_button("Главное меню", payload=get_payload("Главное меню"))

    # CLASSROOM_SETTINGS KEYBOARD
    KEYBOARD_CLASSROOM_SETTINGS = VkKeyboard()
    KEYBOARD_CLASSROOM_SETTINGS.add_button("Основные", payload=get_payload("Основные"))
    KEYBOARD_CLASSROOM_SETTINGS.add_line()
    KEYBOARD_CLASSROOM_SETTINGS.add_button("Уведомления", payload=get_payload("Уведомления"))
    KEYBOARD_CLASSROOM_SETTINGS.add_line()
    KEYBOARD_CLASSROOM_SETTINGS.add_button("Назад", payload=get_payload("Назад"))
    KEYBOARD_CLASSROOM_SETTINGS.add_button("Главное меню", payload=get_payload("Главное меню"))

    # CUSTOMIZED EDIT_WEEKDAY KEYBOARD
    @staticmethod
    def get_edit_weekday_keyboard(add_button_color="secondary", redact_button_color="secondary") -> VkKeyboard:
        keyboard_edit_weekday = VkKeyboard()
        keyboard_edit_weekday.add_button("Добавить",
                                         payload=KeyBoards.get_payload("Добавить"),
                                         color=add_button_color)
        keyboard_edit_weekday.add_button("Удалить урок",
                                         payload=KeyBoards.get_payload("Удалить урок"))
        keyboard_edit_weekday.add_button("Изменить",
                                         payload=KeyBoards.get_payload("Изменить"),
                                         color=redact_button_color)
        keyboard_edit_weekday.add_line()
        keyboard_edit_weekday.add_button("Удалить всё",
                                         payload=KeyBoards.get_payload("Удалить всё"))
        keyboard_edit_weekday.add_line()
        keyboard_edit_weekday.add_button("Отменить",
                                         payload=KeyBoards.get_payload("Отменить"),
                                         color="negative")
        keyboard_edit_weekday.add_button("Сохранить",
                                         payload=KeyBoards.get_payload("Сохранить"),
                                         color="positive")
        keyboard_edit_weekday.add_line()
        keyboard_edit_weekday.add_button("Главное меню",
                                         payload=KeyBoards.get_payload("Главное меню"),
                                         color="primary")

        return keyboard_edit_weekday.get_keyboard()
