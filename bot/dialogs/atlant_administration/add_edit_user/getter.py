import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager

from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            DialogDataConstant as DgDataConst)

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def input_getter(dialog_manager: DialogManager,
                       i18n: TranslatorRunner,
                       event_from_user: User,
                       **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    input_login = (f'{i18n.error.uniq.login()}\n'
                   f'\n{i18n.input.login()}') if widget_data.get(WgDataConst.err_uniq_login.value, False) else \
        i18n.input.login()
    return {
        'input_username': i18n.input.username(),
        'input_login': input_login,
        'input_password': i18n.input.password(),
        'btn_cancel': i18n.button.cancel()
    }


async def card_user_getter(dialog_manager: DialogManager,
                           i18n: TranslatorRunner,
                           event_from_user: User,
                           **kwargs):
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data
    dialog_data = dialog_manager.dialog_data

    dialog_data[DgDataConst.finished_key.value] = True
    user_edit = start_data.get(StDataConst.user_edit.value, False)
    company_name = start_data[StDataConst.company_name.value]

    if user_edit:
        start_data[StDataConst.user_edit.value] = False
        widget_data[WgDataConst.user_edit.value] = True

        username = start_data[StDataConst.username.value]
        login = start_data[StDataConst.user_login.value]

        widget_data[WgDataConst.username.value] = username
        widget_data[WgDataConst.user_login.value] = login
        widget_data[WgDataConst.company_name.value] = company_name

    username = widget_data[WgDataConst.username.value]
    login = widget_data[WgDataConst.user_login.value]
    password = widget_data.get(WgDataConst.user_password.value, '-')

    preview_text = i18n.atlant.admin.info.edit.user(
        full_name=username,
        login=login,
        password=password,
        company=company_name
    )

    return {
        'preview_text': preview_text,
        'btn_edit_username': i18n.button.edit.username(),
        'btn_edit_password': i18n.button.edit.password(),
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back()
    }
