import logging
import asyncio
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram.types import CallbackQuery, Message
from typing import TYPE_CHECKING
from fluentogram import TranslatorRunner
from aiogram_dialog import DialogManager, ShowMode
from bot.database import query
from bot.state.dialog_state import YaDirectLoginsAddRepresentativeSG
from bot.database.models import YaDirectLogins, YandexAccesses, Projects
from bot.services.yandex.utils import check_ya_representative_clients_logins
from bot.services.airflow.utils import create_connection_direct
from bot.services.airflow.dags_generator.dag_func import generate_dag
from bot.lexicon.lexicon_ya import LEXICON_SYSTEM_ID
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.utils.bot_func import bot_current_time
from bot.services.airflow.utils import set_active_dag
from bot.lexicon.constants.constant import (StartDataConstant as StDataConst,
                                            WidgetDataConstant as WgDataConst,
                                            PoolingConstant as poolConst)
from bot.utils.bot_func import alert_msg_to_chat
if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)

_chat_alert_id = LEXICON_TG_BOT['CHAT_ID_ACC_ALERTS']


async def input_error(message: Message,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      error: ValueError) -> None:
    dialog_manager.current_context().widget_data[WgDataConst.err_input_login.value] = True
    await dialog_manager.switch_to(
        state=YaDirectLoginsAddRepresentativeSG.INPUT_LOGINS,
        show_mode=ShowMode.EDIT
    )


async def input_success(message: Message,
                        widget: ManagedTextInput,
                        dialog_manager: DialogManager,
                        text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')

    project_id = int(start_data[StDataConst.project_id.value])

    if widget_data.get(WgDataConst.project_ya_direct_access_token.value, False):
        ya_accesses_token = widget_data[WgDataConst.project_ya_direct_access_token.value]
    else:
        ya_accesses: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
            p_id=project_id,
            s_id=LEXICON_SYSTEM_ID['YA_DIRECT']
        )
        widget_data[WgDataConst.project_ya_direct_access_token.value] = ya_accesses.access_token
        ya_accesses_token = ya_accesses.access_token

    data = [i.strip() for i in text.split(',')]
    data = list(set(data))
    deny, accept = [], []

    request = [check_ya_representative_clients_logins(oauth_token=ya_accesses_token,
                                                      login=login,
                                                      logger=logger) for login in data]
    responses = await asyncio.gather(*request)
    accesses = {}
    [accesses.update(response) for response in responses]
    for k, v in accesses.items():
        if v:
            accept.append(k)
        else:
            deny.append(k)

    if widget_data.get(WgDataConst.ya_direct_representative_accept_logins.value, False):
        accept_logins = widget_data[WgDataConst.ya_direct_representative_accept_logins.value]
        accept_logins.extend(accept)
        widget_data[WgDataConst.ya_direct_representative_accept_logins.value] = list(set(accept_logins))
    else:
        widget_data[WgDataConst.ya_direct_representative_accept_logins.value] = accept
    widget_data[WgDataConst.ya_direct_representative_deny_logins.value] = deny
    await dialog_manager.switch_to(
        state=YaDirectLoginsAddRepresentativeSG.PREVIEW,
        show_mode=ShowMode.EDIT
    )


async def btn_confirm(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    middleware_data = dialog_manager.middleware_data
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    i18n: TranslatorRunner = middleware_data[poolConst.i18n.value]
    project_id = int(start_data[StDataConst.project_id.value])

    project: Projects = await query.get_project_by_id(project_id=project_id)

    time = await bot_current_time()
    project_title: str = project.title
    start_date: str = str(project.created_at)
    company_name: str = project.company.company
    access_token = widget_data[WgDataConst.project_ya_direct_access_token.value]
    list_logins = ''
    requests = []
    for login in widget_data[WgDataConst.item.value]:
        ya_direct: YaDirectLogins = YaDirectLogins()
        ya_direct.project_id = project_id
        ya_direct.direct_login = login
        list_logins = list_logins + login + '\n'
        requests.append(query.add_ya_direct_logins(direct_login=ya_direct))
    await asyncio.gather(*requests)
    requests.clear()
    requests = [create_connection_direct(logger=logger,
                                         project_title=project_title,
                                         login=login,
                                         access_token=access_token,
                                         project_id=str(project_id),
                                         chat_id=LEXICON_TG_BOT['CHAT_ID_ERR_REPORT'],
                                         i18n=i18n,
                                         callback=callback,
                                         time=time) for login in widget_data[WgDataConst.item.value]]
    await asyncio.gather(*requests)

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
                           callback=callback)
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
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.item.value] = []


async def btn_cancel(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)
