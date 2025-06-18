import logging
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button
from aiogram_dialog.widgets.text import Format
from bot.lexicon.constants.constant import DialogDataConstant as dialogConst
from bot.state.dialog_state import AuthorizationSG
from bot.dialogs.authorization.handler import success_input_password, success_input_login, btn_logout
from bot.dialogs.authorization.getter import preview_getter, input_getter, fail_getter

logger = logging.getLogger(__name__)


preview = Window(
    Format(text='{menu_text}'),
    SwitchTo(
        text=Format(text='{btn_login}'),
        id='b_login',
        state=AuthorizationSG.INPUT_LOGIN,
        when='unauthorized'
    ),
    Button(
        text=Format(text='{btn_logout}'),
        id='b_logout',
        on_click=btn_logout,
        when='authorized'
    ),
    state=AuthorizationSG.PREVIEW,
    getter=preview_getter
)

input_login = Window(
    Format(text='{input_login}'),
    TextInput(
        id=dialogConst.input_login.value,
        on_success=success_input_login
    ),
    state=AuthorizationSG.INPUT_LOGIN,
    getter=input_getter
)


input_password = Window(
    Format(text='{input_password}'),
    TextInput(
        id=dialogConst.input_password.value,
        on_success=success_input_password
    ),
    state=AuthorizationSG.INPUT_PASSWORD,
    getter=input_getter
)

fail_authorize = Window(
    Format(text='{menu_text}'),
    SwitchTo(
        text=Format(text='{btn_login}'),
        id='b_login',
        state=AuthorizationSG.INPUT_LOGIN
    ),
    state=AuthorizationSG.FAIL,
    getter=fail_getter
)


authorization_dialog = Dialog(
    preview, input_login, input_password, fail_authorize
)
