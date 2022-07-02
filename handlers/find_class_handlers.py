from supporting_functions import *
from states import States


class FindClassHandlers(SupportingFunctions):
    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db)

    def s_find_class_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_FIND_CLASS"""
        if payload is None:
            classroom_id = None
            stripped_message = message.strip()

            if fullmatch(r"#\d+", stripped_message):
                classroom_id = int(stripped_message[1:])

            elif search(r"onlyfiveEZHD/invite_link/\d+", stripped_message):
                result = search(r"onlyfiveEZHD/invite_link/\d+", stripped_message)
                classroom_id = int(stripped_message[result.start():result.end()].split("/")[-1])

            if classroom_id:
                existing_classroom_ids = self.classroom_db.get_list_of_classroom_ids()

                if classroom_id in existing_classroom_ids:
                    keyboard = VkKeyboard(inline=True)

                    classroom_name, school_name, access, description = \
                        self.classroom_db.get_information_of_classroom(classroom_id)
                    members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)
                    members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

                    for member_user_id in members_dictionary.keys():
                        if user_id == member_user_id:
                            keyboard.add_callback_button("Войти", payload={
                                "text": "enter_the_classroom", "classroom_id": classroom_id
                            })
                            user_in_classroom_text = "Вы состоите в этом классе ✅"
                            break
                    else:
                        keyboard.add_callback_button("Посмотреть", payload={
                            "text": "look_at_the_classroom", "classroom_id": classroom_id
                        })
                        user_in_classroom_text = "Вы не состоите в этом классе ❌"

                    self.send_message(user_id, f"#{classroom_id}\n"
                                               f"Класс: {classroom_name}\n"
                                               f"Школа: {school_name}\n"
                                               f"Описание: {description}\n"
                                               f"Тип класса: {access}\n"
                                               f"Участники: {len(members_dictionary)}/{members_limit}\n\n"
                                               f"{user_in_classroom_text}", keyboard.get_keyboard())
                else:
                    self.send_message(user_id, f"Класса с id {classroom_id} не существует!",
                                      self.get_keyboard("just_menu"))

            else:
                self.send_message(user_id, "Неверный формат записи\n\nОтправьте ссылку-приглашение или id класса в "
                                           "формате #id (например, #1223)", self.get_keyboard("just_menu"))

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)
