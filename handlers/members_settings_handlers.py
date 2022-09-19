from supporting_functions import *


class MembersSettingsHandlers(SupportingFunctions):
    def __init__(self, bot: Bot, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands, event_db: EventCommands, admin_panel_db: AdminCommands) -> None:
        """Initialization"""
        super().__init__(bot=bot, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db, notification_db=notification_db, event_db=event_db,
                         admin_panel_db=admin_panel_db)

    async def s_members_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MEMBERS_SETTINGS"""
        if payload is None:
            await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Редактировать роли":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            trans_message = f"{role_names_text}\n\nВведите номер роли для редактрования:"
            await self.state_transition(user_id, States.S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назначить роли":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            trans_message = f"{role_names_text}\n\nВпишите номер роли, назначать которой хотите:"
            await self.state_transition(user_id, States.S_CHOOSE_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Удалить участника":
            if payload["can"]:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                members_text = self.get_members_text(roles_dictionary)

                trans_message = f"{members_text}\n\nВпиши номер участника, которого ты хочешь удалить:"
                await self.state_transition(user_id, States.S_DELETE_MEMBER_MEMBERS_SETTINGS, trans_message)
            else:
                await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, "Ты не можешь кикать участников из-за "
                                                                                "своей роли")

        elif payload["text"] == "Пригл. ссылка":
            if payload["can"]:
                classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
                invite_code = self.classroom_db.get_classroom_invite_code(classroom_id)

                trans_message = f"Ссылка-приглашение твоего класса👇🏻\n\n" \
                                f"[club{GROUP_ID}|onlyfiveEZHD/invite_link/{invite_code}]"
                await self.state_transition(user_id, States.S_MEMBERS_SETTINGS,
                                            trans_message, sign=self.get_sign(user_id))
            else:
                await self.state_transition(user_id, States.S_MEMBERS_SETTINGS,
                                            "Ты не можешь приглашать участников из-за "
                                            "своей роли")

        elif payload["text"] == "Удалить роли":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            if len(all_role_names) > 2:
                trans_message = f"Все участники с ролью, которые вы удалите, возьмут дефолтную роль\n" \
                                f"Введите номер роли, которую хотите удалить:\n\n{role_names_text}"
                await self.state_transition(user_id, States.S_DELETE_ROLE_MEMBERS_SETTINGS, trans_message)
            else:
                trans_message = f"В классе нет ролей, которые можно было бы удалить!\n\n{role_names_text}"
                await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Добавить роли":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            if len(all_role_names) < 8:
                trans_message = "Добавление ролей\n\nВ классе " \
                                "может быть максимум 8 ролей, но всегда есть минимум 2 (админ, участник)" \
                                ". Роль админа может иметь единственный участник класса, эта роль имеет все " \
                                "привилегии\n\nРоль участника получают те, кто только-только вошли в класс. " \
                                " По умолчанию эта роль также имеет все привилегии класса, кроме удаления " \
                                "класса и кикания участников\n\nРекомедуется начать настройки ролей с " \
                                "редактирования привилегий участников, ведь эту роль по умолчанию" \
                                " будут иметь все новенькие в классе\n\n" \
                                f"Текущие роли:\n{role_names_text}\n\nВпишите название новой роли (макс. " \
                                f"20 символов), она " \
                                f"возьмёт привилегии роли участника (привилегии новой роли можно " \
                                f"отредактировать):"
                await self.state_transition(user_id, States.S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS, trans_message)
            else:
                trans_message = f"Вы этом классе уже максимальное кол-во ролей - 8!\n\n{role_names_text}"
                await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Возвращаемся в меню класса..."
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES, trans_message,
                                        sign=self.get_sign(user_id))

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_add_role_enter_name_members_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
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

                    trans_message = f"Новая роль добавлена!\n\n{role_names_text}"
                    await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)
                else:
                    trans_message = "Роль с таким названием уже существует в этом классе.\nВведите другое название:"
                    await self.state_transition(user_id, States.S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS, trans_message)
            else:
                trans_message = "Длина названия больше 20 символов. Введите другое название:"
                await self.state_transition(user_id, States.S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Возвращаемся в настройки участников..."
            await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_delete_role_members_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
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

                        trans_message = "Роль удалена!"
                        await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)
                    else:
                        trans_message = f"Нельзя удалить роль админа или дефолтную роль\n\n{ask_message}"
                        await self.state_transition(user_id, States.S_DELETE_ROLE_MEMBERS_SETTINGS, trans_message)
                else:
                    trans_message = "Номер роли не может быть отрицательным числом или быть больше текущего" \
                                    f" количества ролей\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_DELETE_ROLE_MEMBERS_SETTINGS, trans_message)
            else:
                trans_message = f"Введено не число\n\n{ask_message}"
                await self.state_transition(user_id, States.S_DELETE_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Возвращаемся в настройки участников..."
            await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_delete_member_members_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
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
                    trans_message = "Что-то пошло не так"
                    for role_id, member_ids in roles_dictionary.items():
                        for member_id in member_ids:
                            if ind == member_index:
                                if role_id != admin_role_id and member_id != user_id:
                                    self.classroom_db.delete_student(classroom_id, member_id)
                                    new_roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                                    new_members_text = self.get_members_text(new_roles_dictionary)

                                    await self.notify_to_kicked_classmate(member_id, classroom_id)
                                    await self.notify_leave_classmate(member_id, classroom_id, kicked=True,
                                                                      without_user_ids=[user_id])

                                    trans_message = f"{new_members_text}\n\nУчастник удалён!\n\n{ask_message}"
                                elif member_id == user_id:
                                    trans_message = f"Ты пытаешься выгнать самого себя\n\n{ask_message}"
                                elif role_id == admin_role_id:
                                    trans_message = f"Нельзя выгнать админа\n\n{ask_message}"
                                break
                            ind += 1
                        else:
                            continue
                        await self.state_transition(user_id, States.S_DELETE_MEMBER_MEMBERS_SETTINGS, trans_message)
                        break

                else:
                    trans_message = f"Число не может быть неположительным или быть больше количества " \
                                    f"участников\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_DELETE_MEMBER_MEMBERS_SETTINGS, trans_message)
            else:
                trans_message = f"Введено не число\n\n{ask_message}"
                await self.state_transition(user_id, States.S_DELETE_MEMBER_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Возвращаемся в настройки участников..."
            await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_choose_role_members_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
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
                        trans_message = "Вы уверены, что хотите назначить кого-то ролью админа? После " \
                                        "назначения вы перестанете быть админом и возьмёте дефолтную роль"
                        await self.state_transition(user_id, States.S_CHOOSE_ADMIN_ROLE_CONFIRMATION_MEMBERS_SETTINGS,
                                                    trans_message)
                    else:
                        roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                        members_text = self.get_members_text(roles_dictionary)

                        trans_message = f"{members_text}\n\nВпишите номер участника, которому хотите " \
                                        f"назначить роль - {role_name}"
                        await self.state_transition(user_id, States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS,
                                                    trans_message)
                    self.role_db.update_user_customize_role_id(user_id, role_id)
                else:
                    trans_message = f"{all_role_names_text}\n\nНомер роли не может быть отрицательным числом" \
                                    f" или быть больше текущего количества ролей\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_CHOOSE_ROLE_MEMBERS_SETTINGS, trans_message)
            else:
                trans_message = f"{all_role_names_text}\n\nВведено не число\n\n{ask_message}"
                await self.state_transition(user_id, States.S_CHOOSE_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Возвращаемся в настройки участников..."
            await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_choose_admin_role_confirmation_members_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_CHOOSE_ADMIN_ROLE_CONFIRMATION_MEMBERS_SETTINGS"""
        if payload is None:
            await self.state_transition(user_id, States.S_CHOOSE_ADMIN_ROLE_CONFIRMATION_MEMBERS_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Нет":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)

            self.role_db.update_user_customize_role_id(user_id, None)

            trans_message = f"{all_role_names_text}\n\nВпишите номер роли, назначать которой хотите:"
            await self.state_transition(user_id, States.S_CHOOSE_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Да":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
            members_text = self.get_members_text(roles_dictionary)

            trans_message = f"{members_text}\n\nВпишите номер участника, которому хотите " \
                            f"назначить роль - {admin_role_name}"
            await self.state_transition(user_id, States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_choose_member_change_role_members_settings_handler(self, user_id: int, message: str, payload: dict
                                                                   ) -> None:
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
                                    member_student_id = self.classroom_db.get_student_id(member_id, classroom_id)
                                    self.role_db.update_student_role(member_student_id, new_role_id)

                                    if admin_role_id == new_role_id:
                                        default_role_id = self.role_db.get_default_role_id(classroom_id)
                                        student_id = self.classroom_db.get_student_id(user_id, classroom_id)
                                        self.role_db.update_student_role(student_id, default_role_id)

                                    new_roles_dictionary = self.classroom_db.get_dict_of_classroom_roles(classroom_id)
                                    new_members_text = self.get_members_text(new_roles_dictionary)

                                    if admin_role_id == new_role_id:
                                        self.role_db.update_user_customize_role_id(user_id, None)

                                        trans_message = f"{new_members_text}\n\nНовая роль участнику назначена!\n\nВы" \
                                                        f" больше не админ"
                                        await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)
                                    else:
                                        trans_message = f"{new_members_text}\n\nНовая роль участнику назначена!" \
                                                        f"\n\n{ask_message}"
                                        await self.state_transition(user_id,
                                                                    States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS,
                                                                    trans_message)
                                elif member_id == user_id:
                                    trans_message = f"{members_text}Ты не можешь переназначить самому себе " \
                                                    f"роль\n\n{ask_message}"
                                    await self.state_transition(user_id,
                                                                States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS,
                                                                trans_message)
                                elif role_id == new_role_id:
                                    trans_message = f"{members_text}\n\nУ этого участника уже эта роль!\n\n" \
                                                    f"{ask_message}"
                                    await self.state_transition(user_id,
                                                                States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS,
                                                                trans_message)
                                break
                            ind += 1
                        else:
                            continue
                        break

                else:
                    trans_message = f"Число не может быть неположительным или быть больше количества " \
                                    f"участников\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS,
                                                trans_message)
            else:
                trans_message = f"Введено не число\n\n{ask_message}"
                await self.state_transition(user_id, States.S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)
            self.role_db.update_user_customize_role_id(user_id, None)

            trans_message = f"{all_role_names_text}\n\nВпишите номер роли, назначать которой хотите:"
            await self.state_transition(user_id, States.S_CHOOSE_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_choose_role_edit_role_members_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS"""
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

                    role_properties_dict = self.role_db.get_role_properties_dict(role_id)
                    role_properties_text = self.get_role_properties_text(role_properties_dict)

                    await self.state_transition(user_id, States.S_EDIT_ROLE_MEMBERS_SETTINGS, role_properties_text)
                else:
                    trans_message = f"{all_role_names_text}\n\nНомер роли не может быть отрицательным числом" \
                                    f" или быть больше текущего количества ролей\n\n{ask_message}"
                    await self.state_transition(user_id, States.S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS, trans_message)
            else:
                trans_message = f"{all_role_names_text}\n\nВведено не число\n\n{ask_message}"
                await self.state_transition(user_id, States.S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            trans_message = "Возвращаемся в настройки участников..."
            await self.state_transition(user_id, States.S_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_edit_role_members_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_EDIT_ROLE_MEMBERS_SETTINGS"""
        if payload is None:
            await self.state_transition(user_id, States.S_EDIT_ROLE_MEMBERS_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻")

        elif payload["text"] == "Класс":
            role_id = self.role_db.get_customizing_role_id(user_id)
            classroom_role_properties_dictionary = self.role_db.get_classroom_role_properties_dict(role_id)
            color_values = self.get_edit_role_keyboard_color_values(classroom_role_properties_dictionary)

            trans_message = "Что участник с этой ролью может делать с классом:"
            await self.state_transition(user_id, States.S_CLASSROOM_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS, trans_message,
                                        *color_values)

        elif payload["text"] == "Участники":
            role_id = self.role_db.get_customizing_role_id(user_id)
            members_role_properties_dictionary = self.role_db.get_members_role_properties_dict(role_id)
            color_values = self.get_edit_role_keyboard_color_values(members_role_properties_dictionary)

            trans_message = "Что участник с этой ролью может делать с другими учатниками:"
            await self.state_transition(user_id, States.S_MEMBERS_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS, trans_message,
                                        *color_values)

        elif payload["text"] == "Дневник":
            role_id = self.role_db.get_customizing_role_id(user_id)
            diary_role_properties_dictionary = self.role_db.get_diary_role_properties_dict(role_id)
            color_values = self.get_edit_role_keyboard_color_values(diary_role_properties_dictionary)

            trans_message = "Что участник с этой ролью может делать с дневником:"
            await self.state_transition(user_id, States.S_DIARY_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS, trans_message,
                                        *color_values)

        elif payload["text"] == "Сменить имя":
            trans_message = "Введите новое имя роли (макс. 20 символов):"
            await self.state_transition(user_id, States.S_ENTER_NAME_EDIT_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            ask_message = "Впишите номер роли, редактировать которую хотите:"

            classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
            all_role_names = self.role_db.get_all_role_names_from_classroom(classroom_id)
            admin_role_name = self.role_db.get_admin_role_name(classroom_id)
            default_role_name = self.role_db.get_default_role_name(classroom_id)
            all_role_names_text = self.get_all_role_names_text(all_role_names, admin_role_name, default_role_name)
            self.role_db.update_user_customize_role_id(user_id, None)

            trans_message = f"{all_role_names_text}\n\n{ask_message}"
            await self.state_transition(user_id, States.S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_enter_name_edit_role_members_settings_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_NAME_EDIT_ROLE_MEMBERS_SETTINGS"""
        if payload is None:
            if len(message) <= 20:
                role_id = self.role_db.get_customizing_role_id(user_id)
                self.role_db.update_role_name(role_id, message)

                role_properties_dict = self.role_db.get_role_properties_dict(role_id)
                role_properties_text = self.get_role_properties_text(role_properties_dict)

                trans_message = f"{role_properties_text}\n\nНазвание роли изменено!"
                await self.state_transition(user_id, States.S_EDIT_ROLE_MEMBERS_SETTINGS, trans_message)
            else:
                trans_message = "Длина нового названия превышает 20 символов\n\n" \
                                "Введите другое новое имя роли (макс. 20 символов):"
                await self.state_transition(user_id, States.S_ENTER_NAME_EDIT_ROLE_MEMBERS_SETTINGS, trans_message)

        elif payload["text"] == "Назад":
            role_id = self.role_db.get_customizing_role_id(user_id)
            role_properties_dict = self.role_db.get_role_properties_dict(role_id)
            role_properties_text = self.get_role_properties_text(role_properties_dict)

            await self.state_transition(user_id, States.S_EDIT_ROLE_MEMBERS_SETTINGS, role_properties_text)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_diary_privilege_edit_role_members_settings_handler(self, user_id: int, payload: dict) -> None:
        """Handling States.S_DIARY_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS"""
        if payload is None:
            role_id = self.role_db.get_customizing_role_id(user_id)
            diary_role_properties_dictionary = self.role_db.get_diary_role_properties_dict(role_id)
            color_values = self.get_edit_role_keyboard_color_values(diary_role_properties_dictionary)

            await self.state_transition(user_id, States.S_DIARY_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻", *color_values)

        elif payload["text"] in ["Текущее дз", "Будущее дз",
                                 "Эталонное расписание", "Текущее расписание", "Будущее расписание"]:
            payload_meaning_dictionary = {
                "Текущее дз": "change_current_homework",
                "Будущее дз": "change_next_homework",
                "Эталонное расписание": "change_standard_week",
                "Текущее расписание": "change_current_week",
                "Будущее расписание": "change_next_week",
            }
            privilege_type = payload_meaning_dictionary[payload["text"]]

            role_id = self.role_db.get_customizing_role_id(user_id)
            diary_role_properties_dictionary = self.role_db.get_diary_role_properties_dict(role_id)
            new_value = False if diary_role_properties_dictionary[privilege_type] else True

            self.role_db.update_role_privilege(role_id, new_value, privilege_type)
            diary_role_properties_dictionary[privilege_type] = new_value

            diary_role_properties_text = self.get_role_properties_text(diary_role_properties_dictionary, "diary")
            color_values = self.get_edit_role_keyboard_color_values(diary_role_properties_dictionary)

            await self.state_transition(user_id, States.S_DIARY_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS,
                                        diary_role_properties_text, *color_values)

        elif payload["text"] == "Назад":
            role_id = self.role_db.get_customizing_role_id(user_id)
            role_properties_dict = self.role_db.get_role_properties_dict(role_id)
            role_properties_text = self.get_role_properties_text(role_properties_dict)

            await self.state_transition(user_id, States.S_EDIT_ROLE_MEMBERS_SETTINGS, role_properties_text)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_members_privilege_edit_role_members_settings(self, user_id: int, payload: dict) -> None:
        """Handling States.S_MEMBERS_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS"""
        if payload is None:
            role_id = self.role_db.get_customizing_role_id(user_id)
            members_role_properties_dictionary = self.role_db.get_members_role_properties_dict(role_id)
            color_values = self.get_edit_role_keyboard_color_values(members_role_properties_dictionary)

            await self.state_transition(user_id, States.S_MEMBERS_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻", *color_values)

        elif payload["text"] in ["Кикание участников", "Приглашение в класс",
                                 "Принятие заявок", "Уведомление участников", "Редактирование событий"]:
            payload_meaning_dictionary = {
                "Кикание участников": "kick_members",
                "Приглашение в класс": "invite_members",
                "Принятие заявок": "accept_requests",
                "Уведомление участников": "notify",
                "Редактирование событий": "redact_events"
            }
            privilege_type = payload_meaning_dictionary[payload["text"]]

            role_id = self.role_db.get_customizing_role_id(user_id)
            members_role_properties_dictionary = self.role_db.get_members_role_properties_dict(role_id)
            new_value = False if members_role_properties_dictionary[privilege_type] else True

            self.role_db.update_role_privilege(role_id, new_value, privilege_type)
            members_role_properties_dictionary[privilege_type] = new_value

            role_properties_dict = self.role_db.get_role_properties_dict(role_id)
            role_properties_text = self.get_role_properties_text(role_properties_dict)
            color_values = self.get_edit_role_keyboard_color_values(members_role_properties_dictionary)

            await self.state_transition(user_id, States.S_MEMBERS_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS,
                                        role_properties_text, *color_values)

        elif payload["text"] == "Назад":
            role_id = self.role_db.get_customizing_role_id(user_id)
            role_properties_dict = self.role_db.get_role_properties_dict(role_id)
            role_properties_text = self.get_role_properties_text(role_properties_dict)

            await self.state_transition(user_id, States.S_EDIT_ROLE_MEMBERS_SETTINGS, role_properties_text)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    async def s_classroom_privilege_edit_role_members_settings(self, user_id: int, payload: dict) -> None:
        """Handling States.S_CLASSROOM_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS"""
        if payload is None:
            role_id = self.role_db.get_customizing_role_id(user_id)
            classroom_role_properties_dictionary = self.role_db.get_classroom_role_properties_dict(role_id)
            color_values = self.get_edit_role_keyboard_color_values(classroom_role_properties_dictionary)

            await self.state_transition(user_id, States.S_CLASSROOM_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS,
                                        "Для навигации используй кнопки!👇🏻", *color_values)

        elif payload["text"] in ["Название класса", "Название школы", "Тип класса",
                                 "Описание класса", "Лимит участников"]:
            payload_meaning_dictionary = {
                "Название класса": "change_classroom_name",
                "Название школы": "change_school_name",
                "Тип класса": "change_classroom_access",
                "Описание класса": "change_description",
                "Лимит участников": "change_members_limit"
            }
            privilege_type = payload_meaning_dictionary[payload["text"]]

            role_id = self.role_db.get_customizing_role_id(user_id)
            classroom_role_properties_dictionary = self.role_db.get_classroom_role_properties_dict(role_id)
            new_value = False if classroom_role_properties_dictionary[privilege_type] else True

            self.role_db.update_role_privilege(role_id, new_value, privilege_type)
            classroom_role_properties_dictionary[privilege_type] = new_value

            role_properties_dict = self.role_db.get_role_properties_dict(role_id)
            role_properties_text = self.get_role_properties_text(role_properties_dict)
            color_values = self.get_edit_role_keyboard_color_values(classroom_role_properties_dictionary)

            await self.state_transition(user_id, States.S_CLASSROOM_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS,
                                        role_properties_text, *color_values)

        elif payload["text"] == "Назад":
            role_id = self.role_db.get_customizing_role_id(user_id)
            role_properties_dict = self.role_db.get_role_properties_dict(role_id)
            role_properties_text = self.get_role_properties_text(role_properties_dict)

            await self.state_transition(user_id, States.S_EDIT_ROLE_MEMBERS_SETTINGS, role_properties_text)

        elif payload["text"] == "Главное меню":
            await self.trans_to_main_menu(user_id)

    @staticmethod
    def get_edit_role_keyboard_color_values(role_properties_dictionary: dict) -> list:
        """Returns keyboard_colors"""
        value_meaning_dict = {
            1: "positive",
            0: "negative"
        }
        return list(map(lambda value: value_meaning_dict[value], list(role_properties_dictionary.values())[:-3]))

    @staticmethod
    def get_role_properties_text(role_properties_dict: dict, role_properties_type=None) -> str:
        """Returns role_properties_text"""
        value_meaning_dict = {
            1: "✅",
            0: "❌"
        }
        role_properties_dict = role_properties_dict.copy()

        is_admin = role_properties_dict.pop("is_admin")
        is_default_member = role_properties_dict.pop("is_default_member")
        role_name = role_properties_dict.pop("role_name")

        if is_admin:
            role_name += " (Админ)"
        elif is_default_member:
            role_name += " (Дефолт)"

        diary_role_properties_text = "Дневник:\n" \
                                     "Редактирование текущего дз {}\n" \
                                     "Редактирование будущего дз {}\n" \
                                     "Редактирование эталонного расписания {}\n" \
                                     "Редактирование текущего расписания {}\n" \
                                     "Редактирование будущего расписания {}\n\n" \

        members_role_properties_text = "Участники:\n" \
                                       "Кикание участников {}\n" \
                                       "Приглашение в класс {}\n" \
                                       "Принятие заявок {}\n" \
                                       "Уведомление участников {}\n" \
                                       "Редактирование событий {}\n\n"

        classroom_role_properties_text = "Класс:\n" \
                                         "Изменение названия класса {}\n" \
                                         "Изменение названия школы {}\n" \
                                         "Изменение типа класса {}\n" \
                                         "Изменение описания класса {}\n" \
                                         "Изменение лимита участников {}"

        if role_properties_type == "diary":
            role_properties_text = "Роль: {}\n\n" \
                                   f"{diary_role_properties_text}"
        elif role_properties_type == "members":
            role_properties_text = "Роль: {}\n\n" \
                                   f"{members_role_properties_text}"
        elif role_properties_type == "classroom":
            role_properties_text = "Роль: {}\n\n" \
                                   f"{classroom_role_properties_text}"
        else:
            role_properties_text = "Роль: {}\n\n" \
                                   f"{diary_role_properties_text}" \
                                   f"{members_role_properties_text}" \
                                   f"{classroom_role_properties_text}"

        return role_properties_text.format(role_name,
                                           *map(lambda value: value_meaning_dict[value], role_properties_dict.values()))
