from aiogram import Router
from aiogram.types import Message


router: Router = Router()

@router.message()
async def process_any_message(message: Message):
    if (message.forward_from_chat is None):
        await message.reply("Im just repost bot")
    else:
        await message.reply(f"Chat ID: {message.forward_from_chat.id}")
