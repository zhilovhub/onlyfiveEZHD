from config import *


class KeyBoards:
    """All keyboards"""

    @staticmethod
    def get_color(color_str: str) -> KeyboardButtonColor:
        color_dict = {
            "positive": KeyboardButtonColor.POSITIVE,
            "negative": KeyboardButtonColor.NEGATIVE,
            "secondary": KeyboardButtonColor.SECONDARY,
            "primary": KeyboardButtonColor.PRIMARY,
        }
        return color_dict[color_str]

    @staticmethod
    def get_payload(text: str, **kwargs) -> dict:
        payload = {"text": text}
        for key, value in kwargs.items():
            payload[key] = value

        return payload

    # EMPTY KEYBOARD
    KEYBOARD_EMPTY = Keyboard()

    # MENU KEYBOARD
    KEYBOARD_MENU = Keyboard()
    KEYBOARD_MENU.add(Text("Найти класс", payload=get_payload("Найти класс")))
    KEYBOARD_MENU.add(Text("Создать класс", payload=get_payload("Создать класс")))
    KEYBOARD_MENU.add(Text("Мои классы", payload=get_payload("Мои классы")))
    # KEYBOARD_MENU.row()
    # KEYBOARD_MENU.add(Text("Создать беседу класса", payload=get_payload("Создать беседу класса")))
    # KEYBOARD_MENU.add(Text("Настройка беседы класса", payload=get_payload("Настройка беседы класса")))
    KEYBOARD_MENU.row()
    KEYBOARD_MENU.add(Text("Обращение в тех. поддержку", payload=get_payload("Обращение в тех. поддержку")))

    # SUBMIT_BACK KEYBOARD
    KEYBOARD_SUBMIT_BACK = Keyboard()
    KEYBOARD_SUBMIT_BACK.add(Text("Отклонить", payload=get_payload("Отклонить")))
    KEYBOARD_SUBMIT_BACK.add(Text("Принять", payload=get_payload("Принять")))
    KEYBOARD_SUBMIT_BACK.row()
    KEYBOARD_SUBMIT_BACK.add(Text("Главное меню", payload=get_payload("Главное меню")))

    # CANCEL_SEND KEYBOARD
    KEYBOARD_CANCEL_SEND = Keyboard()
    KEYBOARD_CANCEL_SEND.add(Text("Отменить", payload=get_payload("Отменить")))
    KEYBOARD_CANCEL_SEND.add(Text("Отправить", payload=get_payload("Отправить")))

    # BACK_MENU KEYBOARD
    KEYBOARD_BACK_MENU = Keyboard()
    KEYBOARD_BACK_MENU.add(Text("Назад", payload=get_payload("Назад")))
    KEYBOARD_BACK_MENU.add(Text("Главное меню", payload=get_payload("Главное меню")))

    # JUST_MENU KEYBOARD
    KEYBOARD_JUST_MENU = Keyboard()
    KEYBOARD_JUST_MENU.add(Text("Главное меню", payload=get_payload("Главное меню")))

    # CLASSROOM_SETTINGS KEYBOARD
    KEYBOARD_CLASSROOM_SETTINGS = Keyboard()
    KEYBOARD_CLASSROOM_SETTINGS.add(Text("Основные", payload=get_payload("Основные")))
    KEYBOARD_CLASSROOM_SETTINGS.row()
    KEYBOARD_CLASSROOM_SETTINGS.add(Text("Уведомления", payload=get_payload("Уведомления")))
    KEYBOARD_CLASSROOM_SETTINGS.row()
    KEYBOARD_CLASSROOM_SETTINGS.add(Text("Назад", payload=get_payload("Назад")))
    KEYBOARD_CLASSROOM_SETTINGS.add(Text("Главное меню", payload=get_payload("Главное меню")))

    # MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS KEYBOARD
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS = Keyboard()
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.add(Text("Да", payload=get_payload("Да")),
                                                                   color=KeyboardButtonColor.NEGATIVE)
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.add(Text("Нет", payload=get_payload("Нет")),
                                                                   color=KeyboardButtonColor.POSITIVE)
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.row()
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.add(Text("Главное меню",
                                                                        payload=get_payload("Главное меню")))

    # MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS KEYBOARD
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS = Keyboard()
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.add(Text("Удалить", payload=get_payload("Удалить")),
                                                                   color=KeyboardButtonColor.NEGATIVE)
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.add(Text("Не удалять",
                                                                        payload=get_payload("Не удалять")),
                                                                   color=KeyboardButtonColor.POSITIVE)
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.row()
    KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.add(Text("Главное меню",
                                                                        payload=get_payload("Главное меню")))

    # BACK_MENU_DELETE_REQUEST
    KEYBOARD_BACK_MENU_DELETE_REQUEST = Keyboard()
    KEYBOARD_BACK_MENU_DELETE_REQUEST.add(Text("Удалить заявку", payload=get_payload("Удалить заявку")),
                                          color=KeyboardButtonColor.NEGATIVE)
    KEYBOARD_BACK_MENU_DELETE_REQUEST.row()
    KEYBOARD_BACK_MENU_DELETE_REQUEST.add(Text("Назад", payload=get_payload("Назад")))
    KEYBOARD_BACK_MENU_DELETE_REQUEST.add(Text("Главное меню", payload=get_payload("Главное меню")))

    # CHOOSE_EVENT KEYBOARD
    @staticmethod
    def get_choose_event_keyboard(sorted_events: list, redact_events: bool) -> str:
        add_event_label = "Добавить событие" if redact_events else "Добавить событие❌"

        choose_event_keyboard = Keyboard()
        for ind, event in enumerate(sorted_events, start=1):
            message_event_id = event["message_event_id"]
            if ind % 5 == 0 and ind != len(sorted_events):
                choose_event_keyboard.add(Text(message_event_id,
                                               payload=KeyBoards.get_payload(event["message_event_id"])))
                choose_event_keyboard.row()
            else:
                choose_event_keyboard.add(Text(message_event_id,
                                               payload=KeyBoards.get_payload(event["message_event_id"])))

        choose_event_keyboard.row()
        choose_event_keyboard.add(Text(add_event_label, payload=KeyBoards.get_payload("Добавить событие",
                                                                                      can=redact_events)))
        choose_event_keyboard.row()
        choose_event_keyboard.add(Text("Назад", payload=KeyBoards.get_payload("Назад")))
        choose_event_keyboard.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return choose_event_keyboard.get_json()

    # NOTIFICATION_SETTINGS KEYBOARD
    @staticmethod
    def get_notification_settings_keyboard(colors) -> str:
        notification_settings_keyboard = Keyboard()
        notification_settings_keyboard.add(Text("Кто-то вступил", payload=KeyBoards.get_payload("Кто-то вступил")),
                                           color=KeyBoards.get_color(colors[0]))
        notification_settings_keyboard.add(Text("Кто-то ушел", payload=KeyBoards.get_payload("Кто-то ушел")),
                                           color=KeyBoards.get_color(colors[1]))
        notification_settings_keyboard.row()
        notification_settings_keyboard.add(Text("Новая заявка", payload=KeyBoards.get_payload("Новая заявка")),
                                           color=KeyBoards.get_color(colors[2]))
        notification_settings_keyboard.row()
        notification_settings_keyboard.add(Text("Назад", payload=KeyBoards.get_payload("Назад")))
        notification_settings_keyboard.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return notification_settings_keyboard.get_json()

    # EDIT_HOMEWORK_WEEKDAY KEYBOARD
    @staticmethod
    def get_edit_homework_weekday_keyboard() -> str:
        keyboard_edit_homework_weekday = Keyboard()
        keyboard_edit_homework_weekday.add(Text("Очистить всё дз", payload=KeyBoards.get_payload("Очистить всё дз")))
        keyboard_edit_homework_weekday.row()
        keyboard_edit_homework_weekday.add(Text("Отменить", payload=KeyBoards.get_payload("Отменить")),
                                           color=KeyboardButtonColor.NEGATIVE)
        keyboard_edit_homework_weekday.add(Text("Сохранить", payload=KeyBoards.get_payload("Сохранить")),
                                           color=KeyboardButtonColor.POSITIVE)
        keyboard_edit_homework_weekday.row()
        keyboard_edit_homework_weekday.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")),
                                           color=KeyboardButtonColor.PRIMARY)

        return keyboard_edit_homework_weekday.get_json()

    # EDIT_HOMEWORK KEYBOARD
    @staticmethod
    def get_edit_homework_keyboard() -> str:
        keyboard_edit_homework = Keyboard()
        keyboard_edit_homework.add(Text("ПН", payload=KeyBoards.get_payload("ПН")))
        keyboard_edit_homework.add(Text("ВТ", payload=KeyBoards.get_payload("ВТ")))
        keyboard_edit_homework.add(Text("СР", payload=KeyBoards.get_payload("СР")))
        keyboard_edit_homework.add(Text("ЧТ", payload=KeyBoards.get_payload("ЧТ")))
        keyboard_edit_homework.add(Text("ПТ", payload=KeyBoards.get_payload("ПТ")))
        keyboard_edit_homework.row()
        keyboard_edit_homework.add(Text("СБ", payload=KeyBoards.get_payload("СБ")))
        keyboard_edit_homework.add(Text("ВС", payload=KeyBoards.get_payload("ВС")))
        keyboard_edit_homework.row()
        keyboard_edit_homework.add(Text("Назад", payload=KeyBoards.get_payload("Назад")))
        keyboard_edit_homework.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_edit_homework.get_json()

    # MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS KEYBOARD
    @staticmethod
    def get_main_dangerous_zone_classroom_settings_keyboard(is_admin: bool) -> str:
        keyboard_main_dangerous_zone_classroom_settings = Keyboard()
        keyboard_main_dangerous_zone_classroom_settings.add(Text("Покинуть класс",
                                                                 payload=KeyBoards.get_payload("Покинуть класс")))
        if is_admin:
            keyboard_main_dangerous_zone_classroom_settings.add(Text("Удалить класс",
                                                                     payload=KeyBoards.get_payload("Удалить класс")),
                                                                color=KeyboardButtonColor.NEGATIVE)
        keyboard_main_dangerous_zone_classroom_settings.row()
        keyboard_main_dangerous_zone_classroom_settings.add(Text("Назад",
                                                                 payload=KeyBoards.get_payload("Назад")))
        keyboard_main_dangerous_zone_classroom_settings.add(Text("Главное меню",
                                                                 payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_main_dangerous_zone_classroom_settings.get_json()

    # MEMBERS_SETTINGS KEYBOARD
    @staticmethod
    def get_members_settings_keyboard(is_admin: bool, kick_members: bool, invite_members: bool) -> str:
        kick_members_label = "Удалить участника" if kick_members else "Удалить участника❌"
        invite_members_label = "Пригл. ссылка" if invite_members else "Пригл. ссылка❌"

        keyboard_members_settings = Keyboard()
        if is_admin:
            keyboard_members_settings.add(Text("Добавить роли",
                                               payload=KeyBoards.get_payload("Добавить роли")))
            keyboard_members_settings.add(Text("Редактировать роли",
                                               payload=KeyBoards.get_payload("Редактировать роли")))
            keyboard_members_settings.row()
            keyboard_members_settings.add(Text("Удалить роли",
                                               payload=KeyBoards.get_payload("Удалить роли")))
            keyboard_members_settings.row()
            keyboard_members_settings.add(Text("Назначить роли",
                                               payload=KeyBoards.get_payload("Назначить роли")))
            keyboard_members_settings.row()
        keyboard_members_settings.add(Text(invite_members_label,
                                           payload=KeyBoards.get_payload("Пригл. ссылка",
                                                                         can=invite_members)))
        if not is_admin:
            keyboard_members_settings.row()
        keyboard_members_settings.add(Text(kick_members_label,
                                           payload=KeyBoards.get_payload("Удалить участника",
                                                                         can=kick_members)))
        keyboard_members_settings.row()
        keyboard_members_settings.add(Text("Назад",
                                           payload=KeyBoards.get_payload("Назад")))
        keyboard_members_settings.add(Text("Главное меню",
                                           payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_members_settings.get_json()

    # MAIN_CLASSROOM_SETTINGS KEYBOARD
    @staticmethod
    def get_main_classroom_settings(change_classroom_access: bool, change_classroom_name: bool,
                                    change_school_name: bool, change_description: bool, change_members_limit: bool
                                    ) -> str:
        classroom_type_label = "Тип класса" if change_classroom_access else "Тип класса❌"
        classroom_name_label = "Название класса" if change_classroom_name else "Название класса❌"
        school_name_label = "Название школы" if change_school_name else "Название школы❌"
        description_label = "Описание класса" if change_description else "Описание класса❌"
        members_limit_label = "Лимит участников" if change_members_limit else "Лимит участников❌"

        keyboard_main_classroom_settings = Keyboard()
        keyboard_main_classroom_settings.add(Text(classroom_type_label,
                                                  payload=KeyBoards.get_payload("Тип класса",
                                                                                can=change_classroom_access)))
        keyboard_main_classroom_settings.row()
        keyboard_main_classroom_settings.add(Text(classroom_name_label,
                                                  payload=KeyBoards.get_payload("Название класса",
                                                                                can=change_classroom_name)))
        keyboard_main_classroom_settings.row()
        keyboard_main_classroom_settings.add(Text(school_name_label,
                                                  payload=KeyBoards.get_payload("Название школы",
                                                                                can=change_school_name)))
        keyboard_main_classroom_settings.row()
        keyboard_main_classroom_settings.add(Text(description_label,
                                                  payload=KeyBoards.get_payload("Описание класса",
                                                                                can=change_description)))
        keyboard_main_classroom_settings.add(Text(members_limit_label,
                                                  payload=KeyBoards.get_payload("Лимит участников",
                                                                                can=change_members_limit)))
        keyboard_main_classroom_settings.row()
        keyboard_main_classroom_settings.add(Text("Опасная зона",
                                                  payload=KeyBoards.get_payload("Опасная зона")),
                                             color=KeyboardButtonColor.NEGATIVE)
        keyboard_main_classroom_settings.row()
        keyboard_main_classroom_settings.add(Text("Назад",
                                                  payload=KeyBoards.get_payload("Назад")))
        keyboard_main_classroom_settings.add(Text("Главное меню",
                                                  payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_main_classroom_settings.get_json()

    # EDIT_WEEK KEYBOARD
    @staticmethod
    def get_edit_week_keyboard(week_type: str) -> str:
        keyboard_edit_week = Keyboard()
        keyboard_edit_week.add(Text("ПН", payload=KeyBoards.get_payload("ПН")))
        keyboard_edit_week.add(Text("ВТ", payload=KeyBoards.get_payload("ВТ")))
        keyboard_edit_week.add(Text("СР", payload=KeyBoards.get_payload("СР")))
        keyboard_edit_week.add(Text("ЧТ", payload=KeyBoards.get_payload("ЧТ")))
        keyboard_edit_week.add(Text("ПТ", payload=KeyBoards.get_payload("ПТ")))
        keyboard_edit_week.row()
        keyboard_edit_week.add(Text("СБ", payload=KeyBoards.get_payload("СБ")))
        keyboard_edit_week.add(Text("ВС", payload=KeyBoards.get_payload("ВС")))
        keyboard_edit_week.row()
        if week_type in ("current", "next"):
            keyboard_edit_week.add(Text("Скопировать с эталонного",
                                        payload=KeyBoards.get_payload("Скопировать с эталонного")))
            keyboard_edit_week.row()
        keyboard_edit_week.add(Text("Назад", payload=KeyBoards.get_payload("Назад")))
        keyboard_edit_week.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_edit_week.get_json()

    # MY_CLASS_MENU2 KEYBOARD
    @staticmethod
    def get_my_class_menu2_keyboard(sign: bool, accept_requests: bool) -> str:
        keyboard_my_class_menu2 = Keyboard()
        if not accept_requests:
            keyboard_my_class_menu2.add(Text("Заявки❌", payload=KeyBoards.get_payload("Заявки",
                                                                                      can=accept_requests)))
        elif sign:
            keyboard_my_class_menu2.add(Text("Заявки‼", payload=KeyBoards.get_payload("Заявки",
                                                                                      can=accept_requests)))
        else:
            keyboard_my_class_menu2.add(Text("Заявки", payload=KeyBoards.get_payload("Заявки",
                                                                                     can=accept_requests)))
        keyboard_my_class_menu2.add(Text("События", payload=KeyBoards.get_payload("События")))
        keyboard_my_class_menu2.add(Text("Уведомить", payload=KeyBoards.get_payload("Уведомить")))
        keyboard_my_class_menu2.row()
        keyboard_my_class_menu2.add(Text("⏪Назад", payload=KeyBoards.get_payload("Назад")))
        keyboard_my_class_menu2.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_my_class_menu2.get_json()

    # MY_CLASS_MENU KEYBOARD
    @staticmethod
    def get_my_class_menu_keyboard(sign: bool) -> str:
        keyboard_my_class_menu = Keyboard()
        keyboard_my_class_menu.add(Text("Дз текущее", payload=KeyBoards.get_payload("Дз текущее")))
        keyboard_my_class_menu.add(Text("Дз будущее", payload=KeyBoards.get_payload("Дз будущее")))
        keyboard_my_class_menu.row()
        keyboard_my_class_menu.add(Text("Расписание текущее",
                                        payload=KeyBoards.get_payload("Расписание текущее")))
        keyboard_my_class_menu.add(Text("Расписание будущее",
                                        payload=KeyBoards.get_payload("Расписание будущее")))
        keyboard_my_class_menu.row()
        keyboard_my_class_menu.add(Text("Расписание эталонное",
                                        payload=KeyBoards.get_payload("Расписание эталонное")))
        keyboard_my_class_menu.row()
        keyboard_my_class_menu.add(Text("Участники", payload=KeyBoards.get_payload("Участники")))
        keyboard_my_class_menu.add(Text("Настройки", payload=KeyBoards.get_payload("Настройки")))
        if sign:
            keyboard_my_class_menu.add(Text("⏩Ещё‼", payload=KeyBoards.get_payload("Ещё")))
        else:
            keyboard_my_class_menu.add(Text("⏩Ещё", payload=KeyBoards.get_payload("Ещё")))
        keyboard_my_class_menu.row()
        keyboard_my_class_menu.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_my_class_menu.get_json()

    # CLASSROOM_PRIVILEGE KEYBOARD
    @staticmethod
    def get_classroom_privilege_keyboard(colors) -> str:
        keyboard_classroom_privilege = Keyboard()
        keyboard_classroom_privilege.add(Text("Название класса", payload=KeyBoards.get_payload("Название класса")),
                                         color=KeyBoards.get_color(colors[0]))
        keyboard_classroom_privilege.row()
        keyboard_classroom_privilege.add(Text("Название школы", payload=KeyBoards.get_payload("Название школы")),
                                         color=KeyBoards.get_color(colors[1]))
        keyboard_classroom_privilege.row()
        keyboard_classroom_privilege.add(Text("Тип класса", payload=KeyBoards.get_payload("Тип класса")),
                                         color=KeyBoards.get_color(colors[2]))
        keyboard_classroom_privilege.row()
        keyboard_classroom_privilege.add(Text("Описание класса", payload=KeyBoards.get_payload("Описание класса")),
                                         color=KeyBoards.get_color(colors[3]))
        keyboard_classroom_privilege.add(Text("Лимит участников", payload=KeyBoards.get_payload("Лимит участников")),
                                         color=KeyBoards.get_color(colors[4]))
        keyboard_classroom_privilege.row()
        keyboard_classroom_privilege.add(Text("Назад", payload=KeyBoards.get_payload("Назад")))
        keyboard_classroom_privilege.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_classroom_privilege.get_json()

    # MEMBERS_PRIVILEGE KEYBOARD
    @staticmethod
    def get_members_privilege_keyboard(colors) -> str:
        keyboard_members_privilege = Keyboard()
        keyboard_members_privilege.add(Text("Кикание участников", payload=KeyBoards.get_payload("Кикание участников")),
                                       color=KeyBoards.get_color(colors[0]))
        keyboard_members_privilege.row()
        keyboard_members_privilege.add(Text("Приглашение в класс",
                                            payload=KeyBoards.get_payload("Приглашение в класс")),
                                       color=KeyBoards.get_color(colors[1]))
        keyboard_members_privilege.row()
        keyboard_members_privilege.add(Text("Принятие заявок", payload=KeyBoards.get_payload("Принятие заявок")),
                                       color=KeyBoards.get_color(colors[2]))
        keyboard_members_privilege.row()
        keyboard_members_privilege.add(Text("Уведомление участников",
                                            payload=KeyBoards.get_payload("Уведомление участников")),
                                       color=KeyBoards.get_color(colors[3]))
        keyboard_members_privilege.row()
        keyboard_members_privilege.add(Text("Редактирование событий",
                                            payload=KeyBoards.get_payload("Редактирование событий")),
                                       color=KeyBoards.get_color(colors[4]))
        keyboard_members_privilege.row()

        keyboard_members_privilege.add(Text("Назад", payload=KeyBoards.get_payload("Назад")))
        keyboard_members_privilege.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_members_privilege.get_json()

    # DIARY_PRIVILEGE KEYBOARD
    @staticmethod
    def get_diary_privilege_keyboard(colors) -> str:
        keyboard_diary_privilege = Keyboard()
        keyboard_diary_privilege.add(Text("Текущее дз", payload=KeyBoards.get_payload("Текущее дз")),
                                     color=KeyBoards.get_color(colors[0]))
        keyboard_diary_privilege.add(Text("Будущее дз", payload=KeyBoards.get_payload("Будущее дз")),
                                     color=KeyBoards.get_color(colors[1]))
        keyboard_diary_privilege.row()
        keyboard_diary_privilege.add(Text("Эталонное расписание",
                                          payload=KeyBoards.get_payload("Эталонное расписание")),
                                     color=KeyBoards.get_color(colors[2]))
        keyboard_diary_privilege.row()
        keyboard_diary_privilege.add(Text("Текущее расписание",
                                          payload=KeyBoards.get_payload("Текущее расписание")),
                                     color=KeyBoards.get_color(colors[3]))
        keyboard_diary_privilege.row()
        keyboard_diary_privilege.add(Text("Будущее расписание", payload=KeyBoards.get_payload("Будущее расписание")),
                                     color=KeyBoards.get_color(colors[4]))
        keyboard_diary_privilege.row()

        keyboard_diary_privilege.add(Text("Назад", payload=KeyBoards.get_payload("Назад")))
        keyboard_diary_privilege.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_diary_privilege.get_json()

    # LOOK_CLASSROOM KEYBOARD
    @staticmethod
    def get_look_classroom_keyboard(classroom_type) -> str:
        keyboard_look_classroom_menu = Keyboard()

        if classroom_type == "public":
            keyboard_look_classroom_menu.add(Text("Войти", payload=KeyBoards.get_payload("Войти")))
            keyboard_look_classroom_menu.row()
        elif classroom_type == "invite":
            keyboard_look_classroom_menu.add(Text("Подать заявку", payload=KeyBoards.get_payload("Подать заявку")))
            keyboard_look_classroom_menu.row()
        elif classroom_type == "look_request":
            keyboard_look_classroom_menu.add(Text("Редактировать заявку",
                                                  payload=KeyBoards.get_payload("Редактировать заявку")))
            keyboard_look_classroom_menu.row()

        keyboard_look_classroom_menu.add(Text("Участники", payload=KeyBoards.get_payload("Участники")))
        keyboard_look_classroom_menu.add(Text("Вступить по ссылке",
                                              payload=KeyBoards.get_payload("Вступить по ссылке")))
        keyboard_look_classroom_menu.row()
        keyboard_look_classroom_menu.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_look_classroom_menu.get_json()

    # ROLE_SETTINGS_MENU KEYBOARD
    @staticmethod
    def get_role_settings_menu_keyboard() -> str:
        keyboard_role_settings_menu = Keyboard()
        keyboard_role_settings_menu.add(Text("Сменить имя", payload=KeyBoards.get_payload("Сменить имя")))
        keyboard_role_settings_menu.row()
        keyboard_role_settings_menu.add(Text("Дневник", payload=KeyBoards.get_payload("Дневник")))
        keyboard_role_settings_menu.add(Text("Участники", payload=KeyBoards.get_payload("Участники")))
        keyboard_role_settings_menu.add(Text("Класс", payload=KeyBoards.get_payload("Класс")))
        keyboard_role_settings_menu.row()
        keyboard_role_settings_menu.add(Text("Назад", payload=KeyBoards.get_payload("Назад")))
        keyboard_role_settings_menu.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_role_settings_menu.get_json()

    # EDIT_WEEKDAY KEYBOARD
    @staticmethod
    def get_edit_weekday_keyboard(add_button_color="secondary", redact_button_color="secondary") -> str:
        keyboard_edit_weekday = Keyboard()
        keyboard_edit_weekday.add(Text("Добавить",
                                       payload=KeyBoards.get_payload("Добавить")),
                                  color=KeyBoards.get_color(add_button_color))
        keyboard_edit_weekday.add(Text("Удалить урок",
                                       payload=KeyBoards.get_payload("Удалить урок")))
        keyboard_edit_weekday.add(Text("Изменить",
                                       payload=KeyBoards.get_payload("Изменить")),
                                  color=KeyBoards.get_color(redact_button_color))
        keyboard_edit_weekday.row()
        keyboard_edit_weekday.add(Text("Удалить всё",
                                       payload=KeyBoards.get_payload("Удалить всё")))
        keyboard_edit_weekday.row()
        keyboard_edit_weekday.add(Text("Отменить",
                                       payload=KeyBoards.get_payload("Отменить")),
                                  color=KeyboardButtonColor.NEGATIVE)
        keyboard_edit_weekday.add(Text("Сохранить",
                                       payload=KeyBoards.get_payload("Сохранить")),
                                  color=KeyboardButtonColor.POSITIVE)
        keyboard_edit_weekday.row()
        keyboard_edit_weekday.add(Text("Главное меню",
                                       payload=KeyBoards.get_payload("Главное меню")),
                                  color=KeyboardButtonColor.PRIMARY)

        return keyboard_edit_weekday.get_json()

    # ACCESS_MENU_BACK KEYBOARD
    @staticmethod
    def get_access_menu_back_keyboard(public_color="secondary", invite_color="secondary",
                                      close_color="secondary") -> str:
        keyboard_access_menu_back = Keyboard()
        keyboard_access_menu_back.add(Text("Публичный", payload=KeyBoards.get_payload("Публичный")),
                                      color=KeyBoards.get_color(public_color))
        keyboard_access_menu_back.add(Text("Заявки", payload=KeyBoards.get_payload("Заявки")),
                                      color=KeyBoards.get_color(invite_color))
        keyboard_access_menu_back.add(Text("Закрытый", payload=KeyBoards.get_payload("Закрытый")),
                                      color=KeyBoards.get_color(close_color))
        keyboard_access_menu_back.row()
        keyboard_access_menu_back.add(Text("Назад", payload=KeyBoards.get_payload("Назад")))
        keyboard_access_menu_back.add(Text("Главное меню", payload=KeyBoards.get_payload("Главное меню")))

        return keyboard_access_menu_back.get_json()
