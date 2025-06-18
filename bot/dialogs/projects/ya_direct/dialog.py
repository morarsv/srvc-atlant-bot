import logging

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format
from aiogram_dialog import Dialog, Window
from bot.state.dialog_state import YaDirectLoginsAddSG
from bot.dialogs.projects.ya_direct.handler import (btn_agency, btn_back,
                                                    btn_advertiser, btn_representative)
from bot.dialogs.projects.ya_direct.getter import preview_getter
from bot.middlewares.authorization_monitor import AuthorizationMiddleware

logger = logging.getLogger(__name__)


ya_direct_add_logins_dialog = Dialog(
    Window(
        Format(
            text='{preview_text}',
        ),
        Button(
            text=Format(
                text='{btn_agency}'
            ),
            id='b_agency',
            on_click=btn_agency
        ),
        Button(
            text=Format(
                text='{btn_advertiser}'
            ),
            id='b_advertiser',
            on_click=btn_advertiser
        ),
        Button(
            text=Format(
                text='{btn_representative}'
            ),
            id='btn_representative',
            on_click=btn_representative
        ),
        Button(
            text=Format(
                text='{btn_back}'
            ),
            id='btn_back',
            on_click=btn_back,
        ),
        getter=preview_getter,
        state=YaDirectLoginsAddSG.PREVIEW
    )
)

ya_direct_add_logins_dialog.callback_query.middleware(AuthorizationMiddleware())
ya_direct_add_logins_dialog.message.middleware(AuthorizationMiddleware())
