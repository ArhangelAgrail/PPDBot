import asyncio
import logging

from aiogram import F, Bot, Dispatcher, types
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from config import Config, load_config
from src.handlers import echo
from aiogram.filters import CommandStart, Command


logger = logging.getLogger(__name__)
argTo = -1002435540164
argFrom = -1002003989241

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
        await message.answer(f"Hello, {message.from_user.first_name}!\n its repost bot")

    @dp.message(Command("setTo"))
    async def set_command(message: types.Message):
        args = message.text
        args = args.split()
        global argTo
        argTo = int(args[1])
        await message.answer(f"Forward messages to {argTo} from {argFrom}")

    @dp.message(Command("setFrom"))
    async def set_command(message: types.Message):
        args = message.text
        args = args.split()
        global argFrom
        argFrom = int(args[1])
        await message.answer(f"Forward messages from {argFrom} to {argTo}")

    @dp.channel_post()
    async def forward_message(message: types.Message):
        if (message.chat.id == argFrom):
            await message.forward(argTo)

    @dp.message(F.photo)
    async def modify_image(message: types.Message):
        await message.answer(f"Get this")

        bio1 = BytesIO()
        bio1.name = 'image.png'
        await message.bot.download(message.photo[-1], bio1)
        bio1.seek(0)
    
        image = Image.open(bio1)
    
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial.ttf', 36)
        draw.text((10, 10), "modified image", font=font)
    
        bio = BytesIO()
        image.save(bio, 'PNG')
        bio.seek(0)
    
        await message.answer_photo(types.BufferedInputFile(bio.read(), 'img.png'))

    @dp.message()
    async def handle_request_chat(message: types.Message):
        if (message.forward_from is not None):
            await message.reply(f"Chat ID: {message.chat.id}")
        else:
            if (message.forward_from_chat is not None):
                await message.reply(f"Channel ID: {message.forward_from_chat.id}")

    #dp.include_router(echo.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
