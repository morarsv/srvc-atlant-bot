import logging

from _operator import itemgetter
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select, ScrollingGroup, Column, Multiselect
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import CompanyAdminProjectsSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.dialogs.company_administration.project.getter import (preview_getter, list_ya_counters_getter,
                                                               ya_counter_getter, list_available_managers_getter,
                                                               list_connected_managers_getter)
from bot.dialogs.company_administration.project.handler import (btn_switch_to_ya_counter, btn_back, btn_confirm_set,
                                                                btn_confirm_remove, btn_back_from_managers,
                                                                btn_ya_list_counters)
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst


logger = logging.getLogger(__name__)

preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    Button(
        text=Format(
            text='{btn_ya_list_counters}'
        ),
        id='btn_ya_list_counters',
        when='ya_counters',
        on_click=btn_ya_list_counters
    ),
    SwitchTo(
        text=Format(
            text='{btn_set_managers}'
        ),
        id='btn_set_managers',
        when='available_managers',
        state=CompanyAdminProjectsSG.LIST_AVAILABLE_MANAGERS
    ),
    SwitchTo(
        text=Format(
            text='{btn_remove_managers}'
        ),
        id='btn_remove_managers',
        when='connected_managers',
        state=CompanyAdminProjectsSG.LIST_CONNECTED_MANAGERS
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_back',
        on_click=btn_back
    ),
    getter=preview_getter,
    state=CompanyAdminProjectsSG.PREVIEW
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
                on_click=btn_switch_to_ya_counter
            )
        ),
        width=1,
        height=5,
        id='scroll_list_ya_counters',
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        state=CompanyAdminProjectsSG.PREVIEW,
        id='btn_back_lc',
        show_mode=ShowMode.EDIT
    ),
    state=CompanyAdminProjectsSG.LIST_YA_COUNTERS,
    getter=list_ya_counters_getter
)

ya_counter_window = Window(
    Format(
        text='{preview_text}'
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        state=CompanyAdminProjectsSG.LIST_YA_COUNTERS,
        id='btn_back_c',
        show_mode=ShowMode.EDIT
    ),
    state=CompanyAdminProjectsSG.YA_COUNTER,
    getter=ya_counter_getter
)

list_available_managers_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.selected_manager_set_to_project.value,
                item_id_getter=itemgetter(1),
                items="managers",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager_set',
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id='btn_confirm_s',
        on_click=btn_confirm_set,
        when='selected'
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        state=CompanyAdminProjectsSG.PREVIEW,
        id='btn_back_s',
        on_click=btn_back_from_managers,
        show_mode=ShowMode.EDIT
    ),
    state=CompanyAdminProjectsSG.LIST_AVAILABLE_MANAGERS,
    getter=list_available_managers_getter
)

list_connected_managers_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.selected_manager_remove_from_project.value,
                item_id_getter=itemgetter(1),
                items="managers",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager_remove',
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id='btn_confirm_r',
        on_click=btn_confirm_remove,
        when='selected'
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        state=CompanyAdminProjectsSG.PREVIEW,
        id='btn_back_r',
        on_click=btn_back_from_managers,
        show_mode=ShowMode.EDIT
    ),
    state=CompanyAdminProjectsSG.LIST_CONNECTED_MANAGERS,
    getter=list_connected_managers_getter
)

company_admin_project_dialog = Dialog(
    preview_window, list_ya_counters_window, list_available_managers_window, list_connected_managers_window,
    ya_counter_window
)

company_admin_project_dialog.callback_query.middleware(AuthorizationMiddleware())
company_admin_project_dialog.message.middleware(AuthorizationMiddleware())
company_admin_project_dialog.message.middleware(MessageMonitorMiddleware())
