import asyncio
import logging

from aiogram import Bot, Dispatcher, types

from config import Config, load_config
from src.handlers import echo
from aiogram.filters import CommandStart, Command


logger = logging.getLogger(__name__)
argTo = -4090486317

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    @dp.message(CommandStart())
    async def process_start_command(message: types.Message):
        await message.answer(f"Hello, {message.from_user.first_name}!\n i repost bot")

    @dp.message(Command("set"))
    async def set_command(message: types.Message):
        args = message.text
        args = args.split()
        global argTo
        argTo = int(args[1])
        await message.answer(f"Forward messages to {argTo}")

    @dp.channel_post()
    async def forward_message(message: types.Message):
        await message.forward(argTo)

    #dp.include_router(echo.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
