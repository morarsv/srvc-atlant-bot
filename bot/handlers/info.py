import logging
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from bot.state.dialog_state import InfoSG


info_router = Router()

logger = logging.getLogger(__name__)


@info_router.message(Command('info'))
async def cmd_info(message: Message,
                   dialog_manager: DialogManager,
                   bot: Bot) -> None:
    try:
        await bot.delete_message(message_id=message.message_id,
                                 chat_id=message.chat.id)
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')

    try:
        await dialog_manager.start(state=InfoSG.PREVIEW,
                                   show_mode=ShowMode.EDIT,
                                   mode=StartMode.RESET_STACK)
    except AttributeError as e:
        logger.error(f'Error: {e}')
        await dialog_manager.start(state=InfoSG.PREVIEW,
                                   show_mode=ShowMode.SEND,
                                   mode=StartMode.RESET_STACK)
