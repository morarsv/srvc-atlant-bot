import logging

from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from bot.lexicon.lexicon_tg import LEXICON_TEMPLATE

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)

_report = LEXICON_TEMPLATE['REPORT']


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    adr = f'<a href="{_report}">{i18n.template.report()}</a>'
    return {
        'menu_text': i18n.connect.user.preview(report=adr),
        'btn_authorization': i18n.button.authorization(),
        'btn_filled_application': i18n.button.filled.application()
    }


async def input_getter(dialog_manager: DialogManager,
                       i18n: TranslatorRunner,
                       event_from_user: User,
                       **kwargs):
    return {
        'input_username': i18n.input.username(),
        'input_company_name': i18n.input.company(),
        'menu_text': i18n.connect.user.send.form()
    }
