from config import *


class KeyBoards:
    """All keyboards"""

    # EMPTY KEYBOARD
    KEYBOARD_EMPTY = VkKeyboard()

    # MENU KEYBOARD
    KEYBOARD_MENU = VkKeyboard()
    KEYBOARD_MENU.add_button(label="Найти класс")
    KEYBOARD_MENU.add_button(label="Создать класс")
    KEYBOARD_MENU.add_button(label="Мои классы")
    KEYBOARD_MENU.add_line()
    KEYBOARD_MENU.add_button(label="Создать беседу класса")
    KEYBOARD_MENU.add_button(label="Настройка беседы класса")
    KEYBOARD_MENU.add_line()
    KEYBOARD_MENU.add_button(label="Обращение в тех. поддержку")

    # CANCEL_BACK KEYBOARD
    KEYBOARD_CANCEL_BACK = VkKeyboard()
    KEYBOARD_CANCEL_BACK.add_button(label="Отменить")
    KEYBOARD_CANCEL_BACK.add_button(label="На шаг назад")

    # CANCEL KEYBOARD
    KEYBOARD_CANCEL = VkKeyboard()
    KEYBOARD_CANCEL.add_button(label="Отменить")

    # YES_NO_CANCEL_BACK KEYBOARD
    KEYBOARD_YES_NO_CANCEL_BACK = VkKeyboard()
    KEYBOARD_YES_NO_CANCEL_BACK.add_button(label="Нет")
    KEYBOARD_YES_NO_CANCEL_BACK.add_button(label="Да")
    KEYBOARD_YES_NO_CANCEL_BACK.add_line()
    KEYBOARD_YES_NO_CANCEL_BACK.add_button(label="Отменить")
    KEYBOARD_YES_NO_CANCEL_BACK.add_button(label="На шаг назад")
    
    # SUBMIT_BACK KEYBOARD
    KEYBOARD_SUBMIT_BACK = VkKeyboard()
    KEYBOARD_SUBMIT_BACK.add_button(label="Отклонить")
    KEYBOARD_SUBMIT_BACK.add_button(label="Принять")

    # MY_CLASS_MENU KEYBOARD
    KEYBOARD_MY_CLASS_MENU = VkKeyboard()
    KEYBOARD_MY_CLASS_MENU.add_button(label="Участники")
    KEYBOARD_MY_CLASS_MENU.add_button(label="Расписание")
    KEYBOARD_MY_CLASS_MENU.add_button(label="Настройки")
    KEYBOARD_MY_CLASS_MENU.add_line()
    KEYBOARD_MY_CLASS_MENU.add_button(label="Главное меню")
