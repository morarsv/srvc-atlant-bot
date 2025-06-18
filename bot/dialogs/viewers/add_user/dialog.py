import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format
from aiogram import F
from bot.state.dialog_state import ViewersAddUserSG
from bot.dialogs.viewers.add_user.getter import preview_getter, input_getter
from bot.dialogs.viewers.add_user.handler import (btn_next_or_end, error_login, error_password,
                                                  btn_next_or_end_login, btn_confirm, btn_back)
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            DialogDataConstant as DgDataConst)
from bot.utils.type_factory import check_format_login, check_format_password

logger = logging.getLogger(__name__)

CANCEL_EDIT = SwitchTo(
    Format(text='{btn_cancel}'),
    when=F['dialog_data'][DgDataConst.finished_key.value],
    id="cnl_edt",
    state=ViewersAddUserSG.PREVIEW,
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
    state=ViewersAddUserSG.INPUT_USERNAME,
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
    state=ViewersAddUserSG.INPUT_LOGIN,
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
    state=ViewersAddUserSG.INPUT_PASSWORD,
    getter=input_getter

)

preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    SwitchTo(
        Format(
            text='{btn_edit_username}'
        ),
        state=ViewersAddUserSG.INPUT_USERNAME,
        id="to_username",
    ),
    SwitchTo(
        Format(
            text='{btn_edit_password}'
        ),
        state=ViewersAddUserSG.INPUT_PASSWORD,
        id="to_password",
    ),
    Button(
        Format(
            text='{btn_confirm}'
        ),
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
    state=ViewersAddUserSG.PREVIEW,
    getter=preview_getter
)

viewers_add_viewer_dialog = Dialog(
    input_username_window, input_login_window,
    input_password_window, preview_window
)

viewers_add_viewer_dialog.message.middleware(AuthorizationMiddleware())
viewers_add_viewer_dialog.callback_query.middleware(AuthorizationMiddleware())
