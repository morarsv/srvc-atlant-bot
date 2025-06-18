import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst

from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def input_company_getter(dialog_manager: DialogManager,
                               i18n: TranslatorRunner,
                               event_from_user: User,
                               **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    preview_text = i18n.input.company()
    if widget_data.get(WgDataConst.err_uniq_company.value, False):
        preview_text = (f'{i18n.error.uniq.company()}\n'
                        f'{i18n.input.company()}')

    return {
        'preview_text': preview_text
    }


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    widget_data = dialog_manager.current_context().widget_data

    company_name = widget_data[WgDataConst.company_name.value]
    preview_text = i18n.atlant.admin.add.company.preview(company=company_name)
    return {
        'preview_text': preview_text,
        'btn_edit_company': i18n.button.edit.company(),
        'btn_add_user': i18n.button.add.user(),
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back()
    }