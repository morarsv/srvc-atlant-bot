import logging

from _operator import itemgetter
from aiogram import F
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select, ScrollingGroup, Column
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import TextInput
from bot.state.dialog_state import ProjectCommentSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.dialogs.projects.comment.getter import preview_getter, input_getter, info_comment_getter
from bot.dialogs.projects.comment.handler import (btn_switch_to_comment, btn_add_comment, btn_back, btn_back_info,
                                                  btn_next_or_end_text, btn_next_or_end_date, btn_confirm)
from bot.lexicon.constants.constant import DialogDataConstant as DgDataConst


logger = logging.getLogger(__name__)

CANCEL_EDIT = SwitchTo(
    text=Format(text='{btn_cancel}'),
    when=F['dialog_data'][DgDataConst.finished_key.value],
    id="cnl_edt",
    state=ProjectCommentSG.INFO,
)

preview_window = Window(
    Format(
        text="{preview_text}"
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='comments',
                item_id_getter=itemgetter(1),
                on_click=btn_switch_to_comment
            )
        ),
        when='comments',
        width=1,
        height=5,
        id='scroll_list_comments',
    ),
    Button(
        text=Format(
            text='{btn_add_comment}'
        ),
        id='b_add_comment',
        on_click=btn_add_comment
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id='b_back',
        on_click=btn_back
    ),
    getter=preview_getter,
    state=ProjectCommentSG.PREVIEW
)

input_date_window = Window(
    Format(
        text="{input_date}"
    ),
    TextInput(
        id='input_date',
        on_success=btn_next_or_end_date
    ),
    CANCEL_EDIT,
    state=ProjectCommentSG.INPUT_DATE,
    getter=input_getter
)

input_text_window = Window(
    Format(
        text="{input_text}"
    ),
    TextInput(
        id='input_text',
        on_success=btn_next_or_end_text
    ),
    state=ProjectCommentSG.INPUT_TEXT,
    getter=input_getter
)

info_comment_window = Window(
    Format(
        text="{preview_text}"
    ),
    SwitchTo(
        text=Format(
            text='{btn_edit_comment}'
        ),
        id='b_edit_comment',
        state=ProjectCommentSG.INPUT_DATE,
        show_mode=ShowMode.EDIT,
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id='b_confirm',
        on_click=btn_confirm,
        when='confirm'
    ),
    SwitchTo(
        text=Format(
            text='{btn_back}'
        ),
        id='b_back_info',
        on_click=btn_back_info,
        state=ProjectCommentSG.PREVIEW,
        show_mode=ShowMode.EDIT,
    ),
    getter=info_comment_getter,
    state=ProjectCommentSG.INFO
)


project_comment_dialog = Dialog(
    preview_window, input_date_window, input_text_window, info_comment_window
)

project_comment_dialog.message.middleware(AuthorizationMiddleware())
project_comment_dialog.callback_query.middleware(AuthorizationMiddleware())
