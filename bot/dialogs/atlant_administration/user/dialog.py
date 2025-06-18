import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import AtlantAdministrationUserSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.dialogs.atlant_administration.user.handler import btn_edit, btn_back
from bot.dialogs.atlant_administration.user.getter import preview_getter


logger = logging.getLogger(__name__)

preview_window = Window(
    Format(text='{preview_text}'),
    Button(
        text=Format(
            text='{btn_edit}'
        ),
        id='btn_edit',
        on_click=btn_edit
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_back',
        on_click=btn_back
    ),
    state=AtlantAdministrationUserSG.PREVIEW,
    getter=preview_getter
)

atlant_administration_user_dialog = Dialog(
    preview_window
)

atlant_administration_user_dialog.message.middleware(AuthorizationMiddleware())
atlant_administration_user_dialog.message.middleware(MessageMonitorMiddleware())
atlant_administration_user_dialog.callback_query.middleware(AuthorizationMiddleware())
