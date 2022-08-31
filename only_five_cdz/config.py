import asyncio
import aiohttp
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, OpenLink

from random import randint
from json import dumps

import os

if os.path.exists("set_environ_vars.py"):
    import only_five_cdz.set_environ_vars

ADMIN_ID = os.environ["ADMIN_ID"]
GROUP_ID_CDZ = os.environ["GROUP_ID_CDZ"]

MAIN_TOKEN = os.environ["MAIN_TOKEN"]

AUTH_TOKEN = os.environ["AUTH_TOKEN"]
