from supporting_functions import *


class FindClassHandlers(SupportingFunctions):
    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db, notification_db=notification_db)

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
                    trans_message = f"Класса с id {classroom_id} не существует!"
                    self.state_transition(user_id, States.S_FIND_CLASS, trans_message)

            else:
                trans_message = "Неверный формат записи\n\nОтправьте ссылку-приглашение или id класса в " \
                                "формате #id (например, #1223)"
                self.state_transition(user_id, States.S_FIND_CLASS, trans_message)

        elif payload["text"] == "Главное меню":
            self.trans_to_main_menu(user_id)

    def s_look_classroom_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_LOOK_CLASSROOM"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        keyboard_kwarg = self.get_look_keyboard_kwargs(user_id, classroom_id)

        if payload is None:
            self.state_transition(user_id, States.S_LOOK_CLASSROOM, "Для навигации используй кнопки!👇🏻",
                                  classroom_type=keyboard_kwarg)

        elif payload["text"] == "Участники":
            roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
            members_text = self.get_members_text(roles_dictionary)

            trans_message = f"Список участников:\n\n{members_text}"
            self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message,
                                  classroom_type=keyboard_kwarg)

        elif payload["text"] == "Войти":
            limit_members = self.classroom_db.get_classroom_members_limit(classroom_id)
            members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)

            if len(members_dictionary) < limit_members:
                default_role_id = self.role_db.get_default_role_id(classroom_id)
                self.classroom_db.insert_new_user_in_classroom(user_id, classroom_id, default_role_id)

                trans_message = "Ты вступил!"
                self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES, trans_message, sign=self.get_sign(user_id))
            else:
                trans_message = "В классе уже максимальное количество людей!"
                self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message, classroom_type=keyboard_kwarg)

        elif payload["text"] == "Подать заявку":
            request_information_list = self.classroom_db.get_list_of_request_information(classroom_id)

            if len(request_information_list) < 10:
                trans_message = "Напишите что-нибудь в заявке (макс. 50 символов)"
                self.state_transition(user_id, States.S_REQUEST_CLASSROOM, trans_message)
            else:
                trans_message = "Почта админа уже переполнена!"
                self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message, classroom_type=keyboard_kwarg)

        elif payload["text"] == "Редактировать заявку":
            request_information = self.classroom_db.get_request_information(user_id, classroom_id)

            trans_message = f"Твоя заявка:\n\n{request_information[3]}\n{request_information[2]}\n\n" \
                            "Напиши что-нибудь новое в заявке (макс. 50 символов)"
            self.state_transition(user_id, States.S_EDIT_REQUEST_CLASSROOM, trans_message)

        elif payload["text"] == "Главное меню":
            self.trans_to_main_menu(user_id)

    def s_request_classroom_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_REQUEST_CLASSROOM"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        keyboard_kwarg = self.get_look_keyboard_kwargs(user_id, classroom_id)

        if payload is None:
            if len(message) <= 50:
                self.classroom_db.insert_new_request(user_id, classroom_id, message)

                trans_message = "Заявка отправлена!"
                self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message, classroom_type=keyboard_kwarg)
            else:
                trans_message = "Длина текста превышает 50 символов! Напиши что-нибудь другое"
                self.state_transition(user_id, States.S_REQUEST_CLASSROOM, trans_message)

        elif payload["text"] == "Назад":
            classroom_name, school_name, access, description = \
                self.classroom_db.get_information_of_classroom(classroom_id)

            members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)
            members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

            trans_message = f"Ты осматриваешь класс {classroom_name}\n\n#{classroom_id}\n" \
                            f"Школа: {school_name}\n" \
                            f"Описание: {description}\n" \
                            f"Тип класса: {access}\n" \
                            f"Участники: {len(members_dictionary)}/{members_limit}"
            self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message, classroom_type=keyboard_kwarg)

        elif payload["text"] == "Главное меню":
            self.trans_to_main_menu(user_id)

    def s_edit_request_classroom_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_EDIT_REQUEST_CLASSROOM"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        keyboard_kwarg = self.get_look_keyboard_kwargs(user_id, classroom_id)

        if payload is None:
            if len(message) <= 50:
                self.classroom_db.update_request(user_id, classroom_id, message)

                trans_message = "Заявка обновлена!"
                self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message, classroom_type=keyboard_kwarg)
            else:
                trans_message = "Длина текста превышает 50 символов! Напиши что-нибудь другое"
                self.state_transition(user_id, States.S_EDIT_REQUEST_CLASSROOM, trans_message)

        elif payload["text"] == "Удалить заявку":
            self.classroom_db.delete_request(user_id, classroom_id)
            keyboard_kwarg = self.get_look_keyboard_kwargs(user_id, classroom_id)

            trans_message = "Заявка удалена!"
            self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message, classroom_type=keyboard_kwarg)

        elif payload["text"] == "Назад":
            classroom_name, school_name, access, description = \
                self.classroom_db.get_information_of_classroom(classroom_id)

            members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)
            members_limit = self.classroom_db.get_classroom_members_limit(classroom_id)

            trans_message = f"Ты осматриваешь класс {classroom_name}\n\n#{classroom_id}\n" \
                            f"Школа: {school_name}\n" \
                            f"Описание: {description}\n" \
                            f"Тип класса: {access}\n" \
                            f"Участники: {len(members_dictionary)}/{members_limit}"
            self.state_transition(user_id, States.S_LOOK_CLASSROOM, trans_message, classroom_type=keyboard_kwarg)

        elif payload["text"] == "Главное меню":
            self.trans_to_main_menu(user_id)
