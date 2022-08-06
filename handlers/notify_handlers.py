from supporting_functions import *


class NotificationHandlers(SupportingFunctions):
    def __init__(self, bot: Bot, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands, event_db: EventCommands) -> None:
        """Initialization"""
        super().__init__(bot=bot, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db, notification_db=notification_db, event_db=event_db)

    async def s_choose_user_for_notification_handler_my_classes(self, user_id: int, message: str, payload: dict
                                                                ) -> None:
        """Handling States.S_CHOOSE_USER_FOR_NOTIFICATION_MYCLASSES"""
        if payload is None:
            pass

        elif payload["text"] == "Всех":
            pass

        elif payload["text"] == "Назад":
            await self.cancel_creating_notification(user_id, to_main_menu=False)


        elif payload["text"] == "Главное меню":
            await self.cancel_creating_notification(user_id, to_main_menu=True)

    async def cancel_creating_notification(self, user_id: int, to_main_menu: bool) -> None:
        """Trans to classroom/main menu"""
        classroom_id = self.classroom_db.get_customizing_classroom_id(user_id)
        notification_id = self.notification_db.get_customizing_notification_id(user_id, classroom_id)
        self.notification_db.delete_notification_from_diary(notification_id)
        if to_main_menu:
            await self.trans_to_main_menu(user_id)
        else:
            await self.state_transition(user_id, States.S_IN_CLASS_MYCLASSES2, "Главное меню класса",
                                        sign=self.get_sign(user_id))
