from .classroom_settings_handlers import *
from .class_create_handlers import *
from .find_class_handlers import *
from .members_settings_handlers import *
from .my_classes_handlers import *
from .technical_support_handlers import *


class Handlers(ClassroomSettingsHandlers, ClassCreateHandlers, FindClassHandlers, MembersSettingsHandlers,
               MyClassesHandlers, TechnicalSupportHandlers):
    """Some atypical handlers"""

    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db)

    def s_nothing_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_NOTHING"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("menu"))

        elif payload["text"] == "Найти класс":
            self.send_message(user_id, "Отправьте ссылку-приглашение или id класса в "
                                       "формате #id (например, #1223)", self.get_keyboard("just_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_FIND_CLASS.value)

        elif payload["text"] == "Создать класс":
            classroom_id = self.classroom_db.insert_new_classroom()
            self.diary_homework_db.insert_classroom_id(classroom_id)

            self.classroom_db.update_user_customize_classroom_id(user_id, classroom_id)
            self.send_message(user_id, "Напишите название будущего класса (макс. 12 символов):",
                              self.get_keyboard("just_menu"))

            self.user_db.set_user_dialog_state(user_id, States.S_ENTER_CLASS_NAME_CLASSCREATE.value)

        elif payload["text"] == "Мои классы":
            user_classrooms_dictionary = self.classroom_db.get_user_classrooms_with_role_id(user_id)

            if not user_classrooms_dictionary:
                self.send_message(user_id, "Пока что ты не состоишь ни в одном классе!", self.get_keyboard("menu"))

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

                self.send_message(user_id, message="Список твоих классов:", template=dumps({
                    "type": "carousel",
                    "elements": elements
                }))

        elif payload["text"] == "Создать беседу класса":
            self.send_message(user_id, "Создаю беседу класса...",
                              self.get_keyboard("menu"))

        elif payload["text"] == "Настройка беседы класса":
            self.send_message(user_id, "Настройка беседы класса...",
                              self.get_keyboard("menu"))

        elif payload["text"] == "Обращение в тех. поддержку":
            self.send_message(user_id, "Опишите свой вопрос...",
                              self.get_keyboard("cancel_send"))
            self.user_db.set_user_dialog_state(user_id, States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE.value)

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

                self.send_message(user_id, f"Ты в классе {classroom_name}\n\n#{classroom_id}\n"
                                           f"Школа: {school_name}\n"
                                           f"Описание: {description}\n"
                                           f"Тип класса: {access}\n"
                                           f"Вы: {role_name}\n"
                                           f"Участники: {len(members_dictionary)}/{members_limit}",
                                  self.get_keyboard("my_class_menu"))
                self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES.value)

            elif payload["text"] == "look_at_the_classroom":
                access_keyboard_dict = {
                    "Публичный": "look_classroom_public",
                    "Заявки": "look_classroom_invite",
                    "Закрытый": "look_classroom_close"
                }

                self.send_message(user_id, f"Ты осматриваешь класс {classroom_name}\n\n#{classroom_id}\n"
                                           f"Школа: {school_name}\n"
                                           f"Описание: {description}\n"
                                           f"Тип класса: {access}\n"
                                           f"Участники: {len(members_dictionary)}/{members_limit}",
                                  self.get_keyboard(access_keyboard_dict[access]))
                self.user_db.set_user_dialog_state(user_id, States.S_LOOK_CLASSROOM.value)

    def p_enter_the_classroom_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with text: enter_the_classroom"""
        if current_dialog_state == States.S_NOTHING.value or current_dialog_state == States.S_FIND_CLASS.value:
            self.s_nothing_handler(user_id, payload)
        else:
            self.send_message(user_id, "Закончи текущее действие или выйди в главное меню")

    def p_edit_week_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payloads with text: standard | current | next"""
        if current_dialog_state == States.S_IN_CLASS_MYCLASSES.value:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            if classroom_id == payload["classroom_id"]:
                self.s_in_class_my_classes_handler(user_id, payload)
            else:
                self.send_message(user_id, "Это расписание не того класса, в котором ты находишься!")
        else:
            self.send_message(user_id, "Ты должен находиться в меню класса, расписание которого собираешься изменить!")

    def p_enter_members_settings_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with text: enter_member_settings"""
        if current_dialog_state == States.S_IN_CLASS_MYCLASSES.value:
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

            if classroom_id == payload["classroom_id"]:
                self.s_in_class_my_classes_handler(user_id, payload)
            else:
                self.send_message(user_id, "Это настройки участников не того класса, в котором ты находишься!")
        else:
            self.send_message(user_id, "Ты должен находиться в меню класса, в настройки участников которого собираешься"
                                       " войти!")

    def p_look_at_the_classroom_handler(self, user_id: int, payload: dict, current_dialog_state: int) -> None:
        """Handling payload with text: look_at_the_classroom"""
        if current_dialog_state in (States.S_FIND_CLASS.value, States.S_NOTHING.value):
            self.s_nothing_handler(user_id, payload)

        else:
            self.send_message(user_id, "Закончи текущее действие или выйди в главное меню")
