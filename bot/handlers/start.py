import logging
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode, ShowMode
from bot.state.dialog_state import StartSG, AuthorizationSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.support_models.models import SupportSessionUser
from bot.lexicon.constants.constant import (PoolingConstant as poolConst,
                                            StartDataConstant as StDataConst)

start_router = Router()
start_router.message.middleware(AuthorizationMiddleware())
start_router.callback_query.middleware(AuthorizationMiddleware())

logger = logging.getLogger(__name__)


@start_router.message(CommandStart())
async def command_start_process(message: Message,
                                dialog_manager: DialogManager,
                                bot: Bot):
    try:
        await bot.delete_message(message_id=message.message_id,
                                 chat_id=message.chat.id)
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    middleware_data = dialog_manager.middleware_data
    tg_id = int(message.from_user.id)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]
    user: SupportSessionUser = online_users.get(tg_id)
    username: str = user['username']
    role_id: int = user['role_id']

    await dialog_manager.start(state=StartSG.PREVIEW,
                               mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.EDIT,
                               data={
                                   StDataConst.username.value: username,
                                   StDataConst.user_role_id.value: role_id
                               })
