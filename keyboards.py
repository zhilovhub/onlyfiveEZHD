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

    # SUBMIT_BACK KEYBOARD
    KEYBOARD_SUBMIT_BACK = VkKeyboard()
    KEYBOARD_SUBMIT_BACK.add_button(label="Отклонить", payload=get_payload("Отклонить"))
    KEYBOARD_SUBMIT_BACK.add_button(label="Принять", payload=get_payload("Принять"))
    KEYBOARD_SUBMIT_BACK.add_line()
    KEYBOARD_SUBMIT_BACK.add_button(label="Главное меню", payload=get_payload("Главное меню"))

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

    # MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS KEYBOARD
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS = VkKeyboard()
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.add_button("Да", payload=get_payload("Да"),
                                                                          color="negative")
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.add_button("Нет", payload=get_payload("Нет"),
                                                                          color="positive")
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.add_line()
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.add_button("Главное меню",
                                                                          payload=get_payload("Главное меню"))

    # MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS KEYBOARD
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS = VkKeyboard()
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.add_button("Удалить", payload=get_payload("Удалить"),
                                                                          color="negative")
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.add_button("Не удалять",
                                                                          payload=get_payload("Не удалять"),
                                                                          color="positive")
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.add_line()
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.add_button("Главное меню",
                                                                          payload=get_payload("Главное меню"))

    # BACK_MENU_DELETE_REQUEST
    KEYBOARD_BACK_MENU_DELETE_REQUEST = VkKeyboard()
    KEYBOARD_BACK_MENU_DELETE_REQUEST.add_button("Удалить заявку", payload=get_payload("Удалить заявку"),
                                                 color="negative")
    KEYBOARD_BACK_MENU_DELETE_REQUEST.add_line()
    KEYBOARD_BACK_MENU_DELETE_REQUEST.add_button("Назад", payload=get_payload("Назад"))
    KEYBOARD_BACK_MENU_DELETE_REQUEST.add_button("Главное меню", payload=get_payload("Главное меню"))

    # NOTIFICATION_SETTINGS KEYBOARD
    @staticmethod
    def get_notification_settings_keyboard(colors) -> VkKeyboard:
        notification_settings_keyboard = VkKeyboard()
        notification_settings_keyboard.add_button("Кто-то вступил", payload=KeyBoards.get_payload("Кто-то вступил"),
                                                  color=colors[0])
        notification_settings_keyboard.add_button("Кто-то ушел", payload=KeyBoards.get_payload("Кто-то ушел"),
                                                  color=colors[1])
        notification_settings_keyboard.add_line()
        notification_settings_keyboard.add_button("Новая заявка", payload=KeyBoards.get_payload("Новая заявка"),
                                                  color=colors[2])
        notification_settings_keyboard.add_button("Назад", payload=KeyBoards.get_payload("Назад"))
        notification_settings_keyboard.add_button("Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return notification_settings_keyboard.get_keyboard()

    # EDIT_HOMEWORK_WEEKDAY KEYBOARD
    @staticmethod
    def get_edit_homework_weekday_keyboard() -> VkKeyboard:
        keyboard_edit_homework_weekday = VkKeyboard()
        keyboard_edit_homework_weekday.add_button("Очистить всё дз", payload=KeyBoards.get_payload("Очистить всё дз"))
        keyboard_edit_homework_weekday.add_line()
        keyboard_edit_homework_weekday.add_button("Отменить", payload=KeyBoards.get_payload("Отменить"),
                                                  color="negative")
        keyboard_edit_homework_weekday.add_button("Сохранить", payload=KeyBoards.get_payload("Сохранить"),
                                                  color="positive")
        keyboard_edit_homework_weekday.add_line()
        keyboard_edit_homework_weekday.add_button("Главное меню", payload=KeyBoards.get_payload("Главное меню"),
                                                  color="primary")

        return keyboard_edit_homework_weekday.get_keyboard()

    # EDIT_HOMEWORK KEYBOARD
    @staticmethod
    def get_edit_homework_keyboard() -> VkKeyboard:
        keyboard_edit_homework = VkKeyboard()
        keyboard_edit_homework.add_button("ПН", payload=KeyBoards.get_payload("ПН"))
        keyboard_edit_homework.add_button("ВТ", payload=KeyBoards.get_payload("ВТ"))
        keyboard_edit_homework.add_button("СР", payload=KeyBoards.get_payload("СР"))
        keyboard_edit_homework.add_button("ЧТ", payload=KeyBoards.get_payload("ЧТ"))
        keyboard_edit_homework.add_button("ПТ", payload=KeyBoards.get_payload("ПТ"))
        keyboard_edit_homework.add_line()
        keyboard_edit_homework.add_button("СБ", payload=KeyBoards.get_payload("СБ"))
        keyboard_edit_homework.add_button("ВС", payload=KeyBoards.get_payload("ВС"))
        keyboard_edit_homework.add_line()
        keyboard_edit_homework.add_button("Назад", payload=KeyBoards.get_payload("Назад"))
        keyboard_edit_homework.add_button("Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_edit_homework.get_keyboard()

    # MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS KEYBOARD
    @staticmethod
    def get_main_dangerous_zone_classroom_settings_keyboard(is_admin: bool) -> VkKeyboard:
        keyboard_main_dangerous_zone_classroom_settings = VkKeyboard()
        keyboard_main_dangerous_zone_classroom_settings.add_button("Покинуть класс",
                                                                   payload=KeyBoards.get_payload("Покинуть класс"))
        if is_admin:
            keyboard_main_dangerous_zone_classroom_settings.add_button("Удалить класс",
                                                                       payload=KeyBoards.get_payload("Удалить класс"),
                                                                       color="negative")
        keyboard_main_dangerous_zone_classroom_settings.add_line()
        keyboard_main_dangerous_zone_classroom_settings.add_button("Назад",
                                                                   payload=KeyBoards.get_payload("Назад"))
        keyboard_main_dangerous_zone_classroom_settings.add_button("Главное меню",
                                                                   payload=KeyBoards.get_payload("Главное меню"))
        
        return keyboard_main_dangerous_zone_classroom_settings.get_keyboard()

    # MEMBERS_SETTINGS KEYBOARD
    @staticmethod
    def get_members_settings_keyboard(is_admin: bool, kick_members: bool, invite_members: bool) -> VkKeyboard:
        kick_members_label = "Удалить участника" if kick_members else "Удалить участника❌"
        invite_members_label = "Пригл. ссылка" if invite_members else "Пригл. ссылка❌"

        keyboard_members_settings = VkKeyboard()
        if is_admin:
            keyboard_members_settings.add_button("Добавить роли", 
                                                 payload=KeyBoards.get_payload("Добавить роли"))
            keyboard_members_settings.add_button("Редактировать роли", 
                                                 payload=KeyBoards.get_payload("Редактировать роли"))
            keyboard_members_settings.add_line()
            keyboard_members_settings.add_button("Удалить роли", 
                                                 payload=KeyBoards.get_payload("Удалить роли"))
            keyboard_members_settings.add_line()
            keyboard_members_settings.add_button("Назначить роли", 
                                                 payload=KeyBoards.get_payload("Назначить роли"))
            keyboard_members_settings.add_line()
        keyboard_members_settings.add_button(invite_members_label, 
                                             payload=KeyBoards.get_payload("Пригл. ссылка",
                                                                           can=invite_members))
        if not is_admin:
            keyboard_members_settings.add_line()
        keyboard_members_settings.add_button(kick_members_label,
                                             payload=KeyBoards.get_payload("Удалить участника",
                                                                           can=kick_members))
        keyboard_members_settings.add_line()
        keyboard_members_settings.add_button("Назад", 
                                             payload=KeyBoards.get_payload("Назад"))
        keyboard_members_settings.add_button("Главное меню", 
                                             payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_members_settings.get_keyboard()

    # MAIN_CLASSROOM_SETTINGS KEYBOARD
    @staticmethod
    def get_main_classroom_settings(change_classroom_access: bool, change_classroom_name: bool,
                                    change_school_name: bool, change_description: bool, change_members_limit: bool
                                    ) -> VkKeyboard:
        classroom_type_label = "Тип класса" if change_classroom_access else "Тип класса❌"
        classroom_name_label = "Название класса" if change_classroom_name else "Название класса❌"
        school_name_label = "Название школы" if change_school_name else "Название школы❌"
        description_label = "Описание класса" if change_description else "Описание класса❌"
        members_limit_label = "Лимит участников" if change_members_limit else "Лимит участников❌"

        keyboard_main_classroom_settings = VkKeyboard()
        keyboard_main_classroom_settings.add_button(classroom_type_label,
                                                    payload=KeyBoards.get_payload("Тип класса",
                                                                                  can=change_classroom_access))
        keyboard_main_classroom_settings.add_line()
        keyboard_main_classroom_settings.add_button(classroom_name_label,
                                                    payload=KeyBoards.get_payload("Название класса",
                                                                                  can=change_classroom_name))
        keyboard_main_classroom_settings.add_line()
        keyboard_main_classroom_settings.add_button(school_name_label,
                                                    payload=KeyBoards.get_payload("Название школы",
                                                                                  can=change_school_name))
        keyboard_main_classroom_settings.add_line()
        keyboard_main_classroom_settings.add_button(description_label,
                                                    payload=KeyBoards.get_payload("Описание класса",
                                                                                  can=change_description))
        keyboard_main_classroom_settings.add_button(members_limit_label,
                                                    payload=KeyBoards.get_payload("Лимит участников",
                                                                                  can=change_members_limit))
        keyboard_main_classroom_settings.add_line()
        keyboard_main_classroom_settings.add_button("Опасная зона",
                                                    payload=KeyBoards.get_payload("Опасная зона"),
                                                    color="negative")
        keyboard_main_classroom_settings.add_line()
        keyboard_main_classroom_settings.add_button("Назад",
                                                    payload=KeyBoards.get_payload("Назад"))
        keyboard_main_classroom_settings.add_button("Главное меню",
                                                    payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_main_classroom_settings.get_keyboard()

    # EDIT_WEEK KEYBOARD
    @staticmethod
    def get_edit_week_keyboard(week_type: str) -> VkKeyboard:
        keyboard_edit_week = VkKeyboard()
        keyboard_edit_week.add_button("ПН", payload=KeyBoards.get_payload("ПН"))
        keyboard_edit_week.add_button("ВТ", payload=KeyBoards.get_payload("ВТ"))
        keyboard_edit_week.add_button("СР", payload=KeyBoards.get_payload("СР"))
        keyboard_edit_week.add_button("ЧТ", payload=KeyBoards.get_payload("ЧТ"))
        keyboard_edit_week.add_button("ПТ", payload=KeyBoards.get_payload("ПТ"))
        keyboard_edit_week.add_line()
        keyboard_edit_week.add_button("СБ", payload=KeyBoards.get_payload("СБ"))
        keyboard_edit_week.add_button("ВС", payload=KeyBoards.get_payload("ВС"))
        keyboard_edit_week.add_line()
        if week_type in ("current", "next"):
            keyboard_edit_week.add_button("Скопировать с эталонного",
                                          payload=KeyBoards.get_payload("Скопировать с эталонного"))
            keyboard_edit_week.add_line()
        keyboard_edit_week.add_button("Назад", payload=KeyBoards.get_payload("Назад"))
        keyboard_edit_week.add_button("Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_edit_week.get_keyboard()

    # MY_CLASS_MENU2 KEYBOARD
    @staticmethod
    def get_my_class_menu2_keyboard(sign: bool, accept_requests: bool) -> VkKeyboard:
        keyboard_my_class_menu2 = VkKeyboard()
        if not accept_requests:
            keyboard_my_class_menu2.add_button(label="Заявки❌", payload=KeyBoards.get_payload("Заявки",
                                                                                              can=accept_requests))
        elif sign:
            keyboard_my_class_menu2.add_button(label="Заявки‼", payload=KeyBoards.get_payload("Заявки",
                                                                                              can=accept_requests))
        else:
            keyboard_my_class_menu2.add_button(label="Заявки", payload=KeyBoards.get_payload("Заявки",
                                                                                             can=accept_requests))
        keyboard_my_class_menu2.add_button(label="События", payload=KeyBoards.get_payload("События"))
        keyboard_my_class_menu2.add_button(label="Уведомить", payload=KeyBoards.get_payload("Уведомить"))
        keyboard_my_class_menu2.add_line()
        keyboard_my_class_menu2.add_button(label="⏪Назад", payload=KeyBoards.get_payload("Назад"))
        keyboard_my_class_menu2.add_button(label="Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_my_class_menu2.get_keyboard()

    # MY_CLASS_MENU KEYBOARD
    @staticmethod
    def get_my_class_menu_keyboard(sign: bool) -> VkKeyboard:
        keyboard_my_class_menu = VkKeyboard()
        keyboard_my_class_menu.add_button(label="Дз текущее", payload=KeyBoards.get_payload("Дз текущее"))
        keyboard_my_class_menu.add_button(label="Дз будущее", payload=KeyBoards.get_payload("Дз будущее"))
        keyboard_my_class_menu.add_line()
        keyboard_my_class_menu.add_button(label="Расписание текущее",
                                          payload=KeyBoards.get_payload("Расписание текущее"))
        keyboard_my_class_menu.add_button(label="Расписание будущее",
                                          payload=KeyBoards.get_payload("Расписание будущее"))
        keyboard_my_class_menu.add_line()
        keyboard_my_class_menu.add_button(label="Расписание эталонное",
                                          payload=KeyBoards.get_payload("Расписание эталонное"))
        keyboard_my_class_menu.add_line()
        keyboard_my_class_menu.add_button(label="Участники", payload=KeyBoards.get_payload("Участники"))
        keyboard_my_class_menu.add_button(label="Настройки", payload=KeyBoards.get_payload("Настройки"))
        if sign:
            keyboard_my_class_menu.add_button(label="⏩Ещё‼", payload=KeyBoards.get_payload("Ещё"))
        else:
            keyboard_my_class_menu.add_button(label="⏩Ещё", payload=KeyBoards.get_payload("Ещё"))
        keyboard_my_class_menu.add_line()
        keyboard_my_class_menu.add_button(label="Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_my_class_menu.get_keyboard()

    # CLASSROOM_PRIVILEGE KEYBOARD
    @staticmethod
    def get_classroom_privilege_keyboard(colors) -> VkKeyboard:
        keyboard_classroom_privilege = VkKeyboard()
        keyboard_classroom_privilege.add_button("Название класса", payload=KeyBoards.get_payload("Название класса"),
                                                color=colors[0])
        keyboard_classroom_privilege.add_line()
        keyboard_classroom_privilege.add_button("Название школы", payload=KeyBoards.get_payload("Название школы"),
                                                color=colors[1])
        keyboard_classroom_privilege.add_line()
        keyboard_classroom_privilege.add_button("Тип класса", payload=KeyBoards.get_payload("Тип класса"),
                                                color=colors[2])
        keyboard_classroom_privilege.add_line()
        keyboard_classroom_privilege.add_button("Описание класса", payload=KeyBoards.get_payload("Описание класса"),
                                                color=colors[3])
        keyboard_classroom_privilege.add_button("Лимит участников", payload=KeyBoards.get_payload("Лимит участников"),
                                                color=colors[4])
        keyboard_classroom_privilege.add_line()
        keyboard_classroom_privilege.add_button("Назад", payload=KeyBoards.get_payload("Назад"))
        keyboard_classroom_privilege.add_button("Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_classroom_privilege.get_keyboard()

    # MEMBERS_PRIVILEGE KEYBOARD
    @staticmethod
    def get_members_privilege_keyboard(colors) -> VkKeyboard:
        keyboard_members_privilege = VkKeyboard()
        keyboard_members_privilege.add_button("Кикание участников", payload=KeyBoards.get_payload("Кикание участников"),
                                              color=colors[0])
        keyboard_members_privilege.add_line()
        keyboard_members_privilege.add_button("Приглашение в класс",
                                              payload=KeyBoards.get_payload("Приглашение в класс"), color=colors[1])
        keyboard_members_privilege.add_line()
        keyboard_members_privilege.add_button("Принятие заявок", payload=KeyBoards.get_payload("Принятие заявок"),
                                              color=colors[2])
        keyboard_members_privilege.add_line()
        keyboard_members_privilege.add_button("Уведомление участников",
                                              payload=KeyBoards.get_payload("Уведомление участников"), color=colors[3])
        keyboard_members_privilege.add_line()

        keyboard_members_privilege.add_button("Назад", payload=KeyBoards.get_payload("Назад"))
        keyboard_members_privilege.add_button("Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_members_privilege.get_keyboard()

    # DIARY_PRIVILEGE KEYBOARD
    @staticmethod
    def get_diary_privilege_keyboard(colors) -> VkKeyboard:
        keyboard_diary_privilege = VkKeyboard()
        keyboard_diary_privilege.add_button("Текущее дз", payload=KeyBoards.get_payload("Текущее дз"), color=colors[0])
        keyboard_diary_privilege.add_button("Будущее дз", payload=KeyBoards.get_payload("Будущее дз"), color=colors[1])
        keyboard_diary_privilege.add_line()
        keyboard_diary_privilege.add_button("Эталонное расписание",
                                            payload=KeyBoards.get_payload("Эталонное расписание"), color=colors[2])
        keyboard_diary_privilege.add_line()
        keyboard_diary_privilege.add_button("Текущее расписание",
                                            payload=KeyBoards.get_payload("Текущее расписание"), color=colors[3])
        keyboard_diary_privilege.add_line()
        keyboard_diary_privilege.add_button("Будущее расписание", payload=KeyBoards.get_payload("Будущее расписание"),
                                            color=colors[4])
        keyboard_diary_privilege.add_line()

        keyboard_diary_privilege.add_button("Назад", payload=KeyBoards.get_payload("Назад"))
        keyboard_diary_privilege.add_button("Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_diary_privilege.get_keyboard()

    # LOOK_CLASSROOM KEYBOARD
    @staticmethod
    def get_look_classroom_keyboard(classroom_type) -> VkKeyboard:
        keyboard_look_classroom_menu = VkKeyboard()

        if classroom_type == "public":
            keyboard_look_classroom_menu.add_button("Войти", payload=KeyBoards.get_payload("Войти"))
            keyboard_look_classroom_menu.add_line()
        elif classroom_type == "invite":
            keyboard_look_classroom_menu.add_button("Подать заявку", payload=KeyBoards.get_payload("Подать заявку"))
            keyboard_look_classroom_menu.add_line()
        elif classroom_type == "look_request":
            keyboard_look_classroom_menu.add_button("Редактировать заявку",
                                                    payload=KeyBoards.get_payload("Редактировать заявку"))
            keyboard_look_classroom_menu.add_line()

        keyboard_look_classroom_menu.add_button("Участники", payload=KeyBoards.get_payload("Участники"))
        keyboard_look_classroom_menu.add_button("Вступить по ссылке",
                                                payload=KeyBoards.get_payload("Вступить по ссылке"))
        keyboard_look_classroom_menu.add_line()
        keyboard_look_classroom_menu.add_button("Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_look_classroom_menu.get_keyboard()

    # ROLE_SETTINGS_MENU KEYBOARD
    @staticmethod
    def get_role_settings_menu_keyboard() -> VkKeyboard:
        keyboard_role_settings_menu = VkKeyboard()
        keyboard_role_settings_menu.add_button("Сменить имя", payload=KeyBoards.get_payload("Сменить имя"))
        keyboard_role_settings_menu.add_line()
        keyboard_role_settings_menu.add_button("Дневник", payload=KeyBoards.get_payload("Дневник"))
        keyboard_role_settings_menu.add_button("Участники", payload=KeyBoards.get_payload("Участники"))
        keyboard_role_settings_menu.add_button("Класс", payload=KeyBoards.get_payload("Класс"))
        keyboard_role_settings_menu.add_line()
        keyboard_role_settings_menu.add_button("Назад", payload=KeyBoards.get_payload("Назад"))
        keyboard_role_settings_menu.add_button("Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_role_settings_menu.get_keyboard()

    # EDIT_WEEKDAY KEYBOARD
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

    # ACCESS_MENU_BACK KEYBOARD
    @staticmethod
    def get_access_menu_back_keyboard(public_color="secondary", invite_color="secondary",
                                      close_color="secondary") -> VkKeyboard:
        keyboard_access_menu_back = VkKeyboard()
        keyboard_access_menu_back.add_button(label="Публичный", payload=KeyBoards.get_payload("Публичный"),
                                             color=public_color)
        keyboard_access_menu_back.add_button(label="Заявки", payload=KeyBoards.get_payload("Заявки"),
                                             color=invite_color)
        keyboard_access_menu_back.add_button(label="Закрытый", payload=KeyBoards.get_payload("Закрытый"),
                                             color=close_color)
        keyboard_access_menu_back.add_line()
        keyboard_access_menu_back.add_button(label="Назад", payload=KeyBoards.get_payload("Назад"))
        keyboard_access_menu_back.add_button(label="Главное меню", payload=KeyBoards.get_payload("Главное меню"))

        return keyboard_access_menu_back.get_keyboard()
