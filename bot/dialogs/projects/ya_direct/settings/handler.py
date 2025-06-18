import logging
import asyncio

from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery
from typing import TYPE_CHECKING
from fluentogram import TranslatorRunner
from aiogram_dialog import DialogManager, ShowMode
from bot.database import query
from bot.database.models import Projects
from bot.services.airflow.dags_generator.dag_func import generate_dag
from bot.lexicon.constants.constant import (StartDataConstant as StDataConst,
                                            WidgetDataConstant as WgDataConst,
                                            PoolingConstant as pooConst)
from bot.services.airflow.utils import set_active_dag
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.utils.bot_func import alert_msg_to_chat

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)
_chat_alert_id = LEXICON_TG_BOT['CHAT_ID_ACC_ALERTS']


async def btn_cancel(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.project_ya_deactivated_logins.value] = []
    widget_data[WgDataConst.project_ya_activated_logins.value] = []


async def btn_activate_confirm(callback: CallbackQuery,
                               button: Button,
                               dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    project_id = start_data[StDataConst.project_id.value]
    project: Projects = await query.get_project_by_id(project_id=project_id)

    project_title = project.title
    start_date: str = str(project.created_at)
    company_name: str = project.company.company
    company_id: int = project.company_id

    i18n: TranslatorRunner = middleware_data[pooConst.i18n.value]

    logins_id = widget_data[WgDataConst.project_ya_activated_logins.value]
    request = [query.set_ya_direct_login_status(l_id=int(login_id), status=True) for login_id in logins_id]
    await asyncio.gather(*request)

    await callback.answer(i18n.successfully.updated())
    await alert_msg_to_chat(chat_id=_chat_alert_id,
                            callback=callback,
                            msg=i18n.alert.edited.ya.direct.logins.activated(
                                title=project_title,
                                company=company_name,
                            ),
                            logger=logger)
    try:
        await generate_dag(logger=logger,
                           project_title=project_title,
                           project_id=project_id,
                           company_name=company_name,
                           start_date=start_date,
                           callback=callback)
    except Exception as e:
        logger.exception(f"Ошибка при генерации дага на стророне микросервиса: {e}")
    await set_active_dag(logger=logger,
                         company=company_name,
                         project_id=str(project_id),
                         company_id=str(company_id),
                         created_date=start_date,
                         i18n=i18n,
                         callback=callback)
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_deactivate_confirm(callback: CallbackQuery,
                                 button: Button,
                                 dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    project_id = start_data[StDataConst.project_id.value]
    project: Projects = await query.get_project_by_id(project_id=project_id)

    project_title = project.title
    start_date: str = str(project.created_at)
    company_name: str = project.company.company
    company_id: int = project.company_id

    i18n: TranslatorRunner = middleware_data[pooConst.i18n.value]

    logins_id = widget_data[WgDataConst.project_ya_deactivated_logins.value]

    request = [query.set_ya_direct_login_status(l_id=int(login_id), status=False) for login_id in logins_id]
    await asyncio.gather(*request)

    await callback.answer(i18n.successfully.updated())
    await alert_msg_to_chat(chat_id=_chat_alert_id,
                            callback=callback,
                            msg=i18n.alert.edited.ya.direct.logins.deactivated(
                                title=project_title,
                                company=company_name,
                            ),
                            logger=logger)
    try:
        await generate_dag(logger=logger,
                           project_title=project_title,
                           project_id=project_id,
                           company_name=company_name,
                           start_date=start_date,
                           callback=callback)
    except Exception as e:
        logger.exception(f"Ошибка при генерации дага на стророне микросервиса: {e}")
    try:
        await set_active_dag(logger=logger,
                             company=company_name,
                             project_id=str(project_id),
                             company_id=str(company_id),
                             created_date=start_date,
                             i18n=i18n,
                             callback=callback)
    except Exception as e:
        logger.exception('Ошибка при активации дага')
    await dialog_manager.done(show_mode=ShowMode.EDIT)
