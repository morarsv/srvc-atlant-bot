import logging
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from fluentogram import TranslatorRunner
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.state.dialog_state import FaqSG
from bot.support_models.models import SupportSessionUser
from typing import TYPE_CHECKING, Any
from bot.lexicon.constants.constant import (PoolingConstant as poolConst,
                                            StartDataConstant as StDataConst)

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

faq_router = Router()
faq_router.message.middleware(AuthorizationMiddleware())
faq_router.callback_query.middleware(AuthorizationMiddleware())

logger = logging.getLogger(__name__)


async def _get_faq_title_by_role(role_id: int,
                                 i18n: TranslatorRunner) -> list[tuple[str, Any]]:
    if role_id == 2:
        faq = [(i18n.faq.how.create.project.title(), 1),
               (i18n.faq.what.next.after.project.title(), 2),
               (i18n.faq.how.add.extra.counter.title(), 3),
               (i18n.faq.how.connect.disconnect.direct.logins.title(), 4),
               (i18n.faq.what.are.viewers.title(), 5),
               (i18n.faq.how.work.viewers.title(), 6)]
        return faq
    if role_id in [1, 3]:
        faq = [(i18n.faq.how.create.project.title(), 1),
               (i18n.faq.what.next.after.project.title(), 2),
               (i18n.faq.how.add.extra.counter.title(), 3),
               (i18n.faq.how.connect.disconnect.direct.logins.title(), 4),
               (i18n.faq.what.are.viewers.title(), 5),
               (i18n.faq.how.work.viewers.title(), 6),
               (i18n.faq.what.are.management.profile.title(), 7),
               (i18n.faq.how.create.manager.title(), 8),
               (i18n.faq.how.give.withdraw.permission.title(), 9)]
        return faq
    if role_id == 4:
        return [(i18n.faq.where.see.project.report.title(), 10)]


@faq_router.message(Command('faq'))
async def faq_help(message: Message,
                   dialog_manager: DialogManager,
                   i18n: TranslatorRunner,
                   bot: Bot) -> None:
    middleware_data = dialog_manager.middleware_data
    dialog_manager.show_mode = ShowMode.EDIT
    try:
        await bot.delete_message(message_id=message.message_id,
                                 chat_id=message.chat.id)
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    tg_id = int(message.from_user.id)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    user: SupportSessionUser = online_users.get(tg_id)
    username: str = user['username']
    role_id: int = user['role_id']
    faq = await _get_faq_title_by_role(role_id=role_id, i18n=i18n)
    await dialog_manager.start(state=FaqSG.MAIN,
                               mode=StartMode.RESET_STACK,
                               data={
                                   StDataConst.username.value: username,
                                   StDataConst.user_role_id.value: role_id,
                                   StDataConst.faq.value: faq
                               })
