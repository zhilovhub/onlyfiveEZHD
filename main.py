from handlers import *

# only_five_cdz imports for heroku
from only_five_cdz import bot as bot_cdz
from only_five_cdz import handlers_class as handlers_class_cdz

# Creating database if not exists
# with connect(
#         host=HOST,
#         port=PORT,
#         user=USER,
#         password=PASSWORD
# ) as connection_to_create_db:
#     with connection_to_create_db.cursor() as cursor:
#         cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}""")

# Connection to the database
connection = connect(DATABASE_URL)
connection.autocommit = True

# Classes for working with database's tables
user_db = UserDataCommands(connection)
classroom_db = ClassroomCommands(connection)
technical_support_db = TechnicalSupportCommands(connection)
diary_homework_db = DiaryHomeworkCommands(connection)
role_db = RoleCommands(connection)
notification_db = NotificationCommands(connection)
event_db = EventCommands(connection)
admin_panel_db = AdminCommands(connection)

# All handlers + bot
bot = Bot(TOKEN)
handlers_class = Handlers(bot=bot,
                          user_db=user_db,
                          classroom_db=classroom_db,
                          technical_support_db=technical_support_db,
                          diary_homework_db=diary_homework_db,
                          role_db=role_db,
                          notification_db=notification_db,
                          event_db=event_db,
                          admin_panel_db=admin_panel_db
                          )


@bot.on.message()
async def listen_messages(message: Message) -> None:
    """Listening new messages"""
    user_id = message.from_id  # Getting user_id
    message_text = message.text.strip()  # Getting message's text
    attachments = message.attachments
    payload = message.get_payload_json()

    try:
        maintenance = admin_panel_db.get_maintenance()

        if not maintenance or user_db.check_user_is_admin(user_id):  # Not maintenance or user is admin
            user_information = await handlers_class.get_user_info(user_id)  # User_id, first_name, nickname

            user_db.insert_new_user(user_id,
                                    user_information["screen_name"],
                                    user_information["first_name"],
                                    user_information["last_name"],
                                    False
                                    )  # Will add a new user if user writes his first message
            classroom_db.insert_new_customizer(user_id)

            if await handlers_class.is_member(user_id):  # Checking first condition

                if user_db.check_user_is_ready(user_id):  # Checking second condition

                    if not attachments and message_text:  # Checking user didn't send attachment
                        current_dialog_state = user_db.get_user_dialog_state(user_id)
                        await filter_dialog_state(user_id, message_text, payload, current_dialog_state)
                    elif attachments:
                        await handlers_class.send_message(user_id,
                                                          "Пиши текстом... Или используй кнопки для навигации!👇🏻")
                    elif not message_text:
                        await handlers_class.send_message(user_id, "Пустой текст😐")
                else:
                    user_db.set_user_is_ready(
                        user_id)  # First condition is True but this is a first user's message

                    await handlers_class.state_transition(user_id, States.S_NOTHING, INTRODUCTION_MESSAGE)
            else:
                await handlers_class.send_message(user_id, "Перед использованием бота подпишись на группу!")
                # User not member
        else:
            await handlers_class.send_message(user_id, "Бот на тех обслуживании")

    except Exception as e:
        await handlers_class.send_message(user_id=user_id,
                                          message="Произошла какая-то ошибка, информация подана админу")
        await handlers_class.send_message(user_id=ADMIN_ID, message=str(e))
        raise e


@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def listen_message_events(event: GroupTypes.MessageEvent):
    """Listening message_events"""
    event_id = event.object.event_id
    user_id = event.object.user_id
    peer_id = event.object.peer_id
    payload = event.object.payload

    try:
        await handlers_class.send_message_event_answer(event_id, user_id, peer_id, "")

        maintenance = admin_panel_db.get_maintenance()

        if not maintenance or user_db.check_user_is_admin(user_id):
            if await handlers_class.is_member(user_id):
                current_dialog_state = user_db.get_user_dialog_state(user_id)
                await filter_callback_button_payload(user_id, payload, current_dialog_state)
            else:
                await handlers_class.send_message(user_id, "Перед использованием бота подпишись на группу!")
        else:
            await handlers_class.send_message(user_id, "Бот на тех обслуживании")
    except Exception as e:
        await handlers_class.send_message(user_id=user_id,
                                          message="Произошла какая-то ошибка, информация подана админу")
        await handlers_class.send_message(user_id=ADMIN_ID, message=str(e))


