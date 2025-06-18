import logging
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import ConnectUserSG
from bot.utils.type_factory import check_format_company
from bot.dialogs.connect_user.getter import preview_getter, input_getter
from bot.dialogs.connect_user.handler import btn_authorization, btn_next_or_end, err_format_company, next_or_end_company
from bot.lexicon.constants.constant import DialogDataConstant as dialogConst

logger = logging.getLogger(__name__)

preview = Window(
    Format(
        text='{menu_text}'
    ),
    Button(
        text=Format(
            text='{btn_authorization}'
        ),
        id='btn_authorization',
        on_click=btn_authorization
    ),
    SwitchTo(
        text=Format(
            text='{btn_filled_application}'
        ),
        id='btn_filled_application',
        state=ConnectUserSG.INPUT_USERNAME
    ),

    state=ConnectUserSG.PREVIEW,
    getter=preview_getter,
)


input_username = Window(
    Format(
        text='{input_username}'
    ),
    TextInput(
        id=dialogConst.username.value,
        on_success=btn_next_or_end
    ),
    state=ConnectUserSG.INPUT_USERNAME,
    getter=input_getter,
)

input_company_name = Window(
    Format(
        text='{input_company_name}'
    ),
    TextInput(
        id=dialogConst.company_name.value,
        type_factory=check_format_company,
        on_error=err_format_company,
        on_success=next_or_end_company
    ),
    state=ConnectUserSG.INPUT_COMPANY,
    getter=input_getter
)

application_form = Window(
    Format(text='{menu_text}'),
    state=ConnectUserSG.APPLICATION_FORM,
    getter=input_getter
)

connect_user_dialog = Dialog(
    preview, input_username, input_company_name, application_form
)
