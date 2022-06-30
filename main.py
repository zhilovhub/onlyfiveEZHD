from handlers import *


class DiaryVkBot(CallbackPayloadHandlers):
    """Listens events and filtering States/CallbackPayloads"""

    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db,
                         classroom_db=classroom_db, technical_support_db=technical_support_db,
                         diary_homework_db=diary_homework_db, role_db=role_db)

    def listen(self) -> None:
        """Listening events"""
        for event in self.bot_long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_user:
                    user_id = event.object.message["from_id"]  # Getting user_id
                    message = event.object.message["text"]  # Getting message's text
                    attachments = event.object.message["attachments"]
                    payload = loads(
                        event.object.message["payload"]) if "payload" in event.object.message else None  # Payload

                    user_information = self.get_user_info(user_id)  # User_id, first_name, nickname

                    self.user_db.insert_new_user(user_id,
                                                 user_information["screen_name"],
                                                 user_information["first_name"],
                                                 user_information["last_name"],
                                                 False
                                                 )  # Will add a new user if user writes his first message
                    self.classroom_db.insert_new_customizer(user_id)

                    if self.is_member(user_id):  # Checking first condition

                        if self.user_db.check_user_is_ready(user_id):  # Checking second condition

                            if not attachments:  # Checking user didn't send attachment
                                self.diary_homework_db.update_change_current_and_next_diary()

                                current_dialog_state = self.user_db.get_user_dialog_state(user_id)
                                self.filter_dialog_state(user_id, message, payload, current_dialog_state)
                            else:
                                self.send_message(user_id, "Пиши текстом... Или используй кнопки для навигации!👇🏻")
                        else:
                            self.user_db.set_user_is_ready(
                                user_id)  # First condition is True but this is a first user's message
                            self.send_message(user_id, "Добро пожаловать в наше сообщество!\n"
                                                       "Что может наш бот? (Инструкция)",
                                              self.get_keyboard("menu"))
                    else:
                        self.send_message(user_id,  # User is not a member
                                          "Перед использованием бота подпишись на группу!",
                                          self.get_keyboard("empty"))
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                event_id = event.object["event_id"]
                user_id = event.object["user_id"]
                peer_id = event.object["peer_id"]
                payload = event.object["payload"]

                self.send_message_event_answer(event_id, user_id, peer_id, "")
                if self.is_member(user_id):
                    current_dialog_state = self.user_db.get_user_dialog_state(user_id)
                    self.filter_callback_button_payload(user_id, payload, current_dialog_state)
                else:
                    self.send_message(user_id,
                                      "Перед использованием бота подпишись на группу!",
                                      self.get_keyboard("empty"))

            else:
                print(event)

    def filter_dialog_state(self, user_id: int, message: str, payload: dict, current_dialog_state: int) -> None:
        """Filtering dialog states"""
        match current_dialog_state:
            case States.S_NOTHING.value:
                self.s_nothing_handler(user_id, payload)

            # CLASSCREATE
            case States.S_ENTER_CLASS_NAME_CLASSCREATE.value:
                self.s_enter_class_name_class_create_handler(user_id, message, payload)

            case States.S_ENTER_SCHOOL_NAME_CLASSCREATE.value:
                self.s_enter_school_name_class_create_handler(user_id, message, payload)

            case States.S_ENTER_ACCESS_CLASSCREATE.value:
                self.s_enter_access_class_create_handler(user_id, payload)

            case States.S_ENTER_DESCRIPTION_CLASSCREATE.value:
                self.s_enter_description_class_create_handler(user_id, message, payload)

            case States.S_SUBMIT_CLASSCREATE.value:
                self.s_submit_class_create_handler(user_id, payload)

            # MYCLASSES
            case States.S_IN_CLASS_MYCLASSES.value:
                self.s_in_class_my_classes_handler(user_id, payload)

            case States.S_EDIT_WEEK_MYCLASSES.value:
                self.s_edit_week_my_classes_handler(user_id, payload)

            case States.S_EDIT_WEEKDAY_MYCLASSES.value:
                self.s_edit_weekday_my_classes_handler(user_id, payload)

            case States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES.value:
                self.s_add_new_lesson_weekday_my_classes_handler(user_id, message, payload)

            case States.S_EDIT_LESSON_WEEKDAY_MYCLASSES.value:
                self.s_edit_lesson_weekday_my_classes_handler(user_id, message, payload)

            # FINDCLASS
            case States.S_FIND_CLASS.value:
                self.s_find_class_handler(user_id, message, payload)

            # CLASSROOMSETTINGS
            case States.S_CLASSROOM_SETTINGS.value:
                self.s_classroom_settings_handler(user_id, payload)

            case States.S_MAIN_CLASSROOM_SETTINGS.value:
                self.s_main_classroom_settings_handler(user_id, payload)

            case States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS.value:
                self.s_main_dangerous_zone_classroom_settings_handler(user_id, payload)

            case States.S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.value:
                self.s_main_dangerous_zone_delete_one_classroom_settings_handler(user_id, payload)

            case States.S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.value:
                self.s_main_dangerous_zone_delete_two_classroom_settings_handler(user_id, payload)

            case States.S_ACCESS_MAIN_CLASSROOM_SETTINGS.value:
                self.s_access_main_classroom_settings_handler(user_id, payload)

            case States.S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS.value:
                self.s_classroom_name_main_classroom_settings_handler(user_id, message, payload)

            case States.S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS.value:
                self.s_school_name_main_classroom_settings_handler(user_id, message, payload)

            case States.S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS.value:
                self.s_description_main_classroom_settings_handler(user_id, message, payload)

            case States.S_LIMIT_MAIN_CLASSROOM_SETTINGS.value:
                self.s_limit_main_classroom_settings_handler(user_id, message, payload)

            # TECHNICALSUPPORT
            case States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE.value:
                self.s_enter_technical_support_message_handler(user_id, message)

            # MEMBERSSETTINGS
            case States.S_MEMBERS_SETTINGS.value:
                self.s_members_settings_handler(user_id, payload)

            case States.S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS.value:
                self.s_add_role_enter_name_members_settings_handler(user_id, message, payload)

            case States.S_DELETE_ROLE_MEMBERS_SETTINGS.value:
                self.s_delete_role_members_settings_handler(user_id, message, payload)

            case States.S_DELETE_MEMBER_MEMBERS_SETTINGS.value:
                self.s_delete_member_members_settings_handler(user_id, message, payload)

    def filter_callback_button_payload(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Filtering payload types"""
        match payload["text"]:
            case "enter_the_classroom":
                self.p_enter_the_classroom_handler(user_id, payload, current_dialog_state)

            case ("edit_standard" | "edit_current" | "edit_next"):
                self.p_edit_week_handler(user_id, payload, current_dialog_state)

            case "enter_members_settings":
                self.p_enter_members_settings(user_id, payload, current_dialog_state)


if __name__ == "__main__":
    with connect(
            host=HOST,
            user=USER,
            password=PASSWORD
    ) as connection_to_create_db:
        with connection_to_create_db.cursor() as cursor:
            cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}""")

    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    user_db = UserDataCommands(connection)
    classroom_db = ClassroomCommands(connection)
    technical_support_db = TechnicalSupportCommands(connection)
    diary_homework_db = DiaryHomeworkCommands(connection)
    role_db = RoleCommands(connection)

    my_bot = DiaryVkBot(token=TOKEN, group_id=GROUP_ID,
                        user_db=user_db,
                        classroom_db=classroom_db,
                        technical_support_db=technical_support_db,
                        diary_homework_db=diary_homework_db,
                        role_db=role_db
                        )

    my_bot.listen()
