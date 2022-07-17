# WRITE VALUES AND RENAME THIS FILE TO config.py

from vk_api.keyboard import VkKeyboard  # import for Keyboards
# import for main file
from vkbottle.bot import Bot, Message
from vkbottle import GroupEventType, GroupTypes
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardButton
from random import randint, choice
from datetime import datetime
from re import search, fullmatch
from json import loads, dumps
# import for states file
from enum import Enum
# import for database file
from mysql.connector import connect, Error
from mysql.connector.connection_cext import CMySQLConnection

# VK_api constants
TOKEN = ""
ADMINS_ID = []
GROUP_ID = 0

# DB constants
HOST = ""
USER = ""
PASSWORD = ""
DATABASE_NAME = ""
