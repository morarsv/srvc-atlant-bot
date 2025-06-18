import logging

from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from bot.lexicon.constants.constant import StartDataConstant as StDataConst
from bot.state.dialog_state import AtlantAdministrationEditAddUserSG

logger = logging.getLogger(__name__)


async def btn_back(callback: CallbackQuery,
                   widget: Any,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_edit(callback: CallbackQuery,
                   widget: Any,
                   dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data

    await dialog_manager.start(
        state=AtlantAdministrationEditAddUserSG.PREVIEW,
        mode=StartMode.NORMAL,
        show_mode=ShowMode.EDIT,
        data={
            StDataConst.company_name.value: start_data[StDataConst.company_name.value],
            StDataConst.username.value: start_data[StDataConst.username.value],
            StDataConst.user_password.value: start_data[StDataConst.user_password.value],
            StDataConst.user_login.value: start_data[StDataConst.user_login.value],
            StDataConst.user_edit.value: True
        }
    )
