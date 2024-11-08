from supporting_functions import *


class TechnicalSupportHandlers(SupportingFunctions):
    def __init__(self, bot: Bot, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands,
                 notification_db: NotificationCommands, event_db: EventCommands, admin_panel_db: AdminCommands) -> None:
        """Initialization"""
        super().__init__(bot=bot, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db, notification_db=notification_db, event_db=event_db,
                         admin_panel_db=admin_panel_db)

    async def s_enter_technical_support_message_handler(self, user_id: int, message: str, payload: dict) -> None:
        """Handling States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE"""
        if payload is None:
            user_message = self.technical_support_db.get_message(user_id) + "\n"
            user_message += message
            self.technical_support_db.insert_message(user_id, user_message)

        elif payload["text"] == "Отменить":
            await self.cancel_entering_technical_support_message(user_id)

        elif payload["text"] == "Отправить":
            trans_message = "Вопросы отправлены администраторам!"
            await self.state_transition(user_id, States.S_NOTHING, trans_message)

    async def cancel_entering_technical_support_message(self, user_id: int) -> None:
        """Cancel creating technical support message and set state to States.S_NOTHING"""
        trans_message = "Отправка обращения в тех. поддержку отменена"
        await self.state_transition(user_id, States.S_NOTHING, trans_message)
