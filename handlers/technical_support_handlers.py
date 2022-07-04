from supporting_functions import *


class TechnicalSupportHandlers(SupportingFunctions):
    def __init__(self, token: str, group_id: int, user_db: UserDataCommands,
                 classroom_db: ClassroomCommands, technical_support_db: TechnicalSupportCommands,
                 diary_homework_db: DiaryHomeworkCommands, role_db: RoleCommands) -> None:
        """Initialization"""
        super().__init__(token=token, group_id=group_id, user_db=user_db, classroom_db=classroom_db,
                         technical_support_db=technical_support_db, diary_homework_db=diary_homework_db,
                         role_db=role_db)

    def s_enter_technical_support_message_handler(self, user_id: int, message: str) -> None:
        """Handling States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE"""
        if message == "Отменить":
            self.cancel_entering_technical_support_message(user_id)

        elif message == "Отправить":
            trans_message = "Вопросы отправлены администраторам!"
            self.state_transition(user_id, States.S_NOTHING, "menu", trans_message)

        else:
            user_message = self.technical_support_db.get_message(user_id) + "\n"
            user_message += message
            self.technical_support_db.insert_message(user_id, user_message)

    def cancel_entering_technical_support_message(self, user_id: int) -> None:
        """Cancel creating technical support message and set state to States.S_NOTHING"""
        self.send_message(user_id, "Отправка обращения в тех. поддержку отменена", self.get_keyboard("menu"))
        self.user_db.set_user_dialog_state(user_id, States.S_NOTHING.value)
