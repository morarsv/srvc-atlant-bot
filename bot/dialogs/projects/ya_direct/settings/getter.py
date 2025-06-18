import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (StartDataConstant as StDataConst,
                                            WidgetDataConstant as WgDataConst)

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    start_data = dialog_manager.start_data

    active_logins = start_data[StDataConst.ya_direct_activated_logins.value] or '-'
    inactive_logins = start_data[StDataConst.ya_direct_deactivated_logins.value] or '-'
    active = start_data[StDataConst.ya_direct_deactivated_logins.value]
    inactive = start_data[StDataConst.ya_direct_activated_logins.value]
    return {
        'preview_text': i18n.project.ya.direct.logins.settings.preview(active=active_logins,
                                                                       inactive=inactive_logins),
        'btn_activate': i18n.button.ya.logins.activate(),
        'btn_deactivate': i18n.button.ya.logins.deactivate(),
        'btn_cancel': i18n.button.cancel(),
        'activate': active,
        'inactive': inactive
    }


async def logins_activate_getter(dialog_manager: DialogManager,
                                 i18n: TranslatorRunner,
                                 event_from_user: User,
                                 **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    logins = start_data[StDataConst.project_ya_list_inactive_logins.value]
    selected = 1 if widget_data.get(WgDataConst.project_ya_activated_logins.value, False) else None
    return {
        'logins': logins,
        'logins_text': i18n.project.ya.direct.logins.settings.activate(),
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back(),
        'selected': selected
    }


async def logins_deactivate_getter(dialog_manager: DialogManager,
                                   i18n: TranslatorRunner,
                                   event_from_user: User,
                                   **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    logins = start_data[StDataConst.project_ya_list_active_logins.value]
    selected = 1 if widget_data.get(WgDataConst.project_ya_deactivated_logins.value, False) else None
    return {
        'logins': logins,
        'logins_text': i18n.project.ya.direct.logins.settings.deactivate(),
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back(),
        'selected': selected
    }
