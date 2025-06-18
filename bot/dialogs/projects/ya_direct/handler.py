import logging
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from bot.services.yandex.utils import get_ya_advertiser_clients_logins, get_ya_agency_clients_logins
from bot.database.models import YandexAccesses
from bot.database import query
from bot.state.dialog_state import (YaDirectLoginsAddAgencySG, YaDirectLoginsAddAdvertiserSG,
                                    YaDirectLoginsAddRepresentativeSG)
from bot.lexicon.lexicon_ya import LEXICON_SYSTEM_ID
from bot.lexicon.constants.constant import StartDataConstant as StDataConst

logger = logging.getLogger(__name__)


async def btn_agency(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data

    project_id = int(start_data[StDataConst.project_id.value])

    ya_accesses: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_DIRECT']
    )
    ya_direct_logins = await get_ya_agency_clients_logins(
        oauth_token=ya_accesses.access_token,
        logger=logger
    )
    await dialog_manager.start(
        state=YaDirectLoginsAddAgencySG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.NORMAL,
        data={
            StDataConst.project_id.value: project_id,
            StDataConst.list_ya_direct_logins.value: ya_direct_logins
        })


async def btn_advertiser(callback: CallbackQuery,
                         button: Button,
                         dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data

    project_id = int(start_data[StDataConst.project_id.value])

    ya_accesses: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_DIRECT']
    )
    ya_direct_logins = await get_ya_advertiser_clients_logins(
        oauth_token=ya_accesses.access_token,
        logger=logger
    )
    await dialog_manager.start(
        state=YaDirectLoginsAddAdvertiserSG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.NORMAL,
        data={
            StDataConst.project_id.value: project_id,
            StDataConst.list_ya_direct_logins.value: ya_direct_logins
        })


async def btn_representative(callback: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data

    project_id = int(start_data[StDataConst.project_id.value])
    await dialog_manager.start(
        state=YaDirectLoginsAddRepresentativeSG.PREVIEW,
        mode=StartMode.NORMAL,
        data={
            StDataConst.project_id.value: project_id
        })


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)
