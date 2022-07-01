from supporting_functions import *
from states import States


class MembersSettingsHandlers(SupportingFunctions):
    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db)

    def s_members_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MEMBERS_SETTINGS"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻", self.get_keyboard("members_settings"))

        elif payload["text"] == "Редактировать роли":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            self.send_message(user_id, f"{role_names_text}\n\nВведите номер роли для редактрования:",
                              self.get_keyboard("back_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Назначить роли":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            self.send_message(user_id, f"{role_names_text}\n\nВпишите номер роли, назначать которой хотите:",
                              self.get_keyboard("back_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_CHOOSE_ROLE_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Удалить участника":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
            members_text = self.get_members_text(roles_dictionary)

            self.send_message(user_id, f"{members_text}\n\nВпиши номер участника, которого ты хочешь удалить:",
                              self.get_keyboard("back_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_DELETE_MEMBER_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Удалить роли":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            if len(all_role_names) > 2:
                self.send_message(user_id, f"Все участники с ролью, которые вы удалите, возьмут дефолтную роль\n"
                                           f"Введите номер роли, которую хотите удалить:\n\n{role_names_text}",
                                  self.get_keyboard("back_menu"))
                self.user_db.set_user_dialog_state(user_id, States.S_DELETE_ROLE_MEMBERS_SETTINGS.value)
            else:
                self.send_message(user_id, f"В классе нет ролей, которые можно было бы удалить!\n\n{role_names_text}",
                                  self.get_keyboard("members_settings"))

        elif payload["text"] == "Добавить роли":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            if len(all_role_names) < 8:
                self.send_message(user_id, "Добавление ролей\n\nВ классе "
                                           "может быть максимум 8 ролей, но всегда есть минимум 2 (админ, участник)"
                                           ". Роль админа может иметь единственный участник класса, эта роль имеет все "
                                           "привилегии\n\nРоль участника получают те, кто только-только вошли в класс. "
                                           " По умолчанию эта роль также имеет все привилегии класса, кроме удаления "
                                           "класса и кикания участников\n\nРекомедуется начать настройки ролей с "
                                           "редактирования привилегий участников, ведь эту роль по умолчанию"
                                           " будут иметь все новенькие в классе\n\n"
                                           f"Текущие роли:\n{role_names_text}\n\nВпишите название новой роли (макс. "
                                           f"20 символов), она "
                                           f"возьмёт привилегии роли участника (привилегии новой роли можно "
                                           f"отредактировать):", self.get_keyboard("back_menu"))
                self.user_db.set_user_dialog_state(user_id, States.S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS.value)
            else:
                self.send_message(user_id, f"Вы этом классе уже максимальное кол-во ролей - 8!\n\n{role_names_text}",
                                  self.get_keyboard("members_settings"))

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в меню класса...", self.get_keyboard("my_class_menu"))
            self.user_db.set_user_dialog_state(user_id, States.S_IN_CLASS_MYCLASSES.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_add_role_enter_name_members_settings_handler(self, user_id: int, message: str,  payload: dict) -> None:
        """Handling States.S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS"""
        if payload is None:
            if len(message) <= 20:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                old_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)

                if message not in old_role_names:
                    self.role_db.insert_new_role(classroom_id, message.strip())
                    role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
                    role_names_text = "\n".join(
                        [f"{ind}. {role_name}" for ind, role_name in enumerate(role_names, start=1)])

                    self.send_message(user_id, f"Новая роль добавлена!\n\n{role_names_text}",
                                      self.get_keyboard("members_settings"))
                    self.user_db.set_user_dialog_state(user_id, States.S_MEMBERS_SETTINGS.value)
                else:
                    self.send_message(user_id, "Роль с таким названием уже существует в этом классе.\nВведите другое "
                                               "название:", self.get_keyboard("back_menu"))
            else:
                self.send_message(user_id, "Длина названия больше 20 символов. Введите другое название:",
                                  self.get_keyboard("back_menu"))

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в настройки участников...", self.get_keyboard("members_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_delete_role_members_settings_handler(self, user_id: int, message: str,  payload: dict) -> None:
        """Handling States.S_DELETE_ROLE_MEMBERS_SETTINGS"""
        if payload is None:
            ask_message = "Введите номер роли, удалить которую хотите:"

            if message.isdigit():
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                role_index = int(message)
                all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)

                if 0 < role_index <= len(all_role_names):
                    admin_role_name = self.role_db.get_admin_role_name(classroom_id)
                    default_role_name = self.role_db.get_default_role_name(classroom_id)
                    role_name = all_role_names[role_index - 1]

                    if role_name != admin_role_name and role_name != default_role_name:
                        default_role_id = self.role_db.get_default_role_id(classroom_id)
                        role_id = self.role_db.get_role_id_by_name(classroom_id, role_name)

                        self.role_db.update_all_roles(role_id, default_role_id)
                        self.role_db.delete_role(role_id)

                        self.send_message(user_id, "Роль удалена!", self.get_keyboard("members_settings"))
                        self.user_db.set_user_dialog_state(user_id, States.S_MEMBERS_SETTINGS.value)
                    else:
                        self.send_message(user_id, f"Нельзя удалить роль админа или дефолтную роль\n\n{ask_message}",
                                          self.get_keyboard("back_menu"))
                else:
                    self.send_message(user_id, "Номер роли не может быть отрицательным числом или быть больше текущего"
                                               f" количества ролей\n\n{ask_message}", self.get_keyboard("back_menu"))
            else:
                self.send_message(user_id, f"Введено не число\n\n{ask_message}",
                                  self.get_keyboard("back_menu"))

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в настройки участников...", self.get_keyboard("members_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_delete_member_members_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_DELETE_MEMBER_MEMBERS_SETTINGS"""
        if payload is None:
            ask_message = "Впиши номер участника, удалить которого хотите:"

            if message.isdigit():
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)
                member_index = int(message) - 1

                if 0 <= member_index < len(members_dictionary):
                    roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                    admin_role_id = self.role_db.get_admin_role_id(classroom_id)

                    ind = 0
                    for role_id, member_ids in roles_dictionary.items():
                        for member_id in member_ids:
                            if ind == member_index:
                                if role_id != admin_role_id and member_id != user_id:
                                    self.classroom_db.delete_student(classroom_id, member_id)
                                    new_roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                                    new_members_text = self.get_members_text(new_roles_dictionary)

                                    self.send_message(user_id,
                                                      f"{new_members_text}\n\nУчастник удалён!\n\n{ask_message}",
                                                      self.get_keyboard("back_menu"))
                                elif member_id == user_id:
                                    self.send_message(user_id, f"Ты пытаешься выгнать самого себя\n\n{ask_message}",
                                                      self.get_keyboard("back_menu"))
                                elif role_id == admin_role_id:
                                    self.send_message(user_id, f"Нельзя выгнать админа\n\n{ask_message}",
                                                      self.get_keyboard("back_menu"))
                                break
                            ind += 1
                        else:
                            continue
                        break

                else:
                    self.send_message(user_id, f"Число не может быть неположительным или быть больше количества "
                                               f"участников\n\n{ask_message}", self.get_keyboard("back_menu"))
            else:
                self.send_message(user_id, f"Введено не число\n\n{ask_message}",
                                  self.get_keyboard("back_menu"))

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в настройки участников...", self.get_keyboard("members_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_choose_role_members_settings_handler(self, user_id: int, message: str,  payload: dict) -> None:
        """Handling States.S_CHOOSE_ROLE_MEMBERS_SETTINGS"""
        if payload is None:
            ask_message = "Впишите номер роли, назначать которой хотите:"

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            if message.isdigit():
                role_index = int(message)

                if 0 < role_index <= len(all_role_names):
                    role_name = all_role_names[role_index - 1]
                    admin_role_id = self.role_db.get_admin_role_id(classroom_id)
                    role_id = self.role_db.get_role_id_by_name(classroom_id, role_name)

                    if role_id == admin_role_id:
                        self.send_message(user_id, "Вы уверены, что хотите назначить кого-то ролью админа? После "
                                                   "назначения вы перестанете быть админом и возьмёте дефолтную роль",
                                          self.get_keyboard("main_dangerous_zone_delete_one_classroom_settings"))
                        self.user_db.set_user_dialog_state(
                            user_id, States.S_CHOOSE_ADMIN_ROLE_CONFIRMATION_MEMBERS_SETTINGS.value)
                    else:
                        roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                        members_text = self.get_members_text(roles_dictionary)

                        self.send_message(user_id, f"{members_text}\n\nВпишите номер участника, которому хотите "
                                                   f"назначить роль - {role_name}", self.get_keyboard("back_menu"))
                        self.user_db.set_user_dialog_state(user_id,
                                                           States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS.value)
                    self.role_db.update_user_customize_role_id(user_id, role_id)
                else:
                    self.send_message(user_id, f"{all_role_names_text}\n\nНомер роли не может быть отрицательным числом"
                                               f" или быть больше текущего количества ролей\n\n{ask_message}",
                                      self.get_keyboard("back_menu"))
            else:
                self.send_message(user_id, f"{all_role_names_text}\n\nВведено не число\n\n{ask_message}",
                                  self.get_keyboard("back_menu"))

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в настройки участников...", self.get_keyboard("members_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_choose_admin_role_confirmation_members_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_CHOOSE_ADMIN_ROLE_CONFIRMATION_MEMBERS_SETTINGS"""
        if payload is None:
            self.send_message(user_id, "Для навигации используй кнопки!👇🏻",
                              self.get_keyboard("main_dangerous_zone_delete_one_classroom_settings"))

        elif payload["text"] == "Нет":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            self.send_message(user_id, f"{all_role_names_text}\n\nВпишите номер роли, назначать которой хотите:",
                              self.get_keyboard("back_menu"))
            self.role_db.update_user_customize_role_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_CHOOSE_ROLE_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Да":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
            members_text = self.get_members_text(roles_dictionary)

            self.send_message(user_id, f"{members_text}\n\nВпишите номер участника, которому хотите "
                                       f"назначить роль - {admin_role_name}", self.get_keyboard("back_menu"))
            self.user_db.set_user_dialog_state(user_id,
                                               States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS.value)

    def s_choose_member_change_role_members_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS"""
        if payload is None:
            new_role_id = self.role_db.get_customizing_role_id(user_id)
            role_name = self.role_db.get_role_name(new_role_id)
            ask_message = f"Впишите номер участника, которому хотите назначить роль - {role_name}"

            if message.isdigit():
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                members_dictionary = self.classroom_db.get_dict_of_classroom_users(classroom_id)
                member_index = int(message) - 1

                if 0 <= member_index < len(members_dictionary):
                    roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                    members_text = self.get_members_text(roles_dictionary)

                    ind = 0
                    for role_id, member_ids in roles_dictionary.items():
                        for member_id in member_ids:
                            if ind == member_index:
                                admin_role_id = self.role_db.get_admin_role_id(classroom_id)

                                if member_id != user_id and role_id != new_role_id:
                                    self.role_db.update_student_role(member_id, new_role_id)

                                    if admin_role_id == new_role_id:
                                        default_role_id = self.role_db.get_default_role_id(classroom_id)
                                        self.role_db.update_student_role(user_id, default_role_id)

                                    new_roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                                    new_members_text = self.get_members_text(new_roles_dictionary)

                                    if admin_role_id == new_role_id:
                                        self.send_message(user_id,
                                                          f"{new_members_text}\n\nНовая роль участнику назначена!\n\nВы"
                                                          f" больше не админ", self.get_keyboard("members_settings"))
                                        self.role_db.update_user_customize_role_id(user_id, "null")
                                        self.user_db.set_user_dialog_state(user_id, States.S_MEMBERS_SETTINGS.value)
                                    else:
                                        self.send_message(user_id,
                                                          f"{new_members_text}\n\nНовая роль участнику назначена!"
                                                          f"\n\n{ask_message}", self.get_keyboard("back_menu"))
                                elif member_id == user_id:
                                    self.send_message(user_id, f"{members_text}Ты не можешь переназначить самому себе "
                                                               f"роль\n\n{ask_message}", self.get_keyboard("back_menu"))
                                elif role_id == new_role_id:
                                    self.send_message(user_id, f"{members_text}\n\nУ этого участника уже эта роль!"
                                                               f"\n\n{ask_message}", self.get_keyboard("back_menu"))
                                break
                            ind += 1
                        else:
                            continue
                        break

                else:
                    self.send_message(user_id, f"Число не может быть неположительным или быть больше количества "
                                               f"участников\n\n{ask_message}", self.get_keyboard("back_menu"))
            else:
                self.send_message(user_id, f"Введено не число\n\n{ask_message}",
                                  self.get_keyboard("back_menu"))

        elif payload["text"] == "Назад":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            self.send_message(user_id, f"{all_role_names_text}\n\nВпишите номер роли, назначать которой хотите:",
                              self.get_keyboard("back_menu"))
            self.role_db.update_user_customize_role_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_CHOOSE_ROLE_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.role_db.update_user_customize_role_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)

    def s_choose_role_edit_role_members_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_EDIT_ROLE_MEMBERS_SETTINGS"""
        if payload is None:
            ask_message = "Впишите номер роли, редактировать которую хотите:"

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            if message.isdigit():
                role_index = int(message)

                if 0 < role_index <= len(all_role_names):
                    role_name = all_role_names[role_index - 1]
                    role_id = self.role_db.get_role_id_by_name(classroom_id, role_name)
                    self.role_db.update_user_customize_role_id(user_id, role_id)

                    self.send_message(user_id, f"Меню настроек роли - {role_name}")
                else:
                    self.send_message(user_id, f"{all_role_names_text}\n\nНомер роли не может быть отрицательным числом"
                                               f" или быть больше текущего количества ролей\n\n{ask_message}",
                                      self.get_keyboard("back_menu"))
            else:
                self.send_message(user_id, f"{all_role_names_text}\n\nВведено не число\n\n{ask_message}",
                                  self.get_keyboard("back_menu"))

        elif payload["text"] == "Назад":
            self.send_message(user_id, "Возвращаемся в настройки участников...", self.get_keyboard("members_settings"))
            self.user_db.set_user_dialog_state(user_id, States.S_MEMBERS_SETTINGS.value)

        elif payload["text"] == "Главное меню":
            self.send_message(user_id, "Возвращение в главное меню", self.get_keyboard("menu"))
            self.classroom_db.update_user_customize_classroom_id(user_id, "null")
            self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)
