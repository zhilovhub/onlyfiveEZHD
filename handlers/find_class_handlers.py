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

    def s_look_classroom_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_LOOK_CLASSROOM"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        keyboard_type = self.get_keyboard_type(user_id, classroom_id)

        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻",
                              self.get_keyboard(keyboard_type))

        elif payload["text"] == "Участники":
            roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
            members_text = self.get_members_text(roles_dictionary)

            self.send_message(user_id, f"Список участников:\n\n{members_text}",
                              self.get_keyboard(keyboard_type))

        elif payload["text"] == "Войти":
            limit_members = self.classroom_db.get_classroom_members_limit(classroom_id)
            members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)

            if len(members_dictionary) < limit_members:
                default_role_id = self.role_db.get_default_role_id(classroom_id)
                self.classroom_db.insert_new_user_in_classroom(user_id, classroom_id, default_role_id)

                self.send_message(user_id, "Ты вступил!", self.get_keyboard("my_class_menu"))
                self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES.value)
            else:
                self.send_message(user_id, "В классе уже максимальное количество людей!",
                                  self.get_keyboard(keyboard_type))

        elif payload["text"] == "Подать заявку":
            self.send_message(user_id, "Напишите что-нибудь в заявке (макс. 50 символов)",
                              self.get_keyboard("back_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_REQUEST_CLASSROOM.value)

        elif payload["text"] == "Редактировать заявку":
            request_information = self.classroom_db.get_request_information(user_id, classroom_id)

            self.send_message(user_id,  f"Твоя заявка:\n\n{request_information[3]}\n{request_information[2]}\n\n"
                                        "Напиши что-нибудь новое в заявке (макс. 50 символов)",
                              self.get_keyboard("back_menu_delete_request"))
            self.user_db.set_user_dialog_state(user_id, States.S_EDIT_REQUEST_CLASSROOM.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_request_classroom_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_REQUEST_CLASSROOM"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

        if payload is None:
            if len(message) <= 50:
                self.classroom_db.insert_new_request(user_id, classroom_id, message)
                keyboard_type = self.get_keyboard_type(user_id, classroom_id)

                self.send_message(user_id, "Заявка отправлена!", self.get_keyboard(keyboard_type))
                self.user_db.set_user_dialog_state(user_id, States.S_LOOK_CLASSROOM.value)
            else:
                self.send_message(user_id, "Длина текста превышает 50 символов! Напиши что-нибудь другое",
                                  self.get_keyboard("back_menu"))

        elif payload["text"] == "Назад":
            keyboard_type = self.get_keyboard_type(user_id, classroom_id)

            classroom_name, school_name, access, description = \
                self.classroom_db.get_information_of_classroom(classroom_id)

            members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)
            members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

            self.send_message(user_id, f"Ты осматриваешь класс {classroom_name}\n\n#{classroom_id}\n"
                                       f"Школа: {school_name}\n"
                                       f"Описание: {description}\n"
                                       f"Тип класса: {access}\n"
                                       f"Участники: {len(members_dictionary)}/{members_limit}",
                              self.get_keyboard(keyboard_type))
            self.user_db.set_user_dialog_state(user_id, States.S_LOOK_CLASSROOM.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_edit_request_classroom_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_EDIT_REQUEST_CLASSROOM"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)

        if payload is None:
            if len(message) <= 50:

                self.classroom_db.update_request(user_id, classroom_id, message)
                keyboard_type = self.get_keyboard_type(user_id, classroom_id)

                self.send_message(user_id, "Заявка обновлена!", self.get_keyboard(keyboard_type))
                self.user_db.set_user_dialog_state(user_id, States.S_LOOK_CLASSROOM.value)
            else:
                self.send_message(user_id, "Длина текста превышает 50 символов! Напиши что-нибудь другое",
                                  self.get_keyboard("back_menu_delete_request"))

        elif payload["text"] == "Удалить заявку":
            self.classroom_db.delete_request(user_id, classroom_id)
            keyboard_type = self.get_keyboard_type(user_id, classroom_id)

            self.send_message(user_id, "Заявка удалена!", self.get_keyboard(keyboard_type))
            self.user_db.set_user_dialog_state(user_id, States.S_LOOK_CLASSROOM.value)

        elif payload["text"] == "Назад":
            keyboard_type = self.get_keyboard_type(user_id, classroom_id)

            classroom_name, school_name, access, description = \
                self.classroom_db.get_information_of_classroom(classroom_id)

            members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)
            members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

            self.send_message(user_id, f"Ты осматриваешь класс {classroom_name}\n\n#{classroom_id}\n"
                                       f"Школа: {school_name}\n"
                                       f"Описание: {description}\n"
                                       f"Тип класса: {access}\n"
                                       f"Участники: {len(members_dictionary)}/{members_limit}",
                              self.get_keyboard(keyboard_type))
            self.user_db.set_user_dialog_state(user_id, States.S_LOOK_CLASSROOM.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню...", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def get_keyboard_type(self, user_id: int, classroom_id: int) -> str:
        """Returns keyboard's type"""
        request_information = self.classroom_db.get_request_information(user_id, classroom_id)

        if request_information:
            return "look_classroom_request"
        else:
            access_keyboard_dict = {
                "Публичный": "look_classroom_public",
                "Заявки": "look_classroom_invite",
                "Закрытый": "look_classroom_close"
            }

            access = self.classroom_db.get_classroom_access(classroom_id)
            return access_keyboard_dict[access]
