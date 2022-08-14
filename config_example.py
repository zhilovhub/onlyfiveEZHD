# WRITE VALUES AND RENAME THIS FILE TO config.py

# import for main file
import asyncio
import aioschedule
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback
from vkbottle import GroupEventType, GroupTypes
from random import randint, choice, choices
from string import ascii_letters, digits
from datetime import datetime, date
from re import search, fullmatch
from json import loads, dumps
# import for states file
from enum import Enum
# import for database file
from psycopg2 import connect, Error
from mysql.connector.connection_cext import CMySQLConnection

# VK_api constants
TOKEN = ""
ADMINS_ID = []
GROUP_ID = 0

# DB constants
HOST = ""
PORT = 0
USER = ""
PASSWORD = ""
DATABASE_NAME = ""
