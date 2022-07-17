from .classroom_settings_handlers import *
from .class_create_handlers import *
from .find_class_handlers import *
from .members_settings_handlers import *
from .my_classes_handlers import *
from .technical_support_handlers import *


class Handlers(ClassroomSettingsHandlers, ClassCreateHandlers, FindClassHandlers, MembersSettingsHandlers,
               MyClassesHandlers, TechnicalSupportHandlers):
    """Some atypical handlers"""

    def __init__(self, bot: Bot, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands) -> None:
        """Initialization"""
        super().__init__(bot=bot, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db, notification_db=notification_db)

    async def s_nothing_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_NOTHING"""
        if payload is None:
            await self.state_transition(user_id, States.S_NOTHING, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Найти класс":
            trans_message = "Отправьте ссылку-приглашение или id класса в формате #id (например, #1223)"
            await self.state_transition(user_id, States.S_FIND_CLASS, trans_message)

        elif payload["text"] == "Создать класс":
            classroom_id = self.classroom_db.insert_new_classroom()
            self.classroom_db.update_user_customize_classroom_id(user_id, classroom_id)

            trans_message = "Напишите название будущего класса (макс. 12 символов):"
            await self.state_transition(user_id, States.S_ENTER_CLASS_NAME_CLASSCREATE, trans_message)

        elif payload["text"] == "Мои классы":
            user_classrooms_dictionary = self.classroom_db.get_user_classrooms_with_role_id(user_id)

            if not user_classrooms_dictionary:
                trans_message = "Пока что ты не состоишь ни в одном классе!"
                await self.state_transition(user_id, States.S_NOTHING, trans_message)

            else:
                elements = []
                for classroom_id, role_id in user_classrooms_dictionary.items():
                    button = {
                        "action": {
                            "type": "callback",
                            "label": "Войти",
                            "payload": {
                                "text": "enter_the_classroom",
                                "classroom_id": classroom_id
                            }
                        }
                    }

                    members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)
                    classroom_name, school_name, access, description = \
                        self.classroom_db.get_information_of_classroom(classroom_id)
                    role_name = self.role_db.get_role_name(role_id)
                    members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

                    elements.append(
                        {
                            "title": classroom_name + "\n" + school_name,
                            "description": f"#{classroom_id}\n"
                                           f"Тип класса: {access}\n"
                                           f"Вы: {role_name}\n"
                                           f"Участники: {len(members_dictionary)}/{members_limit}",
                            "buttons": [button]
                        }
                    )

                await self.send_message(user_id, message="Список твоих классов:", template=dumps({
                    "type": "carousel",
                    "elements": elements
                }))

        elif payload["text"] == "Обращение в тех. поддержку":
            trans_message = "Опишите свой вопрос..."
            await self.state_transition(user_id, States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE, trans_message)

        elif payload["text"] in ("enter_the_classroom", "look_at_the_classroom"):
            classroom_id = payload["classroom_id"]
            classroom_name, school_name, access, description = \
                self.classroom_db.get_information_of_classroom(classroom_id)
            self.classroom_db.update_user_customize_classroom_id(user_id, classroom_id)

            members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)
            members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

            if payload["text"] == "enter_the_classroom":
                for key, value in members_dictionary.items():
                    if key == user_id:
                        role_id = value
                        break
                else:
                    role_id = None
                role_name = self.role_db.get_role_name(role_id)

                trans_message = f"Ты в классе {classroom_name}\n\n#{classroom_id}\n" \
                                f"Школа: {school_name}\n" \
                                f"Описание: {description}\n" \
                                f"Тип класса: {access}\n" \
                                f"Вы: {role_name}\n" \
                                f"Участники: {len(members_dictionary)}/{members_limit}"
                await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES, trans_message,
                                            sign=self.get_sign(user_id))

            elif payload["text"] == "look_at_the_classroom":
                keyboard_kwarg = self.get_look_keyboard_kwargs(user_id, classroom_id)

                trans_message = f"Ты осматриваешь класс {classroom_name}\n\n#{classroom_id}\n" \
                                f"Школа: {school_name}\n" \
                                f"Описание: {description}\n" \
                                f"Тип класса: {access}\n" \
                                f"Участники: {len(members_dictionary)}/{members_limit}"
                await self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message,
                                            classroom_type=keyboard_kwarg)

    async def p_enter_the_classroom_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with text: enter_the_classroom"""
        if current_dialog_state == States.S_NOTHING.value or current_dialog_state == States.S_FIND_CLASS.value:
            await self.s_nothing_handler(user_id, payload)
        else:
            await self.send_message(user_id, "Закончи текущее действие или выйди в главное меню")

    async def p_edit_week_or_homework_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with text: edit_current_homework | edit_next_homework + all week types"""
        if current_dialog_state in (States.S_IN_CLASS_MYCLASSES.value, States.S_IN_CLASS_MYCLASSES2.value):
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            if classroom_id == payload["classroom_id"]:
                await self.s_in_class_my_classes_handler(user_id, payload)
            else:
                await self.send_message(user_id, "Это расписание не того класса, в котором ты находишься!")
        else:
            await self.send_message(user_id,
                                    "Ты должен находиться в меню класса, расписание которого собираешься изменить!")

    async def p_enter_members_settings_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with text: enter_member_settings"""
        if current_dialog_state == States.S_IN_CLASS_MYCLASSES.value:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            if classroom_id == payload["classroom_id"]:
                await self.s_in_class_my_classes_handler(user_id, payload)
            else:
                await self.send_message(user_id, "Это настройки участников не того класса, в котором ты находишься!")
        else:
            await self.send_message(user_id,
                                    "Ты должен находиться в меню класса, в настройки участников которого собираешься"
                                    " войти!")

    async def p_look_at_the_classroom_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with text: look_at_the_classroom"""
        if current_dialog_state in (States.S_FIND_CLASS.value, States.S_NOTHING.value):
            await self.s_nothing_handler(user_id, payload)

        else:
            await self.send_message(user_id, "Закончи текущее действие или выйди в главное меню")

    async def p_accept_cancel_request_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        if current_dialog_state in (States.S_IN_CLASS_MYCLASSES.value, States.S_IN_CLASS_MYCLASSES2.value):
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            if classroom_id == payload["classroom_id"]:
                await self.s_in_class_my_classes_handler(user_id, payload)
            else:
                await self.send_message(user_id, "Это заявки не того класса, в котором ты находишься!")
        else:
            await self.send_message(user_id, "Ты должен находиться в меню класса, заявки которого рассматриваешь!")
