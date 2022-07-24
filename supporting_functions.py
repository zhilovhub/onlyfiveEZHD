from databases import *

from keyboards import KeyBoards
from states import States


class SupportingFunctions:
    """Some functions that can be used in handlers and main.py"""

    def __init__(self, bot: Bot, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands, event_db: EventCommands) -> None:
        """Initialization"""
        self.user_db = user_db
        self.classroom_db = classroom_db
        self.technical_support_db = technical_support_db
        self.diary_homework_db = diary_homework_db
        self.role_db = role_db
        self.notification_db = notification_db
        self.event_db = event_db

        self.bot = bot

    async def send_message(self, user_id=None, message=None, keyboard=None, template=None, user_ids=None) -> None:
        """Send message to user"""
        await self.bot.api.messages.send(
            user_ids=[user_id] if not user_ids else ",".join(map(str, user_ids)),
            message=message,
            keyboard=keyboard if user_id else None,
            template=template,
            random_id=randint(0, 2147483648)
        )

    async def send_message_event_answer(self, event_id: str, user_id: int, peer_id: int, event_data: str) -> None:
        """Send message to user after callback-button using"""
        await self.bot.api.messages.send_message_event_answer(
            event_id=event_id,
            user_id=user_id,
            peer_id=peer_id,
            event_data=event_data
        )

    async def state_transition(self, user_id: int, next_state, message: str, *args, **kwargs) -> None:
        """Changes states"""
        match next_state:
            case States.S_NOTHING:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_MENU.get_json())

            # CLASSCREATE
            case States.S_ENTER_CLASS_NAME_CLASSCREATE:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_JUST_MENU.get_json())

            case States.S_ENTER_SCHOOL_NAME_CLASSCREATE:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_ENTER_ACCESS_CLASSCREATE:
                await self.send_message(user_id, message,
                                        KeyBoards.get_access_menu_back_keyboard())

            case States.S_ENTER_DESCRIPTION_CLASSCREATE:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_SUBMIT_CLASSCREATE:
                await self.send_message(user_id, message,
                                        KeyBoards.get_submit_back_keyboard())

            # MYCLASSES
            case States.S_IN_CLASS_MYCLASSES:
                await self.send_message(user_id, message,
                                        KeyBoards.get_my_class_menu_keyboard(**kwargs))

            case States.S_IN_CLASS_MYCLASSES2:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
                members_role_properties_dictionary = self.role_db.get_members_role_properties_dict(role_id)

                accept_requests = members_role_properties_dictionary["accept_requests"]

                await self.send_message(user_id, message,
                                        KeyBoards.get_my_class_menu2_keyboard(**kwargs,
                                                                              accept_requests=accept_requests))

            case States.S_EDIT_WEEK_MYCLASSES:
                await self.send_message(user_id, message,
                                        KeyBoards.get_edit_week_keyboard(**kwargs))

            case States.S_EDIT_WEEKDAY_MYCLASSES:
                await self.send_message(user_id, message,
                                        KeyBoards.get_edit_weekday_keyboard())

            case States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES:
                await self.send_message(user_id, message,
                                        KeyBoards.get_edit_weekday_keyboard(add_button_color="positive"))

            case States.S_EDIT_LESSON_WEEKDAY_MYCLASSES:
                await self.send_message(user_id, message,
                                        KeyBoards.get_edit_weekday_keyboard(redact_button_color="positive"))

            case States.S_EDIT_HOMEWORK_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.get_edit_homework_keyboard())

            case States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.get_edit_homework_weekday_keyboard())

            case States.S_CHOOSE_EVENT_MYCLASSES:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)

                classroom_events = self.event_db.get_all_classroom_events(classroom_id)
                sorted_events = sorted(classroom_events, key=lambda x: x["message_event_id"])

                members_role_properties_dictionary = self.role_db.get_members_role_properties_dict(role_id)
                redact_events = members_role_properties_dictionary.get("redact_events", False)

                await self.send_message(user_id, message,
                                        KeyBoards.get_choose_event_keyboard(sorted_events, redact_events=redact_events))

            case States.S_CHOOSE_EVENT_TYPE_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.get_choose_event_type_keyboard())

            case States.S_ENTER_NOT_COLLECTIVE_EVENT_NAME_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.KEYBOARD_BACK_MENU)

            case States.S_ENTER_NOT_COLLECTIVE_EVENT_START_TIME_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.KEYBOARD_BACK_MENU)

            case States.S_ENTER_NOT_COLLECTIVE_EVENT_END_TIME_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.get_back_menu_skip_keyboard())

            case States.S_ENTER_COLLECTIVE_EVENT_NAME_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.KEYBOARD_BACK_MENU)

            case States.S_ENTER_COLLECTIVE_EVENT_START_TIME_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.KEYBOARD_BACK_MENU)

            case States.S_ENTER_COLLECTIVE_EVENT_END_TIME_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.get_back_menu_skip_keyboard())

            case States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_COUNT_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.get_back_menu_skip_keyboard())

            case States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_STUDENT_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.get_back_menu_skip_keyboard())

            case States.S_SUBMIT_EVENT_CREATE_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.get_submit_back_keyboard(**kwargs))

            case States.S_EDIT_EVENT_MYCLASSES:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                event_id = self.event_db.get_customizing_event_id(user_id)
                event = self.event_db.get_classroom_event(event_id)

                event_students = self.event_db.get_event_students(event_id)
                student_id = self.classroom_db.get_student_id(user_id, classroom_id)

                await self.send_message(user_id, message,
                                        KeyBoards.get_edit_event_keyboard(event=event,
                                                                          has_joined=student_id in event_students))

            case States.S_ADD_COUNT_COLLECTIVE_EVENT_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.KEYBOARD_BACK_MENU)

            case States.S_DECREASE_COUNT_COLLECTIVE_EVENT_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.KEYBOARD_BACK_MENU)

            case States.S_EVENT_SETTINGS_MYCLASSES:
                await self.send_message(user_id, message, KeyBoards.get_event_settings_keyboard())

            # FINDCLASS
            case States.S_FIND_CLASS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_JUST_MENU.get_json())

            case States.S_LOOK_CLASSROOM:
                await self.send_message(user_id, message,
                                        KeyBoards.get_look_classroom_keyboard(**kwargs))

            case States.S_REQUEST_CLASSROOM:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_EDIT_REQUEST_CLASSROOM:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU_DELETE_REQUEST.get_json())

            # CLASSROOMSETTINGS
            case States.S_CLASSROOM_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_CLASSROOM_SETTINGS.get_json())

            case States.S_MAIN_CLASSROOM_SETTINGS:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
                classroom_role_properties_dictionary = self.role_db.get_classroom_role_properties_dict(role_id)

                classroom_role_properties_dictionary.pop("role_name", None)
                classroom_role_properties_dictionary.pop("is_default_member", None)
                classroom_role_properties_dictionary.pop("is_admin", None)

                await self.send_message(user_id, message,
                                        KeyBoards.get_main_classroom_settings(**classroom_role_properties_dictionary))

            case States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
                admin_role_id = self.role_db.get_admin_role_id(classroom_id)

                is_admin = role_id == admin_role_id

                await self.send_message(user_id, message,
                                        KeyBoards.get_main_dangerous_zone_classroom_settings_keyboard(
                                            is_admin=is_admin))

            case States.S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.
                                        get_json())

            case States.S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.
                                        get_json())

            case States.S_ACCESS_MAIN_CLASSROOM_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.get_access_menu_back_keyboard(**kwargs))

            case States.S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_LIMIT_MAIN_CLASSROOM_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_NOTIFICATION_SETTINGS_CLASSROOM_SETTINGS:
                value_meaning_dict = {
                    1: "positive",
                    0: "negative"
                }
                buttons_colors = list(map(lambda x: value_meaning_dict[x], args))

                await self.send_message(user_id, message,
                                        KeyBoards.get_notification_settings_keyboard(colors=buttons_colors))

            # TECHNICALSUPPORT
            case States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_CANCEL_SEND.get_json())

            # MEMBERSSETTINGS
            case States.S_MEMBERS_SETTINGS:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_id = self.role_db.get_role_id_by_user_id(user_id, classroom_id)
                admin_role_id = self.role_db.get_admin_role_id(classroom_id)
                is_admin = role_id == admin_role_id

                members_role_properties_dictionary = self.role_db.get_members_role_properties_dict(role_id)

                kick_members = members_role_properties_dictionary["kick_members"]
                invite_members = members_role_properties_dictionary["invite_members"]

                await self.send_message(user_id, message,
                                        KeyBoards.get_members_settings_keyboard(is_admin, kick_members, invite_members))

            case States.S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_DELETE_ROLE_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_DELETE_MEMBER_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_CHOOSE_ROLE_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_CHOOSE_ADMIN_ROLE_CONFIRMATION_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS
                                        .get_json())

            case States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_EDIT_ROLE_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.get_role_settings_menu_keyboard())

            case States.S_ENTER_NAME_EDIT_ROLE_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.KEYBOARD_BACK_MENU.get_json())

            case States.S_DIARY_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.get_diary_privilege_keyboard(args))

            case States.S_MEMBERS_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.get_members_privilege_keyboard(args))

            case States.S_CLASSROOM_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS:
                await self.send_message(user_id, message,
                                        KeyBoards.get_classroom_privilege_keyboard(args))

        self.user_db.set_user_dialog_state(user_id, next_state.value)

    async def trans_to_main_menu(self, user_id: int) -> None:
        """Change user's state into S_NOTHING"""
        trans_message = "Возвращение в главное меню"
        self.classroom_db.update_user_customize_classroom_id(user_id, "null")
        self.role_db.update_user_customize_role_id(user_id, "null")
        self.event_db.update_customizing_event_id(user_id, None)
        await self.state_transition(user_id, States.S_NOTHING, trans_message)

    async def is_member(self, user_id: int) -> int:
        """Check is user member of the group"""
        is_member = await self.bot.api.groups.is_member(group_id=GROUP_ID, user_id=user_id)

        return is_member.value

    async def get_user_info(self, user_id: int) -> dict:
        """Get information about user"""
        user_information = (await self.bot.api.users.get(user_ids=[user_id], fields=["screen_name"]))[0]

        return {
            "user_id": user_id,
            "screen_name": user_information.screen_name,
            "first_name": user_information.first_name,
            "last_name": user_information.last_name
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

    def insert_new_student(self, user_id: int, classroom_id: int, role_id: int) -> None:
        """Inserts new student"""
        student_id = self.classroom_db.insert_new_user_in_classroom(user_id, classroom_id, role_id)
        self.notification_db.insert_new_notification(student_id, user_id, classroom_id)

    async def notify_new_classmate(self, user_id: int, classroom_id: int, without_user_ids=None) -> None:
        """Notifies about new classmate"""
        notified_users = self.notification_db.get_users_with_notification_type(classroom_id, "new_classmate")
        if without_user_ids:
            for without_user_id in without_user_ids:
                if without_user_id in notified_users:
                    notified_users.remove(without_user_id)

        if notified_users:
            first_name, last_name = self.user_db.get_user_first_and_last_name(user_id)
            classroom_name = self.classroom_db.get_classroom_name(classroom_id)

            await self.send_message(user_ids=notified_users,
                                    message=f"[id{user_id}|{first_name} {last_name}] вступил в "
                                            f"{classroom_name}!")

    async def notify_request(self, user_id: int, classroom_id: int) -> None:
        """Notifies about request"""
        notified_users = self.notification_db.get_users_with_notification_type(classroom_id, "requests")
        if notified_users:
            first_name, last_name = self.user_db.get_user_first_and_last_name(user_id)
            classroom_name = self.classroom_db.get_classroom_name(classroom_id)

            await self.send_message(user_ids=notified_users,
                                    message=f"[id{user_id}|{first_name} {last_name}] хочет вступить "
                                            f"в {classroom_name}!")

    async def notify_leave_classmate(self, user_id: int, classroom_id: int, kicked: bool,
                                     without_user_ids=None) -> None:
        """Notifies about left classmate"""
        notified_users = self.notification_db.get_users_with_notification_type(classroom_id, "leave_classmate")
        if without_user_ids:
            for without_user_id in without_user_ids:
                if without_user_id in notified_users:
                    notified_users.remove(without_user_id)

        if notified_users:
            first_name, last_name = self.user_db.get_user_first_and_last_name(user_id)
            classroom_name = self.classroom_db.get_classroom_name(classroom_id)

            if kicked:
                await self.send_message(user_ids=notified_users, message=f"[id{user_id}|{first_name} {last_name}] "
                                                                         f"исключён из {classroom_name}!")
            else:
                await self.send_message(user_ids=notified_users, message=f"[id{user_id}|{first_name} {last_name}]"
                                                                         f" покинул {classroom_name}!")

    @staticmethod
    def get_event_diary_text(classroom_events: list) -> str:
        """Returns text of events"""
        def formatted_date(date: date) -> str:
            weekday_dict = {
                0: "ПОНЕДЕЛЬНИК",
                1: "ВТОРНИК",
                2: "СРЕДА",
                3: "ЧЕТВЕРГ",
                4: "ПЯТНИЦА",
                5: "СУББОТА",
                6: "ВОСКРЕСЕНЬЕ"
            }

            month_dict = {
                1: "Янв",
                2: "Фев",
                3: "Мар",
                4: "Апр",
                5: "Май",
                6: "Июн",
                7: "Июл",
                8: "Авг",
                9: "Сен",
                10: "Окт",
                11: "Ноя",
                12: "Дек",
            }
            weekday = weekday_dict[date.weekday()]
            month = month_dict[date.month]

            return f"{weekday}, {date.day} {month}, {date.year}"

        def formatted_collective_event(start_time: datetime, end_time: datetime, label: str, message_event_id: int,
                                       current_count: int, required_count: int, current_students_count: int,
                                       required_students_count: int, finished: int) -> str:
            start_time_date = start_time.strftime("%d.%m.%y")
            if end_time:
                end_time_date = end_time.strftime("%d.%m.%y")
                duration_time = f"{start_time_date} - {end_time_date}"
                emoji = "✅" if datetime.now() > end_time or finished else ""
            else:
                duration_time = start_time_date
                emoji = "✅" if datetime.now() > start_time or finished else ""

            if required_count:
                collected = f"\nСобрано: {current_count}/{required_count}"
            else:
                collected = ""

            if required_students_count:
                student_count_text = f"\nУчастники: {current_students_count}/{required_students_count}"
            else:
                student_count_text = ""

            return f"⚠ {duration_time} {label} (#{message_event_id}) {emoji}{collected}{student_count_text}"

        def formatted_not_collective_event(start_time: datetime, end_time: datetime, label: str, message_event_id: int,
                                           finished: int) -> str:
            start_time_hour_minute = start_time.strftime("%H:%M")
            if end_time:
                end_time_hour_minute = end_time.strftime("%H:%M")
                duration_time = f"{start_time_hour_minute}-{end_time_hour_minute}"
                emoji = "✅" if datetime.now() > end_time or finished else ""
            else:
                duration_time = start_time_hour_minute
                emoji = "✅" if datetime.now() > start_time or finished else ""

            return f"{duration_time} {label} (#{message_event_id}) {emoji}"

        collective_events = []
        days = {}
        for event in classroom_events:
            start_time: datetime = event["start_time"]
            end_time: datetime = event["end_time"]
            label = event["label"]
            message_event_id = event["message_event_id"]
            collective = event["collective"]
            current_count = event["current_count"]
            required_count = event["required_count"]
            current_students_count = event["current_students_count"]
            required_students_count = event["required_students_count"]
            finished = event["finished"]

            if collective:
                collective_events.append(formatted_collective_event(start_time, end_time, label, message_event_id,
                                                                    current_count, required_count,
                                                                    current_students_count, required_students_count,
                                                                    finished))
            else:
                if start_time.date() in days:
                    days[start_time.date()].append(formatted_not_collective_event(start_time, end_time,
                                                                                  label, message_event_id, finished))
                else:
                    days[start_time.date()] = [formatted_not_collective_event(start_time, end_time,
                                                                              label, message_event_id, finished)]

        return "\n\n".join(collective_events) + "\n\n" + \
               "\n\n".join("‼ " + formatted_date(key) + "\n\n" + "\n".join(value) for key, value in days.items())

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
