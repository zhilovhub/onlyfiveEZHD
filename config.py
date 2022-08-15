import os

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
# from mysql.connector import connect, CMySQLConnection, Error
# from aiomysql import create_pool, connect, Error, Pool
from psycopg2 import connect, Error

if os.path.exists("set_environ_vars.py"):
    import set_environ_vars

# VK_api constants
TOKEN = os.environ["TOKEN"]
ADMINS_ID = loads(os.environ["ADMINS_ID"])
GROUP_ID = int(os.environ["GROUP_ID"])

# DB constants
HOST = os.environ["HOST"]
PORT = int(os.environ["PORT"])
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
