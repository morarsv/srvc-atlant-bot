import logging
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import WebApp, Button, SwitchTo, Back, Url
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import StartSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.dialogs.start.getter import preview_getter, attention_project_getter, company_report_getter
from bot.dialogs.start.handler import btn_to_atlant_administrator, btn_to_administrator, btn_to_project, btn_to_viewers

logger = logging.getLogger(__name__)

start_window = Window(
    Format(
        text='{hello_user}'
    ),
    Format(
        text='\n{description_start}',
    ),
    SwitchTo(
        text=Format(
            text='{btn_report_company}'
        ),
        id='btn_report_company',
        state=StartSG.COMPANY_REPORT,
        when='report'
    ),
    SwitchTo(
        text=Format(
            text='{btn_attention}'
        ),
        id='btn_attention',
        when='attention_project',
        state=StartSG.ATTENTION_PROJECT
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
)

attention_window = Window(
    Format(
        text='{preview_text}'
    ),
    Back(
        text=Format(
            text='{btn_back}'
        ),
    ),
    state=StartSG.ATTENTION_PROJECT,
    getter=attention_project_getter,
)

report_window = Window(
    Format(
        text='{preview_text}'
    ),
    Url(
        text=Format(text='{btn_link_url}'),
        url=Format(text='{link_url}'),
        when='link_url'
    ),
    WebApp(
        text=Format(
            text='{btn_web_url}'
        ),
        url=Format(
            text='{web_url}'
        ),
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_back',
        state=StartSG.PREVIEW
    ),
    state=StartSG.COMPANY_REPORT,
    getter=company_report_getter,
)
start_dialog = Dialog(
    start_window, attention_window, report_window
)


start_dialog.callback_query.middleware(AuthorizationMiddleware())
start_dialog.message.middleware(AuthorizationMiddleware())
start_dialog.message.middleware(MessageMonitorMiddleware())
