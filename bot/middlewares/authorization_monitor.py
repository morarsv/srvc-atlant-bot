import logging

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from aiogram_dialog import DialogManager, StartMode, ShowMode
from bot.database import query
from bot.database.models import Users
from bot.lexicon.constants.constant import PoolingConstant as poolConst
from bot.state.dialog_state import ConnectUserSG
from bot.support_models.models import SupportSessionUser

logger = logging.getLogger(__name__)


class AuthorizationMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        user_data: User = data.get(poolConst.event_from_user.value)
        bot = event.bot
        tg_id = int(user_data.id)
        online: dict[int, SupportSessionUser] = data.get(poolConst.online_users.value)
        if tg_id in online.keys():
            return await handler(event, data)
        else:
            user: Users = await query.get_user_by_tg_id(tg_id=tg_id)
            if user is not None:
                online[tg_id] = SupportSessionUser(
                    username=user.full_name,
                    login=user.login,
                    role_id=user.role_id,
                    user_uuid=user.id,
                    company_id=user.company_id,
                    company_name=user.company.company
                )
                data[poolConst.online_users.value] = online
                return await handler(event, data)
            else:
                try:
                    await bot.delete_message(chat_id=event.chat.id,
                                             message_id=event.message_id)
                except AttributeError as e:
                    logger.error(f'Error deleting message: {e}')

                dialog: DialogManager = data[poolConst.dialog_manager.value]
                try:
                    await dialog.start(state=ConnectUserSG.PREVIEW,
                                       mode=StartMode.RESET_STACK,
                                       show_mode=ShowMode.DELETE_AND_SEND)
                except AttributeError as e:
                    logger.error(f'Error deleting message: {e}')
                    await dialog.start(state=ConnectUserSG.PREVIEW,
                                       mode=StartMode.RESET_STACK,
                                       show_mode=ShowMode.SEND)
