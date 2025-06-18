import logging
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from bot.database import query
from bot.database.models import Users
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.utils.bot_func import bot_current_time
from fluentogram import TranslatorRunner
from typing import TYPE_CHECKING
from bot.lexicon.constants.constant import PoolingConstant as poolConst

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner
logger = logging.getLogger(__name__)


async def btn_help(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data[poolConst.i18n.value]
    time = await bot_current_time()

    tg_id = int(callback.from_user.id)
    username = f'@{callback.message.chat.username}' if callback.message.chat.username else \
        i18n.unknown.user()
    adr = f'<a href="tg://user?id={tg_id}">{username}</a>'
    await callback.message.bot.send_message(chat_id=LEXICON_TG_BOT['CHAT_ID'],
                                            text=i18n.help.submit.request.unknown(username=adr,
                                                                                  datetime=time))
    await dialog_manager.done()


async def submit_application(message: Message,
                             widget: ManagedTextInput,
                             dialog_manager: DialogManager,
                             text: str) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    await message.bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
    i18n: TranslatorRunner = dialog_manager.middleware_data[poolConst.i18n.value]
    time = await bot_current_time()

    tg_id = int(message.from_user.id)
    username = f'@{message.chat.username}' if message.chat.username else \
        i18n.unknown.user()
    adr = f'<a href="tg://user?id={tg_id}">{username}</a>'
    user: Users = await query.get_user_by_tg_id(tg_id=tg_id)
    msg = i18n.help.submit.request.user(login=user.login,
                                        company_name=user.company.company,
                                        datetime=time,
                                        text=text)
    await message.bot.send_message(chat_id=LEXICON_TG_BOT['CHAT_ID'],
                                   text=i18n.user.url() + adr + '\n' + msg)
    await dialog_manager.done()
