import logging

from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from bot.state.dialog_state import AuthorizationSG, ConnectUserSG
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.utils.bot_func import bot_current_time
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (DialogDataConstant as dialogConst,
                                            PoolingConstant as poolDataConst,
                                            StartDataConstant as StDataConst)
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)

_chat_id = LEXICON_TG_BOT['CHAT_ID_ACC_ALERTS']


async def btn_authorization(callback: CallbackQuery,
                            widget: Any,
                            dialog_manager: DialogManager) -> None:
    authorized, unauthorized = False, True
    try:
        await dialog_manager.start(state=AuthorizationSG.PREVIEW,
                                   mode=StartMode.RESET_STACK,
                                   show_mode=ShowMode.DELETE_AND_SEND,
                                   data={
                                       StDataConst.authorized.value: authorized,
                                       StDataConst.unauthorized.value: unauthorized,
                                   })
    except AttributeError as e:
        await dialog_manager.start(state=AuthorizationSG.PREVIEW,
                                   mode=StartMode.RESET_STACK,
                                   show_mode=ShowMode.SEND,
                                   data={
                                       StDataConst.authorized.value: authorized,
                                       StDataConst.unauthorized.value: unauthorized,
                                   })
        logger.error(f'Error deleting message: {e}')


async def err_format_company(message: Message,
                             widget: ManagedTextInput,
                             dialog_manager: DialogManager,
                             error: ValueError):
    await dialog_manager.switch_to(state=ConnectUserSG.INPUT_COMPANY,
                                   show_mode=ShowMode.EDIT)
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')


async def btn_next_or_end(message: Message,
                          widget: ManagedTextInput,
                          dialog_manager: DialogManager,
                          text: str) -> None:
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def next_or_end_company(message: Message,
                              widget: ManagedTextInput,
                              dialog_manager: DialogManager,
                              text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data
    i18n: TranslatorRunner = middleware_data[poolDataConst.i18n.value]
    company_name = text
    username = widget_data[dialogConst.username.value]
    tg_id = int(message.from_user.id)
    time = await bot_current_time()
    adr = f'<a href="tg://user?id={tg_id}">{username}</a>'
    msg = i18n.help.application.form(username=adr,
                                     company_name=company_name,
                                     datetime=time)
    await message.bot.send_message(chat_id=_chat_id,
                                   text=msg)
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    await dialog_manager.switch_to(state=ConnectUserSG.APPLICATION_FORM,
                                   show_mode=ShowMode.EDIT)
