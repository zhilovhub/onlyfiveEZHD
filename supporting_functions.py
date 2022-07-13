from databases import *

from keyboards import KeyBoards
from states import States


class SupportingFunctions:
    """Some functions that can be used in handlers and main.py"""

    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands) -> None:
        """Initialization"""
        self.user_db = user_db
        self.classroom_db = classroom_db
        self.technical_support_db = technical_support_db
        self.diary_homework_db = diary_homework_db
        self.role_db = role_db
        self.notification_db = notification_db

        self.vk_session = VkApi(token=token)
        self.bot_long_poll = VkBotLongPoll(vk=self.vk_session, group_id=group_id)

    def send_message(self, user_id: int, message=None, keyboard=None, template=None) -> None:
        """Send message to user"""
        try:
            self.vk_session.method(
                "messages.send",
                {
                    "user_id": user_id,
                    "message": message,
                    "keyboard": keyboard,
                    "template": template,
                    "random_id": randint(0, 2147483648)
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

    def state_transition(self, user_id: int, next_state, message: str, *args, **kwargs) -> None:
        """Changes states"""
        match next_state:
            case States.S_NOTHING:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_MENU.get_keyboard())

            # CLASSCREATE
            case States.S_ENTER_CLASS_NAME_CLASSCREATE:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_JUST_MENU.get_keyboard())

            case States.S_ENTER_SCHOOL_NAME_CLASSCREATE:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_ENTER_ACCESS_CLASSCREATE:
                self.send_message(user_id, message,
                                  KeyBoards.get_access_menu_back_keyboard())

            case States.S_ENTER_DESCRIPTION_CLASSCREATE:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_SUBMIT_CLASSCREATE:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_SUBMIT_BACK.get_keyboard())

            # MYCLASSES
            case States.S_IN_CLASS_MYCLASSES:
                self.send_message(user_id, message,
                                  KeyBoards.get_my_class_menu_keyboard(**kwargs))

            case States.S_IN_CLASS_MYCLASSES2:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
                members_role_properties_dictionary = self.role_db.get_members_role_properties_dict(role_id)

                accept_requests = members_role_properties_dictionary["accept_requests"]

                self.send_message(user_id, message,
                                  KeyBoards.get_my_class_menu2_keyboard(**kwargs, accept_requests=accept_requests))

            case States.S_EDIT_WEEK_MYCLASSES:
                self.send_message(user_id, message,
                                  KeyBoards.get_edit_week_keyboard(**kwargs))

            case States.S_EDIT_WEEKDAY_MYCLASSES:
                self.send_message(user_id, message,
                                  KeyBoards.get_edit_weekday_keyboard())

            case States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES:
                self.send_message(user_id, message,
                                  KeyBoards.get_edit_weekday_keyboard(add_button_color="positive"))

            case States.S_EDIT_LESSON_WEEKDAY_MYCLASSES:
                self.send_message(user_id, message,
                                  KeyBoards.get_edit_weekday_keyboard(redact_button_color="positive"))

            case States.S_EDIT_HOMEWORK_MYCLASSES:
                self.send_message(user_id, message, KeyBoards.get_edit_homework_keyboard())

            case States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES:
                self.send_message(user_id, message, KeyBoards.get_edit_homework_weekday_keyboard())

            # FINDCLASS
            case States.S_FIND_CLASS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_JUST_MENU.get_keyboard())

            case States.S_LOOK_CLASSROOM:
                self.send_message(user_id, message,
                                  KeyBoards.get_look_classroom_keyboard(**kwargs))

            case States.S_REQUEST_CLASSROOM:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_EDIT_REQUEST_CLASSROOM:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU_DELETE_REQUEST.get_keyboard())

            # CLASSROOMSETTINGS
            case States.S_CLASSROOM_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_CLASSROOM_SETTINGS.get_keyboard())

            case States.S_MAIN_CLASSROOM_SETTINGS:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
                classroom_role_properties_dictionary = self.role_db.get_classroom_role_properties_dict(role_id)

                classroom_role_properties_dictionary.pop("role_name", None)
                classroom_role_properties_dictionary.pop("is_default_member", None)
                classroom_role_properties_dictionary.pop("is_admin", None)

                self.send_message(user_id, message,
                                  KeyBoards.get_main_classroom_settings(**classroom_role_properties_dictionary))

            case States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
                admin_role_id = self.role_db.get_admin_role_id(classroom_id)

                is_admin = role_id == admin_role_id

                self.send_message(user_id, message,
                                  KeyBoards.get_main_dangerous_zone_classroom_settings_keyboard(is_admin=is_admin))

            case States.S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.get_keyboard())

            case States.S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.get_keyboard())

            case States.S_ACCESS_MAIN_CLASSROOM_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.get_access_menu_back_keyboard(**kwargs))

            case States.S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_LIMIT_MAIN_CLASSROOM_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_NOTIFICATION_SETTINGS_CLASSROOM_SETTINGS:
                self.send_message(user_id, message, KeyBoards.get_notification_settings_keyboard())

            # TECHNICALSUPPORT
            case States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_CANCEL_SEND.get_keyboard())

            # MEMBERSSETTINGS
            case States.S_MEMBERS_SETTINGS:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
                admin_role_id = self.role_db.get_admin_role_id(classroom_id)
                is_admin = role_id == admin_role_id

                members_role_properties_dictionary = self.role_db.get_members_role_properties_dict(role_id)

                kick_members = members_role_properties_dictionary["kick_members"]
                invite_members = members_role_properties_dictionary["invite_members"]

                self.send_message(user_id, message,
                                  KeyBoards.get_members_settings_keyboard(is_admin, kick_members, invite_members))

            case States.S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_DELETE_ROLE_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_DELETE_MEMBER_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_CHOOSE_ROLE_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_CHOOSE_ADMIN_ROLE_CONFIRMATION_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.get_keyboard())

            case States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_EDIT_ROLE_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.get_role_settings_menu_keyboard())

            case States.S_ENTER_NAME_EDIT_ROLE_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.KEYBOARD_BACK_MENU.get_keyboard())

            case States.S_DIARY_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.get_diary_privilege_keyboard(args))

            case States.S_MEMBERS_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.get_members_privilege_keyboard(args))

            case States.S_CLASSROOM_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS:
                self.send_message(user_id, message,
                                  KeyBoards.get_classroom_privilege_keyboard(args))

        self.user_db.set_user_dialog_state(user_id, next_state.value)

    def trans_to_main_menu(self, user_id: int) -> None:
        """Change user's state into S_NOTHING"""
        trans_message = "Возвращение в главное меню"
        self.classroom_db.update_user_customize_classroom_id(user_id, "null")
        self.role_db.update_user_customize_role_id(user_id, "null")
        self.state_transition(user_id, States.S_NOTHING, trans_message)

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
            "first_name": user_information["first_name"],
            "last_name": user_information["last_name"]
        }

    def get_members_text(self, roles_dictionary: dict) -> str:
        members_text = ""
        ind = 1
        for role_id, member_ids in roles_dictionary.items():
            role_name = self.role_db.get_role_name(role_id)
            members_text += f"{role_name}\n"

            for member_id in member_ids:
                first_name, last_name = self.user_db.get_user_first_and_last_name(member_id)
                members_text += f"{ind}. [id{member_id}|{first_name} {last_name}]\n"
                ind += 1
            members_text += "\n"

        return members_text

    def get_look_keyboard_kwargs(self, user_id: int, classroom_id: int) -> str:
        """Returns look keyboard's kwargs"""
        request_information = self.classroom_db.get_request_information(user_id, classroom_id)

        if request_information:
            return "look_request"
        else:
            access_keyboard_dict = {
                "Публичный": "public",
                "Заявки": "invite",
                "Закрытый": "close"
            }

            access = self.classroom_db.get_classroom_access(classroom_id)
            return access_keyboard_dict[access]

    @staticmethod
    def get_all_role_names_text(all_role_names: list, admin_role_name: str, default_role_name: str) -> str:
        """Returns text of all role names"""
        role_names = []
        for role_name in all_role_names:
            if role_name == admin_role_name:
                role_names.append(f"{role_name} (Админ)")
            elif role_name == default_role_name:
                role_names.append(f"{role_name} (Дефолт)")
            else:
                role_names.append(role_name)

        role_names_text = "\n".join([f"{ind}. {role_name}" for ind, role_name in enumerate(role_names, start=1)])
        return role_names_text

    def get_sign(self, user_id: int) -> bool:
        """Returns sign"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        request_list = self.classroom_db.get_list_of_request_information(classroom_id)

        return True if request_list else False
