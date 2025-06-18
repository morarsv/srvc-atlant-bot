import logging

from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager, ShowMode
from fluentogram import TranslatorRunner


if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def main_getter(dialog_manager: DialogManager,
                      i18n: TranslatorRunner,
                      event_from_user: User,
                      **kwargs):

    return {
        'input_request': i18n.help.input.request(),
        'help': i18n.help.main(),
        'btn_help': i18n.button.submit.application()
    }
