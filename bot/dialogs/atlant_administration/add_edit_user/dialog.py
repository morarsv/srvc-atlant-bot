import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button
from aiogram_dialog.widgets.text import Format
from aiogram import F
from bot.state.dialog_state import AtlantAdministrationEditAddUserSG
from bot.dialogs.atlant_administration.add_edit_user.handler import (btn_next_or_end, error_login,
                                                                     btn_next_or_end_login,
                                                                     error_password, btn_confirm, btn_back)
from bot.dialogs.atlant_administration.add_edit_user.getter import input_getter, card_user_getter
from bot.utils.type_factory import check_format_login, check_format_password
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst, DialogDataConstant as DgDataConst

logger = logging.getLogger(__name__)


CANCEL_EDIT = SwitchTo(
    Format(text='{btn_cancel}'),
    when=F['dialog_data'][DgDataConst.finished_key.value],
    id="cnl_edt",
    state=AtlantAdministrationEditAddUserSG.PREVIEW,
)

input_username_window = Window(
    Format(
        text='{input_username}'
    ),
    TextInput(
        id=WgDataConst.username.value,
        on_success=btn_next_or_end
    ),
    CANCEL_EDIT,
    state=AtlantAdministrationEditAddUserSG.INPUT_USERNAME,
    getter=input_getter,
)

input_login_window = Window(
    Format(
        text='{input_login}'
    ),
    TextInput(
        id=WgDataConst.user_login.value,
        type_factory=check_format_login,
        on_error=error_login,
        on_success=btn_next_or_end_login
    ),
    CANCEL_EDIT,
    state=AtlantAdministrationEditAddUserSG.INPUT_LOGIN,
    getter=input_getter
)

input_password_window = Window(
    Format(
        text='{input_password}'
    ),
    TextInput(
        id=WgDataConst.user_password.value,
        type_factory=check_format_password,
        on_error=error_password,
        on_success=btn_next_or_end
    ),
    CANCEL_EDIT,
    state=AtlantAdministrationEditAddUserSG.INPUT_PASSWORD,
    getter=input_getter
)

card_user_window = Window(
    Format(
        text='{preview_text}'
    ),
    SwitchTo(
        Format(
            text='{btn_edit_username}'
        ),
        state=AtlantAdministrationEditAddUserSG.INPUT_USERNAME,
        id="to_username",
    ),
    SwitchTo(
        Format(
            text='{btn_edit_password}'
        ),
        state=AtlantAdministrationEditAddUserSG.INPUT_PASSWORD,
        id="to_password",
    ),
    Button(
        Format(
            text='{btn_confirm}'
        ),
        when='confirm',
        id="btn_confirm",
        on_click=btn_confirm,
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id="btn_back",
        on_click=btn_back
    ),
    state=AtlantAdministrationEditAddUserSG.PREVIEW,
    getter=card_user_getter
)

atlant_administration_add_edit_user_dialog = Dialog(
    input_username_window, input_login_window, input_password_window, card_user_window
)

atlant_administration_add_edit_user_dialog.message.middleware(AuthorizationMiddleware())
atlant_administration_add_edit_user_dialog.callback_query.middleware(AuthorizationMiddleware())
