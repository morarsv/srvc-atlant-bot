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
    widget_data = dialog_manager.current_context().widget_data

    logins_list = start_data[StDataConst.list_ya_direct_logins.value]
    if 'Error' in logins_list:
        logins = []
        error = logins_list.pop()
        logins_text = i18n.project.direct.request.error(code=error['code'], detail=error['detail'])
    else:
        logins = [(login['Login'], f'{login['ClientId']}/{login['Login']}') for login in logins_list]
        logins = sorted(logins, key=lambda x: x[0])
        logins_text = i18n.project.ya.direct.add.logins.empty()if len(
            logins_list) == 0 else i18n.project.ya.direct.add.logins.full()
    selected = 1 if widget_data.get(WgDataConst.item.value, False) else None
    return {
        'logins': logins,
        'preview_text': logins_text,
        'btn_confirm': i18n.button.confirm(),
        'btn_continue': i18n.button.next(),
        'btn_back': i18n.button.back(),
        'selected': selected
    }
