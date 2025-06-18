import logging
from operator import itemgetter
from aiogram_dialog.widgets.kbd import (Button, Column, ScrollingGroup,
                                        Multiselect, SwitchTo)
from aiogram_dialog.widgets.text import Format
from aiogram_dialog import Dialog, Window
from bot.state.dialog_state import YaDirectLoginsSettingsSG
from bot.dialogs.projects.ya_direct.settings.handler import (btn_activate_confirm, btn_cancel, btn_back,
                                                             btn_deactivate_confirm)
from bot.dialogs.projects.ya_direct.settings.getter import (preview_getter, logins_activate_getter,
                                                            logins_deactivate_getter)
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst

logger = logging.getLogger(__name__)


preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    SwitchTo(
        text=Format(
            text='{btn_activate}'
        ),
        id='b_activate',
        state=YaDirectLoginsSettingsSG.ACTIVATE,
        when='activate'
    ),
    SwitchTo(
        text=Format(
            text='{btn_deactivate}'
        ),
        id='b_deactivate',
        state=YaDirectLoginsSettingsSG.DEACTIVATE,
        when='inactive'
    ),
    Button(
        text=Format(
            text='{btn_cancel}'
        ),
        id='b_cancel',
        on_click=btn_cancel
    ),
    getter=preview_getter,
    state=YaDirectLoginsSettingsSG.PREVIEW,

)

activate_window = Window(
    Format(
        text='{logins_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.project_ya_activated_logins.value,
                item_id_getter=itemgetter(1),
                items="logins",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager_activate',
        when='logins'
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id='b_confirm',
        on_click=btn_activate_confirm,
        when='selected'
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        id='b_back',
        on_click=btn_back,
        state=YaDirectLoginsSettingsSG.PREVIEW,
    ),
    getter=logins_activate_getter,
    state=YaDirectLoginsSettingsSG.ACTIVATE
)

deactivate_window = Window(
    Format(
        text='{logins_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.project_ya_deactivated_logins.value,
                item_id_getter=itemgetter(1),
                items="logins",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager_deactivate',
        when='logins'
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id='btn_confirm',
        on_click=btn_deactivate_confirm,
        when='selected'
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        id='b_back',
        on_click=btn_back,
        state=YaDirectLoginsSettingsSG.PREVIEW,
    ),
    getter=logins_deactivate_getter,
    state=YaDirectLoginsSettingsSG.DEACTIVATE
)

ya_direct_settings_logins_dialog = Dialog(
    preview_window, activate_window, deactivate_window
)

ya_direct_settings_logins_dialog.callback_query.middleware(AuthorizationMiddleware())
ya_direct_settings_logins_dialog.message.middleware(AuthorizationMiddleware())
ya_direct_settings_logins_dialog.message.middleware(MessageMonitorMiddleware())
