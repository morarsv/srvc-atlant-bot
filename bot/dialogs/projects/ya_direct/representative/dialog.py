import logging
from operator import itemgetter

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button, ScrollingGroup, Multiselect, Column
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import YaDirectLoginsAddRepresentativeSG
from bot.dialogs.projects.ya_direct.representative.handler import (btn_cancel, input_success,
                                                                   btn_confirm, input_error, btn_back)
from bot.dialogs.projects.ya_direct.representative.getter import (logins_getter, input_getter,
                                                                  representative_getter)
from bot.utils.type_factory import check_format_list_logins
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst
from bot.middlewares.authorization_monitor import AuthorizationMiddleware

logger = logging.getLogger(__name__)

preview_window = Window(
    Format(
        text='{preview_text}',
    ),
    SwitchTo(
        text=Format(
            text='{btn_add_logins}'
        ),
        id='b_add_logins',
        state=YaDirectLoginsAddRepresentativeSG.INPUT_LOGINS
    ),
    SwitchTo(
        text=Format(
            text='{btn_select_logins}'
        ),
        id='b_select_logins',
        when='accept',
        state=YaDirectLoginsAddRepresentativeSG.LIST_LOGINS
    ),
    Button(
        text=Format(
            text='{btn_cancel}'
        ),
        id='b_cancel',
        on_click=btn_cancel
    ),
    state=YaDirectLoginsAddRepresentativeSG.PREVIEW,
    getter=representative_getter
)

input_logins_window = Window(
    Format(
        text='{preview_text}'
    ),
    TextInput(
        id="logins",
        type_factory=check_format_list_logins,
        on_error=input_error,
        on_success=input_success
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        id="btn_back",
        state=YaDirectLoginsAddRepresentativeSG.PREVIEW
    ),
    state=YaDirectLoginsAddRepresentativeSG.INPUT_LOGINS,
    getter=input_getter
)

list_logins_window = Window(
    Format(
        text='{preview_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.item.value,
                item_id_getter=itemgetter(1),
                items="logins",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager',
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id='btn_confirm',
        on_click=btn_confirm,
        when='selected'
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        id="btn_back",
        on_click=btn_back,
        state=YaDirectLoginsAddRepresentativeSG.PREVIEW,
    ),
    getter=logins_getter,
    state=YaDirectLoginsAddRepresentativeSG.LIST_LOGINS
)

ya_direct_add_representative_logins_dialog = Dialog(
    preview_window, input_logins_window, list_logins_window
)

ya_direct_add_representative_logins_dialog.callback_query.middleware(AuthorizationMiddleware())
ya_direct_add_representative_logins_dialog.message.middleware(AuthorizationMiddleware())
