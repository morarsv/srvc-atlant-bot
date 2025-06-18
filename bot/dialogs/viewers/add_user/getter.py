import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager

from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
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


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    dialog_data = dialog_manager.dialog_data

    dialog_data[DgDataConst.finished_key.value] = True

    username = widget_data[WgDataConst.username.value]
    login = widget_data[WgDataConst.user_login.value]
    password = widget_data[WgDataConst.user_password.value]

    preview_text = i18n.viewers.add.info.viewer(
        full_name=username,
        login=login,
        password=password
    )
    return {
        'preview_text': preview_text,
        'btn_edit_username': i18n.button.edit.username(),
        'btn_edit_password': i18n.button.edit.password(),
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back()
    }
