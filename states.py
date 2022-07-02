from config import *


class States(Enum):
    """Dialog States"""

    S_NOTHING = 0

    S_ENTER_CLASS_NAME_CLASSCREATE = 1
    S_ENTER_SCHOOL_NAME_CLASSCREATE = 2
    S_ENTER_ACCESS_CLASSCREATE = 3
    S_ENTER_DESCRIPTION_CLASSCREATE = 4
    S_SUBMIT_CLASSCREATE = 5

    S_ENTER_TECHNICAL_SUPPORT_MESSAGE = 6

    S_IN_CLASS_MYCLASSES = 7
    S_EDIT_WEEK_MYCLASSES = 8
    S_EDIT_WEEKDAY_MYCLASSES = 9
    S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES = 10
    S_EDIT_LESSON_WEEKDAY_MYCLASSES = 11

    S_FIND_CLASS = 12
    S_LOOK_CLASSROOM = 36

    S_CLASSROOM_SETTINGS = 13
    S_MAIN_CLASSROOM_SETTINGS = 14
    S_MAIN_DANGEROUS_ZONE_CLASSROOM_SETTINGS = 15
    S_MAIN_DANGEROUS_ZONE_DELETE_ONE_CLASSROOM_SETTINGS = 16
    S_MAIN_DANGEROUS_ZONE_DELETE_TWO_CLASSROOM_SETTINGS = 17
    S_ACCESS_MAIN_CLASSROOM_SETTINGS = 18
    S_CLASSROOM_NAME_MAIN_CLASSROOM_SETTINGS = 19
    S_SCHOOL_NAME_MAIN_CLASSROOM_SETTINGS = 20
    S_DESCRIPTION_MAIN_CLASSROOM_SETTINGS = 21
    S_LIMIT_MAIN_CLASSROOM_SETTINGS = 22

    S_MEMBERS_SETTINGS = 23
    S_ADD_ROLE_ENTER_NAME_MEMBERS_SETTINGS = 24
    S_DELETE_ROLE_MEMBERS_SETTINGS = 25
    S_DELETE_MEMBER_MEMBERS_SETTINGS = 26
    S_CHOOSE_ROLE_MEMBERS_SETTINGS = 27
    S_CHOOSE_ADMIN_ROLE_CONFIRMATION_MEMBERS_SETTINGS = 28
    S_CHOOSE_MEMBER_CHANGE_ROLE_MEMBERS_SETTINGS = 29
    S_CHOOSE_ROLE_EDIT_ROLE_MEMBERS_SETTINGS = 30
    S_EDIT_ROLE_MEMBERS_SETTINGS = 31
    S_ENTER_NAME_EDIT_ROLE_MEMBERS_SETTINGS = 32
    S_DIARY_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS = 33
    S_MEMBERS_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS = 34
    S_CLASSROOM_PRIVILEGE_EDIT_ROLE_MEMBERS_SETTINGS = 35

    @staticmethod
    def get_next_state_config(current_state: Enum) -> tuple:
        """Returns next state's configuration"""
        match current_state:
            case States.S_ENTER_CLASS_NAME_CLASSCREATE:
                return States.S_ENTER_SCHOOL_NAME_CLASSCREATE, \
                       "back_menu", \
                       "Название школы будущего класса (макс. 32 символа):"

            case States.S_ENTER_SCHOOL_NAME_CLASSCREATE:
                return States.S_ENTER_ACCESS_CLASSCREATE, \
                       "access_menu_back", \
                       "Тип будущего класса?"

            case States.S_ENTER_ACCESS_CLASSCREATE:
                return States.S_ENTER_DESCRIPTION_CLASSCREATE, \
                       "back_menu", \
                       "Краткое описание класса (макс. 200 символов):"

            case States.S_ENTER_DESCRIPTION_CLASSCREATE:
                return States.S_SUBMIT_CLASSCREATE, \
                       "submit_back", \
                       "Создать класс?"

            case States.S_SUBMIT_CLASSCREATE:
                return States.S_NOTHING, \
                       "menu", \
                       "Поздравляю! Класс создан"

            case States.S_ENTER_TECHNICAL_SUPPORT_MESSAGE:
                return States.S_NOTHING, \
                       "menu", \
                       "Вопросы отправлены администраторам!"
