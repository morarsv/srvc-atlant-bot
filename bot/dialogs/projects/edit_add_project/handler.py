import asyncio
import logging

from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from bot.database.models import Projects
from bot.database import query
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            PoolingConstant as poolConst,
                                            DialogDataConstant as DgDataConst)
from bot.utils.bot_func import bot_current_time, alert_msg_to_chat, get_session_data
from bot.services.web_reports.utils import web_add_project, web_update_project, web_delete_project
from bot.services.msvc.generator import func
from bot.state.dialog_state import StartSG, ProjectsEditAddSG
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from fluentogram import TranslatorRunner
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)

_chat_alert_id = LEXICON_TG_BOT['CHAT_ID_ACC_ALERTS']


async def err_format_title(message: Message,
                           widget: ManagedTextInput,
                           dialog_manager: DialogManager,
                           error: ValueError) -> None:
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    await dialog_manager.switch_to(state=ProjectsEditAddSG.INPUT_TITLE, show_mode=ShowMode.EDIT)


async def btn_next_or_end_title(message: Message,
                                widget: ManagedTextInput,
                                dialog_manager: DialogManager,
                                text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    dialog_data = dialog_manager.dialog_data

    widget_data[WgDataConst.status_confirm.value] = 1
    widget_data[WgDataConst.project_title.value] = text
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')

    if dialog_data.get(DgDataConst.finished_key.value, False):
        await dialog_manager.switch_to(state=ProjectsEditAddSG.PREVIEW, show_mode=ShowMode.EDIT)
    else:
        await dialog_manager.next(show_mode=ShowMode.EDIT)


async def btn_next_or_end_description(message: Message,
                                      widget: ManagedTextInput,
                                      dialog_manager: DialogManager,
                                      text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    dialog_data = dialog_manager.dialog_data

    widget_data[WgDataConst.status_confirm.value] = 1
    widget_data[WgDataConst.project_description.value] = text
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')

    if dialog_data.get(DgDataConst.finished_key.value, False):
        await dialog_manager.switch_to(state=ProjectsEditAddSG.PREVIEW, show_mode=ShowMode.EDIT)
    else:
        await dialog_manager.next(show_mode=ShowMode.EDIT)


async def btn_confirm(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data
    middleware_data = dialog_manager.middleware_data

    i18n: TranslatorRunner = middleware_data[poolConst.i18n.value]
    status_edit = widget_data.get(StDataConst.status_edit.value, False)
    title = widget_data[WgDataConst.project_title.value]
    description = widget_data.get(WgDataConst.project_description.value, ' ')

    time: str = await bot_current_time()
    tg_id = int(callback.from_user.id)
    _, login, _, user_uuid, company_id, company_name = get_session_data(tg_id=tg_id,
                                                                        dialog_manager=dialog_manager)

    if status_edit:
        project_id = int(start_data[StDataConst.project_id.value])
        await web_update_project(
            logger=logger,
            project_id=project_id,
            project_title=title,
            callback=callback
        )
        await query.update_project_by_id(p_id=project_id, title=title, description=description)
        asyncio.create_task(func.generate_dag(logger=logger,
                                              project_title=title,
                                              project_id=project_id,
                                              company_name=company_name,
                                              start_date=time))
        asyncio.create_task(func.generate_dbt_project(
            logger=logger,
            company_id=company_id,
            company_name=company_name
        ))
    else:
        project: Projects = Projects()
        project.title = title
        project.description = description
        project.company_id = company_id
        project.user_login = login
        await query.add_project_and_comment_and_report_and_set_manager(project=project,
                                                                       user_id=user_uuid)
        project: Projects = await query.get_project_by_title_description_and_user_login(
            title=title,
            description=description,
            user_login=login
        )
        logger.info(f'Added project. Title: {project.title}, ID:{project.id}')
        comment_id: int = await query.get_comment_id_by_comment_and_date(comment='First comment',
                                                                         specified_date=str(project.created_at)[:10],
                                                                         project_id=project.id)
        await func.add_comment(
            logger=logger,
            comment_id=comment_id
        )
        await web_add_project(
            logger=logger,
            user_id=str(user_uuid),
            project=project,
            callback=callback
        )
        asyncio.create_task(func.generate_dag(logger=logger,
                                              project_title=title,
                                              project_id=project.id,
                                              company_name=company_name,
                                              start_date=time))
        asyncio.create_task(func.generate_dbt_project(
            logger=logger,
            company_id=company_id,
            company_name=company_name
        ))
        await alert_msg_to_chat(chat_id=_chat_alert_id,
                                msg=i18n.alert.added.project(
                                    title=title,
                                    company=company_name
                                ),
                                logger=logger)
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_cancel(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_delete(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    middleware_data = dialog_manager.middleware_data
    widget_data = dialog_manager.current_context().widget_data
    i18n: TranslatorRunner = middleware_data[poolConst.i18n.value]
    project_id = int(start_data[StDataConst.project_id.value])
    tg_id = int(callback.from_user.id)
    username, _, role_id, _, company_id, company_name = get_session_data(tg_id=tg_id,
                                                                         dialog_manager=dialog_manager)
    await query.delete_project_by_id(p_id=project_id)
    await web_delete_project(
        logger=logger,
        project_id=project_id,
        callback=callback
    )
    asyncio.create_task(func.generate_dbt_project(
        logger=logger,
        company_id=company_id,
        company_name=company_name
    ))
    title = widget_data[WgDataConst.project_title.value]
    logger.info(f'Project deleted. Title {title}, ID: {project_id}')

    await alert_msg_to_chat(chat_id=_chat_alert_id,
                            msg=i18n.alert.deleted.project(
                                title=title,
                                company=company_name
                            ),
                            logger=logger)

    await dialog_manager.start(state=StartSG.PREVIEW,
                               mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.EDIT,
                               data={
                                   StDataConst.username.value: username,
                                   StDataConst.user_role_id.value: role_id
                               })
