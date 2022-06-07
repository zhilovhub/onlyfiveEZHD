from vk_api.keyboard import VkKeyboard  # import for Keyboards
# import for main file
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api.exceptions import VkApiError
from random import randint
# import for states file
from enum import Enum
# import for database file
from mysql.connector import connect, Error

# VK_api constants
TOKEN = ""  # Write here the group token
ADMIN_ID = 0  # Write here the admin id
GROUP_ID = 0  # Write here the group id

# DB constants
HOST = "localhost"  # Write here the db host
USER = "root"  # Write here the db user
PASSWORD = "1234"  # Write here the db password
DATABASE_NAME = "bot_main_db"  # Write here the db name
