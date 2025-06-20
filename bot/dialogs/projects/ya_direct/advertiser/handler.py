import logging
import asyncio

from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery
from typing import TYPE_CHECKING
from fluentogram import TranslatorRunner
from aiogram_dialog import DialogManager, ShowMode
from bot.database import query
from bot.database.models import YaDirectLogins, YandexAccesses, Projects
from bot.lexicon.lexicon_ya import LEXICON_SYSTEM_ID
from bot.lexicon.constants.constant import (StartDataConstant as StDataConst,
                                            PoolingConstant as poolConst,
                                            WidgetDataConstant as WgDataConst)
from bot.services.airflow.utils import create_connection_direct, set_active_dag
from bot.services.airflow.dags_generator.dag_func import generate_dag
from bot.utils.bot_func import bot_current_time
from bot.utils.bot_func import alert_msg_to_chat
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner
logger = logging.getLogger(__name__)

_chat_alert_id = LEXICON_TG_BOT['CHAT_ID_ACC_ALERTS']


async def btn_confirm(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    middleware_data = dialog_manager.middleware_data
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    i18n: TranslatorRunner = middleware_data[poolConst.i18n.value]
    project_id = int(start_data[StDataConst.project_id.value])

    ya_accesses: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_DIRECT']
    )

    if not widget_data.get(WgDataConst.item.value):
        await callback.answer(i18n.select.nothing())
    else:
        time = await bot_current_time()

        project: Projects = await query.get_project_by_id(project_id=project_id)

        start_date: str = str(project.created_at)
        project_title: str = project.title
        company_name: str = project.company.company
        list_logins = ''
        request = []
        for login in widget_data[WgDataConst.item.value]:
            login = login.split('/')[1]
            list_logins = list_logins + login + '\n'
            ya_direct: YaDirectLogins = YaDirectLogins()
            ya_direct.project_id = project_id
            ya_direct.direct_login = login
            request.append(query.add_ya_direct_logins(direct_login=ya_direct))
        await asyncio.gather(*request)
        request.clear()
        request = [create_connection_direct(logger=logger,
                                            project_title=project_title,
                                            login=login.split('/')[1],
                                            access_token=ya_accesses.access_token,
                                            project_id=str(project_id),
                                            chat_id=LEXICON_TG_BOT['CHAT_ID_ERR_REPORT'],
                                            i18n=i18n,
                                            callback=callback,
                                            time=time) for login in widget_data[WgDataConst.item.value]]
        await asyncio.gather(*request)
        await alert_msg_to_chat(chat_id=_chat_alert_id,
                                callback=callback,
                                msg=i18n.alert.added.ya.direct.login(
                                    title=project_title,
                                    company=company_name
                                ),
                                logger=logger)
        try:
            await generate_dag(logger=logger,
                               project_title=project_title,
                               project_id=project_id,
                               company_name=company_name,
                               start_date=start_date,
                               callback=callback
                               )
        except Exception as e:
            logger.exception(f"Ошибка при генерации дага на стророне микросервиса: {e}")
        await set_active_dag(logger=logger,
                             company=company_name,
                             project_id=str(project_id),
                             company_id=project.company_id,
                             created_date=start_date,
                             i18n=i18n,
                             callback=callback)
        await callback.answer(i18n.successfully.added())
        await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)