async def filter_dialog_state(user_id: int, message: str, payload: dict, current_dialog_state: int) -> None:
    """Filtering dialog states"""
    match current_dialog_state:
        case States.S_NOTHING.value:
            await handlers_class.s_nothing_handler(user_id, payload)

        # CLASSCREATE
        case States.S_ENTER_CLASS_NAME_CLASSCREATE.value:
            await handlers_class.s_enter_class_name_class_create_handler(user_id, message, payload)

        case States.S_ENTER_SCHOOL_NAME_CLASSCREATE.value:
            await handlers_class.s_enter_school_name_class_create_handler(user_id, message, payload)

        case States.S_ENTER_ACCESS_CLASSCREATE.value:
            await handlers_class.s_enter_access_class_create_handler(user_id, payload)

        case States.S_ENTER_DESCRIPTION_CLASSCREATE.value:
            await handlers_class.s_enter_description_class_create_handler(user_id, message, payload)

        case States.S_SUBMIT_CLASSCREATE.value:
            await handlers_class.s_submit_class_create_handler(user_id, payload)

        # MYCLASSES
        case States.S_IN_CLASS_MYCLASSES.value:
            await handlers_class.s_in_class_my_classes_handler(user_id, payload)

        case States.S_IN_CLASS_MYCLASSES2.value:
            await handlers_class.s_in_class_my_classes2_handler(user_id, payload)

        case States.S_EDIT_WEEK_MYCLASSES.value:
            await handlers_class.s_edit_week_my_classes_handler(user_id, payload)

        case States.S_EDIT_WEEKDAY_MYCLASSES.value:
            await handlers_class.s_edit_weekday_my_classes_handler(user_id, payload)

        case States.S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES.value:
            await handlers_class.s_add_new_lesson_weekday_my_classes_handler(user_id, message, payload)

        case States.S_EDIT_LESSON_WEEKDAY_MYCLASSES.value:
            await handlers_class.s_edit_lesson_weekday_my_classes_handler(user_id, message, payload)

        case States.S_EDIT_HOMEWORK_MYCLASSES.value:
            await handlers_class.s_edit_homework_my_classes_handler(user_id, payload)

        case States.S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES.value:
            await handlers_class.s_edit_homework_weekday_my_classes_handler(user_id, message, payload)

        # NOTIFICATIONS
        case States.S_CHOOSE_USER_FOR_NOTIFICATION_MYCLASSES.value:
            await handlers_class.s_choose_user_for_notification_handler_my_classes(user_id, message, payload)

        case States.S_ENTER_TEXT_FOR_NOTIFICATION_MYCLASSES.value:
            await handlers_class.s_enter_text_for_notification_handler_my_classes(user_id, message, payload)

        case States.S_ENTER_DATE_FOR_NOTIFICATION_MYCLASSES.value:
            await handlers_class.s_enter_date_for_notification_handler_my_classes(user_id, message, payload)

        case States.S_ACCEPT_CREATE_NOTIFICATION_MYCLASSES.value:
            await handlers_class.s_accept_create_notification_my_classes_handler(user_id, payload)

        # EVENTS
        case States.S_CHOOSE_EVENT_MYCLASSES.value:
            await handlers_class.s_choose_event_handler(user_id, payload)

        case States.S_CHOOSE_EVENT_TYPE_MYCLASSES.value:
            await handlers_class.s_choose_event_type_handler(user_id, payload)

        case States.S_ENTER_NOT_COLLECTIVE_EVENT_NAME_MYCLASSES.value:
            await handlers_class.s_enter_not_collective_event_name_handler(user_id, message, payload)

        case States.S_ENTER_NOT_COLLECTIVE_EVENT_START_TIME_MYCLASSES.value:
            await handlers_class.s_enter_not_collective_event_start_time_handler(user_id, message, payload)

        case States.S_ENTER_NOT_COLLECTIVE_EVENT_END_TIME_MYCLASSES.value:
            await handlers_class.s_enter_not_collective_event_end_time_handler(user_id, message, payload)

        case States.S_SUBMIT_EVENT_CREATE_MYCLASSES.value:
            await handlers_class.s_submit_event_create_handler(user_id, payload)

        case States.S_ENTER_COLLECTIVE_EVENT_NAME_MYCLASSES.value:
            await handlers_class.s_enter_collective_event_name_handler(user_id, message, payload)

        case States.S_ENTER_COLLECTIVE_EVENT_START_TIME_MYCLASSES.value:
            await handlers_class.s_enter_collective_event_start_time_handler(user_id, message, payload)

        case States.S_ENTER_COLLECTIVE_EVENT_END_TIME_MYCLASSES.value:
            await handlers_class.s_enter_collective_event_end_time_handler(user_id, message, payload)

        case States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_COUNT_MYCLASSES.value:
            await handlers_class.s_enter_collective_event_required_count_handler(user_id, message, payload)

        case States.S_ENTER_COLLECTIVE_EVENT_REQUIRED_STUDENT_MYCLASSES.value:
            await handlers_class.s_enter_collective_event_required_student_handler(user_id, message, payload)

        case States.S_EDIT_EVENT_MYCLASSES.value:
            await handlers_class.s_edit_event_handler(user_id, payload)

        case States.S_ADD_COUNT_COLLECTIVE_EVENT_MYCLASSES.value:
            await handlers_class.s_add_count_collective_event_handler(user_id, message, payload)

        case States.S_DECREASE_COUNT_COLLECTIVE_EVENT_MYCLASSES.value:
            await handlers_class.s_decrease_count_collective_event_handler(user_id, message, payload)

        case States.S_EVENT_SETTINGS_MYCLASSES.value:
            await handlers_class.s_event_settings_handler(user_id, payload)

        case States.S_ENTER_NEW_EVENT_NAME_MYCLASSES.value:
            await handlers_class.s_enter_new_event_name_handler(user_id, message, payload)

        case States.S_ENTER_NEW_EVENT_REQUIRED_COUNT.value:
            await handlers_class.s_enter_new_event_required_count_handler(user_id, message, payload)

        case States.S_ENTER_NEW_EVENT_REQUIRED_STUDENTS_COUNT.value:
            await handlers_class.s_enter_new_event_required_students_count_handler(user_id, message, payload)

        case States.S_ENTER_NEW_EVENT_START_TIME.value:
            await handlers_class.s_enter_new_event_start_time_handler(user_id, message, payload)

        case States.S_ENTER_NEW_EVENT_END_TIME.value:
            await handlers_class.s_enter_new_event_end_time_handler(user_id, message, payload)

        # FINDCLASS
        case States.S_FIND_CLASS.value:
            await handlers_class.s_find_class_handler(user_id, message, payload)

        case States.S_LOOK_CLASSROOM.value:
            await handlers_class.s_look_classroom_handler(user_id, payload)

        case States.S_REQUEST_CLASSROOM.value:
            await handlers_class.s_request_classroom_handler(user_id, message, payload)

        case States.S_EDIT_REQUEST_CLASSROOM.value:
            await handlers_class.s_edit_request_classroom_handler(user_id, message, payload)

        # CLASSROOMSETTINGS
        case States.S_CLASSROOM_SETTINGS.value:
            await handlers_class.s_classroom_settings_handler(user_id, payload)

        case States.S_MAIN_CLASSROOM_SETTINGS.value:
            await handlers_class.s_main_classroom_settings_handler(user_id, payload)

        case States.S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS.value:
            await handlers_class.s_main_dangerous_zone_classroom_settings_handler(user_id, payload)

        case States.S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS.value:
            await handlers_class.s_main_dangerous_zone_delete_one_classroom_settings_handler(user_id, payload)

        case States.S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS.value:
            await handlers_class.s_main_dangerous_zone_delete_two_classroom_settings_handler(user_id, payload)

        case States.S_ACCESS_MAIN_CLASSROOM_SETTINGS.value:
            await handlers_class.s_access_main_classroom_settings_handler(user_id, payload)

        case States.S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS.value:
            await handlers_class.s_classroom_name_main_classroom_settings_handler(user_id, message, payload)

        case States.S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS.value:
            await handlers_class.s_school_name_main_classroom_settings_handler(user_id, message, payload)

        case States.S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS.value:
            await handlers_class.s_description_main_classroom_settings_handler(user_id, message, payload)

        case States.S_LIMIT_MAIN_CLASSROOM_SETTINGS.value:
            await handlers_class.s_limit_main_classroom_settings_handler(user_id, message, payload)

        case States.S_NOTIFICATION_SETTINGS_CLASSROOM_SETTINGS.value:
            await handlers_class.s_notification_settings_classroom_settings_handler(user_id, payload)

        # TECHNICALSUPPORT
        case States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE.value:
            await handlers_class.s_enter_technical_support_message_handler(user_id, message, payload)

        # MEMBERSSETTINGS
        case States.S_MEMBERS_SETTINGS.value:
            await handlers_class.s_members_settings_handler(user_id, payload)

        case States.S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS.value:
            await handlers_class.s_add_role_enter_name_members_settings_handler(user_id, message, payload)

        case States.S_DELETE_ROLE_MEMBERS_SETTINGS.value:
            await handlers_class.s_delete_role_members_settings_handler(user_id, message, payload)

        case States.S_DELETE_MEMBER_MEMBERS_SETTINGS.value:
            await handlers_class.s_delete_member_members_settings_handler(user_id, message, payload)

        case States.S_CHOOSE_ROLE_MEMBERS_SETTINGS.value:
            await handlers_class.s_choose_role_members_settings_handler(user_id, message, payload)

        case States.S_CHOOSE_ADMIN_ROLE_CONFIRMATION_MEMBERS_SETTINGS.value:
            await handlers_class.s_choose_admin_role_confirmation_members_settings_handler(user_id, payload)

        case States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS.value:
            await handlers_class.s_choose_member_change_role_members_settings_handler(user_id, message, payload)

        case States.S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS.value:
            await handlers_class.s_choose_role_edit_role_members_settings_handler(user_id, message, payload)

        case States.S_EDIT_ROLE_MEMBERS_SETTINGS.value:
            await handlers_class.s_edit_role_members_settings_handler(user_id, payload)

        case States.S_ENTER_NAME_EDIT_ROLE_MEMBERS_SETTINGS.value:
            await handlers_class.s_enter_name_edit_role_members_settings_handler(user_id, message, payload)

        case States.S_DIARY_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS.value:
            await handlers_class.s_diary_privilege_edit_role_members_settings_handler(user_id, payload)

        case States.S_MEMBERS_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS.value:
            await handlers_class.s_members_privilege_edit_role_members_settings(user_id, payload)

        case States.S_CLASSROOM_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS.value:
            await handlers_class.s_classroom_privilege_edit_role_members_settings(user_id, payload)


