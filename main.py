from handlers import *

from json import loads


class DiaryVkBot(CallbackPayloadHandlers):
    """Listens events and filtering States/CallbackPayloads"""

    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db,
                         classroom_db=classroom_db, technical_support_db=technical_support_db,
                         diary_homework_db=diary_homework_db)

    def listen(self) -> None:
        """Listening events"""
        for event in self.bot_long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_user:
                    user_id = event.object.message["from_id"]  # Getting user_id
                    message = event.object.message["text"]  # Getting message's text
                    payload = loads(event.object.message["payload"]) if "payload" in event.object.message else None  # Payload

                    user_information = self.get_user_info(user_id)  # User_id, first_name, nickname

                    self.user_db.insert_new_user(user_id,
                                                 user_information["screen_name"],
                                                 user_information["first_name"],
                                                 False
                                                 )  # Will add a new user if user writes his first message
                    self.classroom_db.insert_new_customizer(user_id)

                    if self.is_member(user_id):  # Checking first condition

                        if self.user_db.check_user_is_ready(user_id):  # Checking second condition
                            current_dialog_state = self.user_db.get_user_dialog_state(user_id)
                            self.filter_dialog_state(user_id, message, payload, current_dialog_state)
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

            case States.S_EDIT_STANDARD_WEEK_MYCLASSES.value:
                self.s_edit_standard_week_my_classes_handler(user_id, payload)

            case States.S_EDIT_STANDARD_WEEKDAY_MYCLASSES.value:
                self.s_edit_standard_weekday_my_classes_handler(user_id, payload)

            # TECHNICALSUPPORT
            case States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE.value:
                self.s_enter_technical_support_message_handler(user_id, message)

    def filter_callback_button_payload(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Filtering payload types"""
        match payload["text"]:
            case "enter_the_classroom":
                self.p_enter_the_classroom_handler(user_id, payload, current_dialog_state)

            case "Изменить эталонное расписание":
                self.p_edit_standard_week_handler(user_id, payload, current_dialog_state)


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
    diary_homework_db= DiaryHomeworkCommands(connection)

    my_bot = DiaryVkBot(token=TOKEN, group_id=GROUP_ID,
                        user_db=user_db,
                        classroom_db=classroom_db,
                        technical_support_db=technical_support_db,
                        diary_homework_db=diary_homework_db
                        )

    my_bot.listen()
