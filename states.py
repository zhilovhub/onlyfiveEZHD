from config import *


class States(Enum):
    """Dialog States"""

    S_NOTHING = 0

    S_ENTER_CLASS_NAME_CLASSCREATE = 1
    S_ENTER_SCHOOL_NAME_CLASSCREATE = 2
    S_ENTER_ACCESS_CLASSCREATE = 3
    S_ENTER_DESCRIPTION_CLASSCREATE = 4
    S_SUBMIT_CLASSCREATE = 5

    S_IN_CLASS_MYCLASSES = 6
    S_TIMETABLE_MENU_MYCLASSES = 7
    S_TIMETABLE_MYCLASSES = 8

    @staticmethod
    def get_next_state_config(current_state: Enum) -> tuple:
        """Returns next state's configuration"""
        match current_state:
            case States.S_ENTER_CLASS_NAME_CLASSCREATE:
                return States.S_ENTER_SCHOOL_NAME_CLASSCREATE, \
                       "cancel_back", \
                       ["Название школы будущего класса (макс. 32 символа):"]

            case States.S_ENTER_SCHOOL_NAME_CLASSCREATE:
                return States.S_ENTER_ACCESS_CLASSCREATE, \
                       "yes_no_cancel_back", \
                       ["Могут ли участники класса приглашать других людей?"]

            case States.S_ENTER_ACCESS_CLASSCREATE:
                return States.S_ENTER_DESCRIPTION_CLASSCREATE, \
                       "cancel_back", \
                       ["Краткое описание класса (макс. 200 символов):"]

            case States.S_ENTER_DESCRIPTION_CLASSCREATE:
                return States.S_SUBMIT_CLASSCREATE, \
                       "submit_back", \
                       ["Создать класс?"]

            case States.S_SUBMIT_CLASSCREATE:
                return States.S_NOTHING, \
                       "menu", \
                       []
