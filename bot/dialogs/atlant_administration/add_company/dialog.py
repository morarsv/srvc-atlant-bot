import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import AtlantAdministrationAddCompanySG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.utils.type_factory import check_format_company
from bot.dialogs.atlant_administration.add_company.handler import (err_format_company, next_or_end_company,
                                                                   add_user_from_company, btn_confirm, btn_back)
from bot.dialogs.atlant_administration.add_company.getter import input_company_getter, preview_getter


logger = logging.getLogger(__name__)


input_window = Window(
    Format(
        text='{preview_text}'
    ),
    TextInput(
        id='company_name',
        type_factory=check_format_company,
        on_error=err_format_company,
        on_success=next_or_end_company
    ),
    state=AtlantAdministrationAddCompanySG.INPUT_COMPANY,
    getter=input_company_getter
)

card_company_window = Window(
    Format(
        text='{preview_text}'
    ),
    SwitchTo(
        text=Format(
            text='{btn_edit_company}'
        ),
        id="b_edit_company",
        state=AtlantAdministrationAddCompanySG.INPUT_COMPANY,
    ),
    Button(
        text=Format(
            text='{btn_add_user}'
        ),
        id="b_add_user",
        on_click=add_user_from_company,
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id="b_confirm",
        on_click=btn_confirm,
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id="b_back",
        on_click=btn_back
    ),
    getter=preview_getter,
    state=AtlantAdministrationAddCompanySG.PREVIEW
)

atlant_administration_add_company_dialog = Dialog(
    input_window, card_company_window
)

atlant_administration_add_company_dialog.message.middleware(AuthorizationMiddleware())
atlant_administration_add_company_dialog.callback_query.middleware(AuthorizationMiddleware())
