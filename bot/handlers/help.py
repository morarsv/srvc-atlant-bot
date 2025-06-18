from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from fluentogram import TranslatorRunner
from bot.database.models import Users
from bot.database import query
from bot.state.dialog_state import HelpSG
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

help_router = Router()


@help_router.message(Command('help'))
async def cmd_help(message: Message,
                   dialog_manager: DialogManager,
                   i18n: TranslatorRunner,
                   bot: Bot) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    try:
        await bot.delete_message(message_id=message.message_id,
                                 chat_id=message.chat.id)
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    tg_id = int(message.from_user.id)
    user: Users = await query.get_user_by_tg_id(tg_id=tg_id)

    if user:
        await dialog_manager.start(state=HelpSG.REQUEST, mode=StartMode.NORMAL)
    else:
        await dialog_manager.start(state=HelpSG.MAIN, mode=StartMode.NORMAL)
