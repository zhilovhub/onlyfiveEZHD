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
    S_IN_CLASS_MYCLASSES2 = 37
    S_EDIT_WEEK_MYCLASSES = 8
    S_EDIT_WEEKDAY_MYCLASSES = 9
    S_ADD_NEW_LESSON_WEEKDAY_MYCLASSES = 10
    S_EDIT_LESSON_WEEKDAY_MYCLASSES = 11
    S_EDIT_HOMEWORK_MYCLASSES = 40
    S_EDIT_HOMEWORK_WEEKDAY_MYCLASSES = 41
    S_CHOOSE_EVENT_MYCLASSES = 43
    S_CHOOSE_EVENT_TYPE_MYCLASSES = 44
    S_ENTER_NOT_COLLECTIVE_EVENT_NAME_MYCLASSES = 45
    S_ENTER_NOT_COLLECTIVE_EVENT_START_TIME_MYCLASSES = 46
    S_ENTER_NOT_COLLECTIVE_EVENT_END_TIME_MYCLASSES = 47
    S_SUBMIT_EVENT_CREATE_MYCLASSES = 48
    S_ENTER_COLLECTIVE_EVENT_NAME_MYCLASSES = 49
    S_ENTER_COLLECTIVE_EVENT_START_TIME_MYCLASSES = 50
    S_ENTER_COLLECTIVE_EVENT_END_TIME_MYCLASSES = 51
    S_ENTER_COLLECTIVE_EVENT_REQUIRED_COUNT_MYCLASSES = 52
    S_ENTER_COLLECTIVE_EVENT_REQUIRED_STUDENT_MYCLASSES = 53
    S_EDIT_EVENT_MYCLASSES = 54
    S_ADD_COUNT_COLLECTIVE_EVENT_MYCLASSES = 55
    S_DECREASE_COUNT_COLLECTIVE_EVENT_MYCLASSES = 56
    S_EVENT_SETTINGS_MYCLASSES = 57
    S_ENTER_NEW_EVENT_NAME_MYCLASSES = 58

    S_FIND_CLASS = 12
    S_LOOK_CLASSROOM = 36
    S_REQUEST_CLASSROOM = 38
    S_EDIT_REQUEST_CLASSROOM = 39

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
    S_NOTIFICATION_SETTINGS_CLASSROOM_SETTINGS = 42

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
