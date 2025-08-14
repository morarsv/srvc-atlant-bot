import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            DialogDataConstant as DgDataConst)

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    start_data = dialog_manager.start_data
    comments = start_data[StDataConst.project_comments.value]
    preview_text = i18n.comment.preview() + '\n\n' + i18n.comment.add()

    return {
        'preview_text': preview_text,
        'btn_add_comment': i18n.button.add.comment(),
        'btn_back': i18n.button.back(),
        'comments': comments
    }


async def input_getter(dialog_manager: DialogManager,
                       i18n: TranslatorRunner,
                       event_from_user: User,
                       **kwargs):
    start_data = dialog_manager.start_data
    dialog_data = dialog_manager.dialog_data
    widget_data = dialog_manager.current_context().widget_data

    project_created_at: str = start_data[StDataConst.project_created_at.value]

    input_date = i18n.comment.input.date(date=project_created_at)
    skip = None if dialog_data.get(DgDataConst.finished_key.value) else 1
    input_date = input_date + '\n\n' + i18n.comment.input.err.date() if \
        widget_data.get(WgDataConst.err_input_date.value) else input_date

    return {
        'input_text': i18n.comment.input.text(),
        'input_date': input_date,
        'btn_cancel': i18n.button.cancel(),
        'btn_skip': i18n.button.skip(),
        'skip': skip
    }


async def info_comment_getter(dialog_manager: DialogManager,
                              i18n: TranslatorRunner,
                              event_from_user: User,
                              **kwargs):
    dialog_data = dialog_manager.dialog_data
    widget_data = dialog_manager.current_context().widget_data

    dialog_data[DgDataConst.finished_key.value] = True

    text = widget_data[WgDataConst.comment_text.value]
    date = widget_data[WgDataConst.comment_date.value]
    confirm = 1 if widget_data.get(WgDataConst.status_confirm.value) else None

    return {
        'preview_text': i18n.comment.info(comment=text,
                                          date=date),
        'btn_edit_comment': i18n.button.edit.comment(),
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back(),
        'confirm': confirm
    }
