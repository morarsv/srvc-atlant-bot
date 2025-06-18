import logging
from _operator import itemgetter
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select, ScrollingGroup, Column
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import CompanyAdminSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.dialogs.company_administration.getter import preview_getter, list_users_getter, list_projects_getter
from bot.dialogs.company_administration.handler import (btn_switch_to_user, btn_switch_to_project, btn_back,
                                                        btn_add_user, btn_logout_frm_sessions)

logger = logging.getLogger(__name__)

preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    Button(
        text=Format(
            text='{btn_add_user}'
        ),
        id='btn_add_user',
        on_click=btn_add_user
    ),
    SwitchTo(
        text=Format(
            text='{btn_list_projects}'
        ),
        id='btn_list_projects',
        when='projects',
        state=CompanyAdminSG.LIST_PROJECTS
    ),
    SwitchTo(
        text=Format(
            text='{btn_list_users}'
        ),
        id='btn_list_users',
        when='users',
        state=CompanyAdminSG.LIST_USERS
    ),
    Button(
        text=Format(
            text='{btn_logout_from_sessions}'
        ),
        id='btn_logout_from_sessions',
        on_click=btn_logout_frm_sessions
    ),
    Button(
        text=Format(
                text='{btn_back}'
        ),
        id='btn_back',
        on_click=btn_back
    ),
    getter=preview_getter,
    state=CompanyAdminSG.PREVIEW
)

list_projects_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='projects',
                item_id_getter=itemgetter(1),
                on_click=btn_switch_to_project
            )
        ),
        width=1,
        height=5,
        id='scroll_list_projects',
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        state=CompanyAdminSG.PREVIEW,
        id='btn_back_p',
        show_mode=ShowMode.EDIT
    ),
    state=CompanyAdminSG.LIST_PROJECTS,
    getter=list_projects_getter
)

list_users_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='users',
                item_id_getter=itemgetter(1),
                on_click=btn_switch_to_user
            )
        ),
        width=1,
        height=5,
        id='scroll_list_users',
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        state=CompanyAdminSG.PREVIEW,
        id='btn_back_p',
        show_mode=ShowMode.EDIT
    ),
    state=CompanyAdminSG.LIST_USERS,
    getter=list_users_getter
)

company_admin_dialog = Dialog(
    preview_window, list_projects_window, list_users_window
)

company_admin_dialog.callback_query.middleware(AuthorizationMiddleware())
company_admin_dialog.message.middleware(AuthorizationMiddleware())
company_admin_dialog.message.middleware(MessageMonitorMiddleware())
