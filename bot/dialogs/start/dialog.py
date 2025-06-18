import logging
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import WebApp, Button
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import StartSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.dialogs.start.getter import preview_getter
from bot.dialogs.start.handler import btn_to_atlant_administrator, btn_to_administrator, btn_to_project, btn_to_viewers

logger = logging.getLogger(__name__)

start_dialog = Dialog(
    Window(
        Format(
            text='{hello_user}'
        ),
        Format(
            text='\n{description_start}',
        ),
        WebApp(
            text=Format(
                text='{btn_report_company}'
            ),
            url=Format(
                text='{report_url}'
            ),
            when='report'
        ),
        Button(
            text=Format(
                text='{btn_to_atlant_administrator}'
            ),
            id='btn_to_atlant_administrator',
            when='atlant_administrator',
            on_click=btn_to_atlant_administrator
        ),
        Button(
            text=Format(
                text='{btn_to_administrator}'
            ),
            id='btn_to_administrator',
            when='administrator',
            on_click=btn_to_administrator

        ),
        Button(
            text=Format(
                text='{btn_to_viewers}'
            ),
            id='btn_to_viewers',
            when='viewer',
            on_click=btn_to_viewers
        ),
        Button(
            text=Format(
                text='{btn_to_project}'
            ),
            id='btn_to_project',
            on_click=btn_to_project
        ),
        state=StartSG.PREVIEW,
        getter=preview_getter,
    ),
)


start_dialog.callback_query.middleware(AuthorizationMiddleware())
start_dialog.message.middleware(AuthorizationMiddleware())
start_dialog.message.middleware(MessageMonitorMiddleware())
