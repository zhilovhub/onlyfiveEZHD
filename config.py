import os

# import for main file
import asyncio
import aioschedule
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback
from vkbottle import GroupEventType, GroupTypes
from random import randint, choice, choices
from string import ascii_letters, digits
from datetime import datetime, date, timedelta
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
ADMIN_ID = int(os.environ["ADMIN_ID"])
GROUP_ID = int(os.environ["GROUP_ID"])

# DB constants
DATABASE_URL = os.environ["DATABASE_URL"]

INTRODUCTION_MESSAGE = """✌🏻 Добро пожаловать в наше сообщество!

Этот бот - аналог ЭЖД (электронного дневника школьника)

Создан он для того, чтобы его пользователи могли ввести и редактировать в пару кликов свой электронный дневник школьника, всегда могли быть в курсе актуальных событий своего класса, а также имели возможность удобно уведомлять о всяких событиях ❗

P.S. Также этот бот будет очень полезен студентам, у которых зачастую отсутствуют электронные дневники

⚙ Краткое введение в функционал бота:

1. С помощью этого бота можно создавать свои классы, искать классы других людей. Эти функции можно найти в главном меню 🔑

2. В классе можно редактировать расписание и домашние задания, объявлять события, создавать уведомления (которые должны прийти в указанное время) для конкретных участников 📕

3. Во избежание хаоса в классе, связанного с нежелательным редактированием расписания и т.д, админ может создавать для участников роли, у которых будут свои привилегии 🚯"""
