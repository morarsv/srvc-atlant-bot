import logging

from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from datetime import datetime
from bot.database.models import ProjectComment
from bot.database import query
from bot.utils.bot_func import send_alert_to_chat
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            DialogDataConstant as DgDataConst)
from bot.services.msvc.generator import func
from bot.state.dialog_state import ProjectCommentSG
from typing import Any

logger = logging.getLogger(__name__)

_chat_alert_id = LEXICON_TG_BOT['CHAT_ID_ACC_ALERTS']


async def btn_switch_to_comment(callback: CallbackQuery,
                                widget: Any,
                                dialog_manager: DialogManager,
                                selected_item: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    comment_id = int(selected_item)
    comment: ProjectComment = await query.get_comment_by_id(comment_id=comment_id)

    widget_data[WgDataConst.comment_text.value] = comment.comment
    widget_data[WgDataConst.comment_date.value] = comment.specified_date
    widget_data[WgDataConst.mode_edit.value] = True
    widget_data[WgDataConst.comment_id.value] = comment_id

    await dialog_manager.switch_to(state=ProjectCommentSG.INFO,
                                   show_mode=ShowMode.EDIT)


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_add_comment(callback: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager) -> None:
    dialog_data = dialog_manager.dialog_data
    dialog_data[DgDataConst.finished_key.value] = False
    await dialog_manager.switch_to(state=ProjectCommentSG.INPUT_DATE,
                                   show_mode=ShowMode.EDIT)


async def btn_next_or_end_text(message: Message,
                               widget: ManagedTextInput,
                               dialog_manager: DialogManager,
                               text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data

    widget_data[WgDataConst.comment_text.value] = text
    widget_data[WgDataConst.status_confirm.value] = True
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')

    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def btn_next_or_end_date(message: Message,
                               widget: ManagedTextInput,
                               dialog_manager: DialogManager,
                               text: str) -> None:
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    widget_data[WgDataConst.status_confirm.value] = True
    project_created_at = start_data[StDataConst.project_created_at.value]
    date = text
    fmt = '%d%m%Y'
    end_ftm = '%d-%m-%Y'

    widget_data[WgDataConst.status_confirm.value] = True

    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')

    try:
        date = date.replace(' ', '')
        date = datetime.strptime(date, fmt)
        project_created_at = datetime.strptime(project_created_at, end_ftm)
        widget_data[WgDataConst.comment_date.value] = date.strftime(end_ftm)
    except ValueError:
        widget_data[WgDataConst.err_input_date.value] = True
        await dialog_manager.switch_to(state=ProjectCommentSG.INPUT_DATE,
                                       show_mode=ShowMode.EDIT)
        return
    if project_created_at > date:
        widget_data[WgDataConst.err_input_date.value] = True
        await dialog_manager.switch_to(state=ProjectCommentSG.INPUT_DATE,
                                       show_mode=ShowMode.EDIT)
    else:
        widget_data[WgDataConst.err_input_date.value] = False
        await dialog_manager.next(show_mode=ShowMode.EDIT)


async def btn_confirm(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    text = widget_data[WgDataConst.comment_text.value]
    date = widget_data[WgDataConst.comment_date.value]
    project_id = int(start_data[StDataConst.project_id.value])
    project_title = start_data[StDataConst.project_title.value]

    if widget_data.get(WgDataConst.mode_edit.value, False):
        comment_id = int(widget_data[WgDataConst.comment_id.value])
        widget_data[WgDataConst.mode_edit.value] = False
        await send_alert_to_chat(text=
                                 f'Project ID: {project_id}\n'
                                 f'Project Title: {project_title}\n'
                                 f'Comment: {text}',
                                 chat_id=_chat_alert_id)
        await query.update_comment_by_id(
            comment_id=comment_id,
            project_id=project_id,
            project_title=project_title,
            comment=text,
            specified_date=date
        )
        await func.edit_comment(logger=logger,
                                comment_id=comment_id)

    else:
        await send_alert_to_chat(text=
                                 f'Project ID: {project_id}\n'
                                 f'Project Title: {project_title}\n'
                                 f'Comment: {text}',
                                 chat_id=_chat_alert_id)
        await query.add_comment(
            project_id=project_id,
            project_title=project_title,
            comment=text,
            specified_date=date
        )
        comment_id: int = await query.get_comment_id_by_comment_and_date(
            comment=text,
            specified_date=date,
            project_id=project_id
        )
        await func.add_comment(
            logger=logger,
            comment_id=comment_id
        )

    list_comments: list[ProjectComment] = await query.get_list_comments_by_project_id(
        project_id=int(project_id)
    )

    comments = [(f'{str(c.specified_date)[:10]} {c.comment[:15]}...', str(c.id)) for c in list_comments]
    start_data[StDataConst.project_comments.value] = comments

    widget_data[WgDataConst.status_confirm.value] = False
    await dialog_manager.switch_to(state=ProjectCommentSG.PREVIEW,
                                   show_mode=ShowMode.EDIT)


async def btn_back_info(callback: CallbackQuery,
                        button: Button,
                        dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.status_confirm.value] = False
