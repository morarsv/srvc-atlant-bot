import logging
from _operator import itemgetter

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (ScrollingGroup, Button, Back,
                                        Column, Select, Multiselect)
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import ViewersSG
from bot.dialogs.viewers.getter import preview_getter, list_viewers_getter, info_viewer_getter, list_projects_getter
from bot.dialogs.viewers.handler import (btn_list_viewers, btn_add_user, btn_delete_viewer, btn_back,
                                         btn_remove_project, btn_switch_to_viewer, btn_set_project, btn_confirm,
                                         back_from_projects)
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst

logger = logging.getLogger(__name__)

preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    Button(
        text=Format(
            text='{btn_list_viewers}'
        ),
        id='btn_list_viewers',
        when='viewers',
        on_click=btn_list_viewers
    ),
    Button(
        text=Format(
            text='{btn_add_user}'
        ),
        id='btn_add_user',
        on_click=btn_add_user
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id='button_back',
        on_click=btn_back
    ),
    getter=preview_getter,
    state=ViewersSG.PREVIEW
)

list_viewers_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='viewers',
                item_id_getter=itemgetter(1),
                on_click=btn_switch_to_viewer
            )
        ),
        width=1,
        height=5,
        id='scroll'
    ),
    Back(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_back'
    ),
    getter=list_viewers_getter,
    state=ViewersSG.LIST_VIEWERS
)

info_viewer_window = Window(
    Format(
        text='{preview_text}'
    ),
    Button(
        text=Format(
            text='{btn_delete_viewer}'
        ),
        id='btn_delete_viewer',
        on_click=btn_delete_viewer
    ),
    Button(
        text=Format(
            text='{btn_set_project}'
        ),
        id='btn_set_project',
        on_click=btn_set_project,
        when='set_project'
    ),
    Button(
        text=Format(
            text='{btn_remove_project}'
        ),
        id='btn_remove_project',
        on_click=btn_remove_project,
        when='remove_project'
    ),
    Back(
        text=Format(
            text='{btn_back}'
        ),
    ),
    getter=info_viewer_getter,
    state=ViewersSG.INFO_VIEWER
)

list_projects_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.projects_id.value,
                item_id_getter=itemgetter(1),
                items='projects',
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
    Back(
        text=Format(
            text='{btn_back}'
        ),
        on_click=back_from_projects
    ),
    getter=list_projects_getter,
    state=ViewersSG.LIST_PROJECTS
)

viewers_dialog = Dialog(
    preview_window, list_viewers_window, info_viewer_window, list_projects_window
)

viewers_dialog.callback_query.middleware(AuthorizationMiddleware())
viewers_dialog.message.middleware(AuthorizationMiddleware())
viewers_dialog.message.middleware(MessageMonitorMiddleware())
