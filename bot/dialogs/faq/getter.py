import logging
from aiogram.types import User
from typing import TYPE_CHECKING
from aiogram_dialog import DialogManager, ShowMode
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (StartDataConstant as StDataConst,
                                            WidgetDataConstant as WgDataConst)
if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def main_getter(dialog_manager: DialogManager,
                      i18n: TranslatorRunner,
                      event_from_user: User,
                      **kwargs):
    start_data = dialog_manager.start_data
    faq = start_data[StDataConst.faq.value]
    preview_text = i18n.faq.preview()

    return {
        'preview_text': preview_text,
        'faq': faq
    }


async def faq_getter(dialog_manager: DialogManager,
                     i18n: TranslatorRunner,
                     event_from_user: User,
                     **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    faq = widget_data[WgDataConst.faq.value]
    return {
        'faq': faq,
        'btn_back': i18n.button.back()
    }
