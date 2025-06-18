import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode, ShowMode
from bot.state.dialog_state import AuthorizationSG
from bot.database.models import Users
from bot.lexicon.constants.constant import (PoolingConstant as poolConst,
                                            StartDataConstant as StDataConst)
from bot.database import query
from bot.middlewares.authorization_monitor import AuthorizationMiddleware

logger = logging.getLogger(__name__)

authorization_router = Router()
authorization_router.message.middleware(AuthorizationMiddleware())
authorization_router.callback_query.middleware(AuthorizationMiddleware())


@authorization_router.message(Command('authorization'))
async def command_start_process(message: Message,
                                dialog_manager: DialogManager,
                                bot: Bot):
    middleware_data = dialog_manager.middleware_data
    online_users: dict[int: str] = middleware_data[poolConst.online_users.value]
    tg_id = message.from_user.id
    authorized, unauthorized = False, False
    try:
        await bot.delete_message(message_id=message.message_id,
                                 chat_id=message.chat.id)
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')

    if tg_id in online_users:
        authorized = True
    else:
        user: Users = await query.get_user_by_tg_id(tg_id=tg_id)
        if user:
            authorized = True
        else:
            unauthorized = False

    await dialog_manager.start(state=AuthorizationSG.PREVIEW,
                               mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.EDIT,
                               data={
                                   StDataConst.authorized.value: authorized,
                                   StDataConst.unauthorized.value: unauthorized,
                               })
