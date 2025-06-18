import logging

from _operator import itemgetter
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Select, ScrollingGroup, Column, Back
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import AtlantAdministrationProjectSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.dialogs.atlant_administration.project.handler import btn_back, btn_switch_to_counter, btn_counters_list
from bot.dialogs.atlant_administration.project.getter import preview_getter, list_counters_getter, counter_getter


logger = logging.getLogger(__name__)


preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    Button(
        text=Format(
            text='{btn_counters_list}'
        ),
        when='counters',
        id='btn_counters_list',
        on_click=btn_counters_list
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_back',
        on_click=btn_back
    ),
    getter=preview_getter,
    state=AtlantAdministrationProjectSG.PREVIEW
)

list_ya_counters_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='counters',
                item_id_getter=itemgetter(1),
                on_click=btn_switch_to_counter
            )
        ),
        width=1,
        height=5,
        id='scroll_list_counters',
    ),
    Back(
        text=Format(
            text='{btn_back}'
        ),
    ),
    getter=list_counters_getter,
    state=AtlantAdministrationProjectSG.LIST_COUNTRIES
)

counter_window = Window(
    Format(
        text='{preview_text}'
    ),
    Back(
        text=Format(
            text='{btn_back}'
        ),
    ),
    getter=counter_getter,
    state=AtlantAdministrationProjectSG.COUNTER
)

atlant_administration_project_dialog = Dialog(
    preview_window, list_ya_counters_window, counter_window
)

atlant_administration_project_dialog.message.middleware(AuthorizationMiddleware())
atlant_administration_project_dialog.message.middleware(MessageMonitorMiddleware())
atlant_administration_project_dialog.callback_query.middleware(AuthorizationMiddleware())
