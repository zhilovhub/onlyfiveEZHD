from config import *

from keyboards import KeyBoards


class SupportingFunctions:
    """Some functions that can be used in handlers.py and main.py"""

    def __init__(self, token: str, group_id: int) -> None:
        """Initialization"""
        self.vk_session = VkApi(token=token)
        self.bot_long_poll = VkBotLongPoll(vk=self.vk_session, group_id=group_id)

    def send_message(self, user_id: int, message: str, keyboard=None) -> None:
        """Send message to user"""
        try:
            self.vk_session.method(
                "messages.send",
                {
                    "user_id": user_id,
                    "message": message,
                    "keyboard": keyboard,
                    "random_id": randint(0, 2 ** 10)
                }
            )
        except VkApiError as e:
            print(e)

    def send_message_event_answer(self, event_id: str, user_id: int, peer_id: int, event_data: str) -> None:
        """Send message to user after callback-button using"""
        try:
            self.vk_session.method(
                "messages.sendMessageEventAnswer",
                {
                    "event_id": event_id,
                    "user_id": user_id,
                    "peer_id": peer_id,
                    "event_data": event_data
                }
            )

        except VkApiError as e:
            print(e)

    @staticmethod
    def get_keyboard(keyboard_type: str) -> VkKeyboard:
        """Get the keyboard"""
        if keyboard_type == "empty":
            return KeyBoards.KEYBOARD_EMPTY.get_empty_keyboard()

        elif keyboard_type == "menu":
            return KeyBoards.KEYBOARD_MENU.get_keyboard()

        elif keyboard_type == "cancel_back":
            return KeyBoards.KEYBOARD_CANCEL_BACK.get_keyboard()

        elif keyboard_type == "cancel":
            return KeyBoards.KEYBOARD_CANCEL.get_keyboard()

        elif keyboard_type == "yes_no_cancel_back":
            return KeyBoards.KEYBOARD_YES_NO_CANCEL_BACK.get_keyboard()

        elif keyboard_type == "submit_back":
            return KeyBoards.KEYBOARD_SUBMIT_BACK.get_keyboard()

        elif keyboard_type == "my_class_menu":
            return KeyBoards.KEYBOARD_MY_CLASS_MENU.get_keyboard()

        elif keyboard_type == "timetable_menu":
            return KeyBoards.TIMETABLE_MENU_KEYBOARD.get_keyboard()

        elif keyboard_type == "timetable":
            return KeyBoards.TIMETABLE_KEYBOARD.get_keyboard()

        elif keyboard_type == "standard_week":
            return KeyBoards.STANDARD_WEEK_KEYBOARD.get_keyboard()

    def is_member(self, user_id: int) -> int:
        """Check is user member of the group"""
        is_member = self.vk_session.method(
            "groups.isMember",
            {
                "group_id": GROUP_ID,
                "user_id": user_id
            }
        )

        return is_member

    def get_user_info(self, user_id: int) -> dict:
        """Get information about user"""
        user_information = self.vk_session.method(
            "users.get",
            {
                "user_ids": user_id,
                "fields": "screen_name"
            }
        )[0]

        return {
            "user_id": user_id,
            "screen_name": user_information["screen_name"],
            "first_name": user_information["first_name"]
        }