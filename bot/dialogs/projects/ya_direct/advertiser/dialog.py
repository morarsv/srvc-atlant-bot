import logging
from operator import itemgetter
from aiogram_dialog.widgets.kbd import (Button, Column, ScrollingGroup,
                                        Multiselect)
from aiogram_dialog.widgets.text import Format
from aiogram_dialog import Dialog, Window
from bot.state.dialog_state import YaDirectLoginsAddAdvertiserSG
from bot.dialogs.projects.ya_direct.advertiser.handler import btn_confirm, btn_back
from bot.dialogs.projects.ya_direct.advertiser.getter import preview_getter
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst

logger = logging.getLogger(__name__)


ya_direct_add_advertiser_logins_dialog = Dialog(
    Window(
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
            when='logins'
        ),
        Button(
            text=Format('{btn_confirm}'),
            id='btn_confirm',
            on_click=btn_confirm,
            when='selected'
        ),
        Button(
            text=Format(text='{btn_back}'),
            id='b_back',
            on_click=btn_back,
        ),
        getter=preview_getter,
        state=YaDirectLoginsAddAdvertiserSG.PREVIEW
    )
)

ya_direct_add_advertiser_logins_dialog.callback_query.middleware(AuthorizationMiddleware())
ya_direct_add_advertiser_logins_dialog.message.middleware(AuthorizationMiddleware())
ya_direct_add_advertiser_logins_dialog.message.middleware(MessageMonitorMiddleware())
