import logging
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import HelpSG
from bot.dialogs.help.getter import main_getter
from bot.dialogs.help.handler import btn_help, submit_application

logger = logging.getLogger(__name__)

help_dialog = Dialog(
    Window(
        Format(
            text='{help}'
        ),
        Button(
            text=Format(
                text='{btn_help}'
            ),
            id='b_help',
            on_click=btn_help
        ),
        state=HelpSG.MAIN,
    ),
    Window(
        Format(
            text='{input_request}'
        ),
        TextInput(
            id="LOGIN",
            on_success=submit_application
        ),
        state=HelpSG.REQUEST,
    ),
    getter=main_getter,
)
