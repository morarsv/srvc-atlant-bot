import logging

from _operator import itemgetter
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Button, ScrollingGroup, Column, Select
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import AtlantAdministrationSG

from bot.dialogs.atlant_administration.handler import (btn_add_company, btn_add_user, btn_list_companies, btn_back,
                                                       btn_add_user_for_company, btn_switch_to_company,
                                                       btn_switch_to_user, btn_switch_to_project)
from bot.dialogs.atlant_administration.getter import (preview_getter, add_user_getter, list_users_getter,
                                                      list_company_getter, card_company_getter, list_projects_getter)

from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware


logger = logging.getLogger(__name__)


preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    Button(
        text=Format(
            text='{btn_add_company}'
        ),
        id='btn_add_company',
        on_click=btn_add_company
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
            text='{btn_list_company}'
        ),
        id='btn_list_companies',
        on_click=btn_list_companies
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_back',
        on_click=btn_back
    ),
    getter=preview_getter,
    state=AtlantAdministrationSG.PREVIEW
)

add_user_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='companies',
                item_id_getter=itemgetter(1),
                on_click=btn_add_user_for_company
            )
        ),
        width=1,
        height=5,
        id='scroll_add_user'
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_back_from_add_user',
        state=AtlantAdministrationSG.PREVIEW
    ),
    state=AtlantAdministrationSG.ADD_USER,
    getter=add_user_getter
)

list_companies_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='companies',
                item_id_getter=itemgetter(1),
                on_click=btn_switch_to_company
            )
        ),
        width=1,
        height=5,
        id='scroll_list_company'
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_back_from_list_company',
        state=AtlantAdministrationSG.PREVIEW
    ),
    state=AtlantAdministrationSG.LIST_COMPANIES,
    getter=list_company_getter
)

card_company_window = Window(
    Format(
        text='{preview_text}'
    ),
    SwitchTo(
        Format(
            text='{btn_list_users}'
        ),
        id='btn_list_users',
        state=AtlantAdministrationSG.LIST_USERS,
        when='users'
    ),
    SwitchTo(
        Format(
            text='{btn_list_projects}'
        ),
        id='btn_list_projects',
        state=AtlantAdministrationSG.LIST_PROJECTS,
        when='projects'
    ),
    SwitchTo(
        Format(
            text='{btn_back}'
        ),
        id='btn_back_from_card_company',
        state=AtlantAdministrationSG.LIST_COMPANIES
    ),
    state=AtlantAdministrationSG.CARD_COMPANY,
    getter=card_company_getter
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
        id='btn_back_from_list_users',
        state=AtlantAdministrationSG.CARD_COMPANY
    ),
    state=AtlantAdministrationSG.LIST_USERS,
    getter=list_users_getter
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
        id='btn_back_from_list_projects',
        state=AtlantAdministrationSG.CARD_COMPANY
    ),
    state=AtlantAdministrationSG.LIST_PROJECTS,
    getter=list_projects_getter
)

atlant_administration_dialog = Dialog(
    preview_window, add_user_window, list_companies_window, card_company_window,
    list_users_window, list_projects_window
)

atlant_administration_dialog.message.middleware(AuthorizationMiddleware())
atlant_administration_dialog.message.middleware(MessageMonitorMiddleware())
atlant_administration_dialog.callback_query.middleware(AuthorizationMiddleware())
