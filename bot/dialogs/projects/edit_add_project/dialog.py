import logging

from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Next
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import ProjectsEditAddSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.dialogs.projects.edit_add_project.getter import preview_getter, input_getter
from bot.dialogs.projects.edit_add_project.handler import (err_format_title, btn_next_or_end_title,
                                                           btn_next_or_end_description, btn_confirm, btn_cancel,
                                                           btn_delete)
from bot.lexicon.constants.constant import DialogDataConstant as DgDataConst
from bot.utils.type_factory import check_format_title

logger = logging.getLogger(__name__)

CANCEL_EDIT = SwitchTo(
    text=Format(text='{btn_cancel}'),
    when=F['dialog_data'][DgDataConst.finished_key.value],
    id="cnl_edt",
    state=ProjectsEditAddSG.PREVIEW,
)

SKIP_DESCRIPTION = Next(
    text=Format(text='{btn_skip}'),
    when='skip',
)

input_title_window = Window(
    Format(
        text="{input_title}"
    ),
    TextInput(
        id='input_title',
        type_factory=check_format_title,
        on_error=err_format_title,
        on_success=btn_next_or_end_title
    ),
    CANCEL_EDIT,
    state=ProjectsEditAddSG.INPUT_TITLE,
    getter=input_getter
)

input_description_window = Window(
    Format(
        text='{input_description}'
    ),
    TextInput(
        id='input_description',
        on_success=btn_next_or_end_description
    ),
    SKIP_DESCRIPTION,
    CANCEL_EDIT,
    state=ProjectsEditAddSG.INPUT_DESCRIPTION,
    getter=input_getter
)

preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    SwitchTo(
        text=Format(
            text='{btn_edit_title}'
        ),
        id='btn_edit_title',
        state=ProjectsEditAddSG.INPUT_TITLE
    ),
    SwitchTo(
        text=Format(
            text='{btn_edit_description}'
        ),
        id='btn_edit_description',
        state=ProjectsEditAddSG.INPUT_DESCRIPTION
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id='btn_confirm',
        on_click=btn_confirm,
        when='confirm'
    ),
    Button(
        text=Format(
            text='{btn_delete}'
        ),
        id='btn_delete',
        on_click=btn_delete,
        when='delete'
    ),
    Button(
        text=Format(
            text='{btn_cancel}'
        ),
        id='btn_cancel',
        on_click=btn_cancel,
    ),
    state=ProjectsEditAddSG.PREVIEW,
    getter=preview_getter
)

project_edit_add_dialog = Dialog(
    input_title_window, input_description_window, preview_window
)

project_edit_add_dialog.message.middleware(AuthorizationMiddleware())
project_edit_add_dialog.callback_query.middleware(AuthorizationMiddleware())
