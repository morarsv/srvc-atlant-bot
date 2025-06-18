import logging
from typing import Any, Awaitable, Callable, Dict


from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


logger = logging.getLogger(__name__)


class MessageMonitorMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if hasattr(event, 'text'):
            bot = event.bot
            await bot.delete_message(chat_id=event.chat.id, message_id=event.message_id)
            if event.text in ['/info', '/help', '/authorization', '/faq']:
                return await handler(event, data)
            return

        return await handler(event, data)
