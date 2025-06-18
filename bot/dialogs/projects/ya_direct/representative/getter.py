import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def representative_getter(dialog_manager: DialogManager,
                                i18n: TranslatorRunner,
                                event_from_user: User,
                                **kwargs):
    widget_data = dialog_manager.current_context().widget_data

    accept_data = widget_data.get(WgDataConst.ya_direct_representative_accept_logins.value, [])
    deny_data = widget_data.get(WgDataConst.ya_direct_representative_deny_logins.value, [])

    accept_logins = ', '.join(accept_data) or '-'
    deny_logins = ', '.join(deny_data) or '-'
    preview_text = i18n.project.ya.direct.add.representative.description.add()
    preview_text = f'{i18n.project.ya.direct.add.representative.logins(
        accept=accept_logins,
        deny=deny_logins
    )}\n\n{preview_text}' if accept_data or deny_data else preview_text
    preview_text = f'{preview_text}\n\n{i18n.project.ya.direct.add.representative.description.select()}' \
        if accept_data else preview_text

    accept = 1 if accept_data else None
    return {
        'preview_text': preview_text,
        'btn_add_logins': i18n.button.add.ya.logins(),
        'btn_select_logins': i18n.button.select.logins(),
        'btn_cancel': i18n.button.cancel(),
        'accept': accept
    }


async def logins_getter(dialog_manager: DialogManager,
                        i18n: TranslatorRunner,
                        event_from_user: User,
                        **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    accept_logins = widget_data[WgDataConst.ya_direct_representative_accept_logins.value]
    logins = [(i, i) for i in accept_logins]
    selected = 1 if widget_data.get(WgDataConst.item.value) else None
    return {
        'preview_text': i18n.project.ya.direct.add.representative.accept.add.logins(),
        'logins': logins,
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back(),
        'selected': selected
    }


async def input_getter(dialog_manager: DialogManager,
                       i18n: TranslatorRunner,
                       event_from_user: User,
                       **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    status = widget_data.get(WgDataConst.err_input_login.value, False)
    preview_text = i18n.project.ya.direct.add.representative.input.logins()
    preview_text = (f'{i18n.project.ya.direct.add.representative.input.error()}\n\n'
                    f'{preview_text}') if status else preview_text

    return {
        'preview_text': preview_text,
        'btn_back': i18n.button.back()
    }
