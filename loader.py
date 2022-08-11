from handlers import *


async def on_startup() -> tuple:
    """Returns handlers_class and creates Database"""
    async with connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD
    ) as connection_to_create_db:
        async with connection_to_create_db.cursor() as cursor:
            await cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}""")


    # Classes for working with database's tables
    connection = await connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        db=DATABASE_NAME
    )

    user_db = UserDataCommands(connection)
    classroom_db = ClassroomCommands(connection)
    technical_support_db = TechnicalSupportCommands(connection)
    diary_homework_db = DiaryHomeworkCommands(connection)
    role_db = RoleCommands(connection)
    notification_db = NotificationCommands(connection)
    event_db = EventCommands(connection)

    # All handlers + bot
    bot = Bot(TOKEN)
    handlers_class = Handlers(bot=bot,
                              user_db=user_db,
                              classroom_db=classroom_db,
                              technical_support_db=technical_support_db,
                              diary_homework_db=diary_homework_db,
                              role_db=role_db,
                              notification_db=notification_db,
                              event_db=event_db
                              )

    return bot, handlers_class


bot, handlers_class = asyncio.run(on_startup())
