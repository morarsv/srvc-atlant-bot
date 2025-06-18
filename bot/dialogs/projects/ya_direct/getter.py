import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):

    return {
        'preview_text': i18n.project.ya.direct.add.preview(),
        'btn_agency': i18n.button.agency(),
        'btn_advertiser': i18n.button.advertiser(),
        'btn_representative': i18n.button.representative(),
        'btn_back': i18n.button.back()
    }
