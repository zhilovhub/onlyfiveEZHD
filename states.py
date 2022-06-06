from enum import Enum


class States(Enum):
    """Dialog States"""

    S_NOTHING = 0

    S_ENTER_NAME_CLASSCREATE = 1
    S_ENTER_CAN_INVITE_EVERYONE_CLASSCREATE = 2
    S_SUBMIT_CLASSCREATE = 3
