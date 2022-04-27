from vk_api.keyboard import VkKeyboard


class KeyBoards:
    """All keyboards"""

    # EMPTY KEYBOARD
    KEYBOARD_EMPTY = VkKeyboard(one_time=True)

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
