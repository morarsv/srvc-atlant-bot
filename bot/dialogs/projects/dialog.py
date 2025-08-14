import logging

from _operator import itemgetter
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.kbd import WebApp, Button, SwitchTo, Select, ScrollingGroup, Column, Back, Row, Group, Url
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import ProjectsSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.dialogs.projects.getter import (preview_getter, list_projects_getter, info_project_getter,
                                         add_service_getter, ya_access_getter, report_project_getter)
from bot.dialogs.projects.handler import (btn_add_project, btn_back, btn_switch_to_project, btn_button_comments,
                                          btn_settings_ya_logins, btn_settings_ya_counters,
                                          btn_edit_project, btn_update_list_project, update_status,
                                          btn_add_ya_logins, btn_add_ya_counters, switch_to_service,
                                          btn_ya_metrika_access, btn_ya_direct_access)

logger = logging.getLogger(__name__)

preview_window = Window(
    Format(
        text="{preview_text}"
    ),
    Row(
        SwitchTo(
            text=Format(
                text="{btn_list_projects}"
            ),
            id='b_list_projects',
            show_mode=ShowMode.EDIT,
            state=ProjectsSG.LIST_PROJECTS,
            on_click=btn_update_list_project,
            when='projects'
        ),
        Button(
            text=Format(
                text='{btn_add_project}'
            ),
            id='b_add_project',
            on_click=btn_add_project,
            when='access'
        ),
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id='b_back',
        on_click=btn_back
    ),
    getter=preview_getter,
    state=ProjectsSG.PREVIEW
)

list_projects_window = Window(
    Format(
        text="{preview_text}"
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
    Back(
        text=Format(
            text='{btn_back}'
        ),
        on_click=btn_update_list_project
    ),
    getter=list_projects_getter,
    state=ProjectsSG.LIST_PROJECTS
)

info_project_window = Window(
    Format(
        text="{preview_text}"
    ),
    SwitchTo(
        text=Format(text='{btn_report_project}'),
        id='btn_report_project',
        state=ProjectsSG.REPORT,
    ),
    Button(
        text=Format(
            text='{btn_button_comments}'
        ),
        id='btn_button_comments',
        on_click=btn_button_comments,
        when='access'
    ),
    Button(
        text=Format(
            text='{btn_settings_ya_logins}'
        ),
        id='btn_settings_ya_logins',
        on_click=btn_settings_ya_logins,
        when='logins'
    ),
    Button(
        text=Format(
            text='{btn_list_ya_counters}'
        ),
        id='btn_settings_ya_counters',
        on_click=btn_settings_ya_counters,
        when='counters'
    ),
    Group(
        Row(
            SwitchTo(
                text=Format(
                    text='{btn_add_service}'
                ),
                id='b_service',
                on_click=switch_to_service,
                state=ProjectsSG.ADD_SERVICE
            ),
            Button(
                text=Format(
                    text='{btn_edit}'
                ),
                id='b_edit',
                on_click=btn_edit_project
            ),
        ),
        when='access'
    ),
    Back(
        text=Format(
            text='{btn_back}'
        ),
        on_click=btn_update_list_project
    ),
    getter=info_project_getter,
    state=ProjectsSG.INFO_PROJECT
)

project_report_window = Window(
    Format(
        text="{preview_text}"
    ),
    Url(
        text=Format(text='{btn_link_url}'),
        url=Format(text='{link_url}'),
        when='link_url'
    ),
    WebApp(
        text=Format(text='{btn_web_url}'),
        url=Format(text='{web_url}')
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_back_r',
        state=ProjectsSG.INFO_PROJECT
    ),
    getter=report_project_getter,
    state=ProjectsSG.REPORT
)

add_service_window = Window(
    Format(
        text='{preview_text}'
    ),
    Button(
        text=Format(
            text='{btn_add_ya_logins}'
        ),
        id='btn_add_ya_logins',
        on_click=btn_add_ya_logins,
        when='direct_in'
    ),
    Button(
        text=Format(
            text='{btn_add_ya_counters}'
        ),
        id='btn_add_ya_counters',
        on_click=btn_add_ya_counters,
        when='metrika_in'
    ),
    Button(
        text=Format(text='{btn_ya_direct_access}'),
        id='btn_ya_direct_access',
        on_click=btn_ya_direct_access
    ),
    Button(
        text=Format(text='{btn_ya_metrika_access}'),
        id='btn_ya_metrika_access',
        on_click=btn_ya_metrika_access
    ),
    Back(
        text=Format(
            text='{btn_back}'
        ),
    ),
    getter=add_service_getter,
    state=ProjectsSG.ADD_SERVICE
)

ya_access_window = Window(
    Format(text='{preview_text}'),
    Url(
        text=Format(text='{btn_open_browser}'),
        url=Format(text='{link}')
    ),
    WebApp(
        text=Format(text='{btn_open_tg_web}'),
        url=Format(text='{link}')
    ),
    Back(
        text=Format(
            text='{btn_back}',
        ),
        on_click=update_status
    ),
    getter=ya_access_getter,
    state=ProjectsSG.YA_ACCESS
)


project_dialog = Dialog(
    preview_window, list_projects_window, info_project_window, add_service_window, ya_access_window,
    project_report_window
)

project_dialog.message.middleware(AuthorizationMiddleware())
project_dialog.message.middleware(MessageMonitorMiddleware())
project_dialog.callback_query.middleware(AuthorizationMiddleware())
