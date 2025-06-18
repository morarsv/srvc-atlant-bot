import asyncio
from aiogram import Bot
from aiogram.types import Message


async def delete_msg(msg: Message, time: int, bot: Bot) -> None:
    await asyncio.sleep(time)
    await bot.delete_message(message_id=msg.message_id, chat_id=msg.chat.id)