async def filter_callback_button_payload(user_id: int, payload: dict, current_dialog_state: int) -> None:
    """Filtering payload types"""
    match payload["text"]:
        case "enter_the_classroom":
            await handlers_class.p_enter_the_classroom_handler(user_id, payload, current_dialog_state)

        case ("edit_standard" | "edit_current" | "edit_next" | "edit_current_homework" | "edit_next_homework"):
            await handlers_class.p_edit_week_or_homework_handler(user_id, payload, current_dialog_state)

        case "enter_members_settings":
            await handlers_class.p_enter_members_settings_handler(user_id, payload, current_dialog_state)

        case "look_at_the_classroom":
            await handlers_class.p_look_at_the_classroom_handler(user_id, payload, current_dialog_state)

        case ("accept_request" | "cancel_request" | "event_settings"):
            await handlers_class.p_accept_cancel_request_handler(user_id, payload, current_dialog_state)


async def aioscheduler_tasks() -> None:
    aioschedule.every().monday.at("0:00").do(diary_homework_db.update_change_current_and_next_diary)
    aioschedule.every(10).seconds.do(handlers_class.check_events_started)
    aioschedule.every(10).seconds.do(handlers_class.check_events_finished)
    aioschedule.every(10).seconds.do(handlers_class.delete_finished_events)
    aioschedule.every(10).seconds.do(handlers_class.check_notifications)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.5)


async def create_tasks() -> None:
    """Creates tasks for asyncio-loop"""
    tasks = [
        bot.run_polling(),
        aioscheduler_tasks(),

        # for heroku
        handlers_class_cdz.set_auth_data(),
        bot_cdz.run_polling(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(create_tasks())
