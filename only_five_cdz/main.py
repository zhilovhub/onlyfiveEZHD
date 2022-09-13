from only_five_cdz.handlers import *

# Bot + handlers
bot = Bot(MAIN_TOKEN)
handlers_class = Handlers(bot)


@bot.on.message()
async def listen_message(message: Message) -> None:
    """Listening new messages"""
    user_id = message.from_id  # Getting user_id
    message_text = message.text.strip()  # Getting message's text
    attachments = message.attachments

    await handlers_class.send_message(user_id, "Бот закрыт на тех обслуживание")
    # if await handlers_class.is_member(user_id):
    #     if (not attachments or attachments and not attachments[0].link) and not message_text:
    #         await handlers_class.send_message(user_id, "Ты должен отправить ссылку на мэш-тест")
    #     else:
    #         if attachments and attachments[0].link:
    #             url = attachments[0].link.url
    #         else:
    #             url = message_text
    #         await handlers_class.handler(user_id, url)
    #
    # else:
    #     await handlers_class.send_message(user_id, "Перед использованием бота подпишись на группу!")


async def create_tasks() -> None:
    """Creates tasks for asyncio"""
    tasks = [
        bot.run_polling(),
        handlers_class.set_auth_data()
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(create_tasks())
