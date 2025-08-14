import asyncio
import logging
from typing import Any
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from bot.database.models import Users, Companies
from bot.database import query
from argon2 import PasswordHasher
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            PoolingConstant as poolConst,
                                            DialogDataConstant as DgDataConst)
from bot.services.web_reports.utils import web_add_user, web_add_company, web_update_user
from bot.services.msvc.generator import func
from bot.state.dialog_state import AtlantAdministrationEditAddUserSG, StartSG
from bot.support_models.models import SupportSessionUser

logger = logging.getLogger(__name__)


async def btn_next_or_end(message: Message,
                          widget: ManagedTextInput,
                          dialog_manager: DialogManager,
                          text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.mode_edit.value] = True
    dialog_data = dialog_manager.dialog_data
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    if dialog_data.get(DgDataConst.finished_key.value, False):
        await dialog_manager.switch_to(AtlantAdministrationEditAddUserSG.PREVIEW,
                                       show_mode=ShowMode.EDIT)
    else:
        await dialog_manager.next(show_mode=ShowMode.EDIT)


async def btn_next_or_end_login(message: Message,
                                widget: ManagedTextInput,
                                dialog_manager: DialogManager,
                                text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.mode_edit.value] = True
    login = text.lower()

    user: Users = await query.get_user_by_login(login=login)
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    if user is not None:
        widget_data[WgDataConst.err_uniq_login.value] = True
        await dialog_manager.switch_to(AtlantAdministrationEditAddUserSG.INPUT_LOGIN,
                                       show_mode=ShowMode.EDIT)
    else:
        widget_data[WgDataConst.user_login.value] = login
        widget_data[WgDataConst.err_uniq_login.value] = False
        await dialog_manager.next(show_mode=ShowMode.EDIT)


async def error_login(message: Message,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      error: ValueError):
    await dialog_manager.switch_to(state=AtlantAdministrationEditAddUserSG.INPUT_LOGIN,
                                   show_mode=ShowMode.EDIT)
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')


async def error_password(message: Message,
                         widget: ManagedTextInput,
                         dialog_manager: DialogManager,
                         error: ValueError):
    await dialog_manager.switch_to(state=AtlantAdministrationEditAddUserSG.INPUT_PASSWORD,
                                   show_mode=ShowMode.EDIT)
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')


async def btn_back(callback: CallbackQuery,
                   widget: Any,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_confirm(callback: CallbackQuery,
                      widget: Any,
                      dialog_manager: DialogManager) -> None:
    middleware_data = dialog_manager.middleware_data
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    start_password = start_data.get(StDataConst.user_password.value, None)

    username = widget_data[WgDataConst.username.value]
    login = widget_data[WgDataConst.user_login.value]
    password = widget_data.get(WgDataConst.user_password.value, None)

    ph: PasswordHasher = PasswordHasher()
    user = Users()
    hashed_password = ph.hash(password) if password else start_password

    user.full_name = username
    user.login = login
    user.password = hashed_password
    user.role_id = 1

    new_company = StDataConst.new_company.value
    old_company = StDataConst.old_company.value

    status = start_data.get(StDataConst.status.value, False)
    edit_user = widget_data.get(WgDataConst.user_edit.value, False)

    if edit_user:
        await query.update_atlant_user_by_login(login=login,
                                                full_name=username,
                                                password=hashed_password)
        await web_update_user(
            logger=logger,
            login=login,
            callback=callback
        )
        await dialog_manager.done(show_mode=ShowMode.EDIT)

    elif status == old_company:

        company_id = start_data[StDataConst.company_id.value]
        user.company_id = company_id
        await query.add_user(user=user)
        await web_add_user(
            logger=logger,
            user_login=login,
            callback=callback
        )
        await dialog_manager.done(show_mode=ShowMode.EDIT)

    elif status == new_company:

        company_name = start_data[StDataConst.company_name.value]
        company: Companies = Companies()
        company.company = company_name
        await query.add_company_and_user(company=company, user=user)
        company: Companies = await query.get_company_by_name(name=company_name)
        asyncio.create_task(func.generate_dbt_company(
            logger=logger,
            company_id=company.id,
            company_name=company_name
        ))
        await web_add_company(
            logger=logger,
            company_name=company_name,
            callback=callback
        )
        await web_add_user(
            logger=logger,
            user_login=login,
            callback=callback
        )

        tg_id = int(dialog_manager.event.from_user.id)
        online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

        support_user: SupportSessionUser = online_users.get(tg_id)
        username_pool: str = support_user['username']
        role_id_pool: int = support_user['role_id']

        await dialog_manager.start(
            show_mode=ShowMode.EDIT,
            mode=StartMode.RESET_STACK,
            state=StartSG.PREVIEW,
            data={
                StDataConst.username.value: username_pool,
                StDataConst.user_role_id.value: role_id_pool
            }
        )
