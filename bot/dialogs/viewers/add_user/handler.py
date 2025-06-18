import logging
from typing import Any
from uuid import UUID
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from bot.database.models import Users
from bot.database import query
from argon2 import PasswordHasher
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            DialogDataConstant as DgDataConst,
                                            PoolingConstant as poolConst)
from bot.services.web_reports.utils import web_add_user
from bot.state.dialog_state import ViewersAddUserSG, ViewersSG
from bot.support_models.models import SupportSessionUser


logger = logging.getLogger(__name__)


async def btn_next_or_end(message: Message,
                          widget: ManagedTextInput,
                          dialog_manager: DialogManager,
                          text: str) -> None:
    dialog_data = dialog_manager.dialog_data
    await message.delete()
    if dialog_data.get(DgDataConst.finished_key.value, False):
        await dialog_manager.switch_to(state=ViewersAddUserSG.PREVIEW,
                                       show_mode=ShowMode.EDIT)
    else:
        await dialog_manager.next(show_mode=ShowMode.EDIT)


async def btn_next_or_end_login(message: Message,
                                widget: ManagedTextInput,
                                dialog_manager: DialogManager,
                                text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    login = text.lower()

    user: Users = await query.get_user_by_login(login=login)
    await message.delete()
    if user is not None:
        widget_data[WgDataConst.err_uniq_login.value] = True
        await dialog_manager.switch_to(state=ViewersAddUserSG.INPUT_LOGIN,
                                       show_mode=ShowMode.EDIT)
    else:
        widget_data[WgDataConst.user_login.value] = login.lower()
        widget_data[WgDataConst.err_uniq_login.value] = False
        await dialog_manager.next(show_mode=ShowMode.EDIT)


async def error_login(message: Message,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      error: ValueError):
    await dialog_manager.switch_to(state=ViewersAddUserSG.INPUT_LOGIN,
                                   show_mode=ShowMode.EDIT)
    await message.delete()


async def error_password(message: Message,
                         widget: ManagedTextInput,
                         dialog_manager: DialogManager,
                         error: ValueError):
    await dialog_manager.switch_to(state=ViewersAddUserSG.INPUT_PASSWORD,
                                   show_mode=ShowMode.EDIT)
    await message.delete()


async def btn_back(callback: CallbackQuery,
                   widget: Any,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_confirm(callback: CallbackQuery,
                      widget: Any,
                      dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    username = widget_data[WgDataConst.username.value]
    login = widget_data[WgDataConst.user_login.value]
    company_id = start_data[StDataConst.company_id.value]
    password = widget_data[WgDataConst.user_password.value]
    manager_id = start_data[StDataConst.manager_uuid.value]

    ph: PasswordHasher = PasswordHasher()
    user = Users()
    hashed_password = ph.hash(password)

    user.full_name = username
    user.login = login
    user.password = hashed_password
    user.role_id = 4
    user.company_id = company_id

    await query.add_viewer(user=user, manager_id=UUID(manager_id))
    await web_add_user(
        logger=logger,
        user_login=login,
        callback=callback
    )

    tg_id = int(callback.from_user.id)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    manager: SupportSessionUser = online_users.get(tg_id)
    user_id: UUID = manager['user_uuid']
    company_id: int = manager['company_id']

    list_users: list[Users] = await query.get_viewers_by_manager_id(manager_id=user_id)
    users = [(user.full_name, user.login) for user in list_users]

    await dialog_manager.start(
        state=ViewersSG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.RESET_STACK,
        data={
            StDataConst.list_viewers.value: users,
            StDataConst.manager_uuid.value: str(user_id),
            StDataConst.company_id.value: company_id
        }
    )
