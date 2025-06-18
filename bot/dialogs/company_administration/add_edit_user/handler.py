import logging
from typing import Any
from uuid import UUID
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from bot.database.models import Users, Projects
from bot.database import query
from argon2 import PasswordHasher
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            PoolingConstant as poolConst,
                                            DialogDataConstant as DgDataConst)
from bot.services.web_reports.utils import web_add_user, web_update_user, web_delete_manager, web_delete_viewer
from bot.state.dialog_state import CompanyAdminAddEditUserSG, CompanyAdminSG
from bot.support_models.models import SupportSessionUser

logger = logging.getLogger(__name__)


async def back_to_company_admin(dialog_manager: DialogManager,
                                company_id: int) -> None:

    list_projects: list[Projects] = await query.get_projects_by_company(company_id=company_id)
    list_users: list[Users] = await query.get_active_users_by_company_id(company_id=company_id)

    projects: list[tuple[str, int]] = [(project.title, project.id) for project in list_projects]
    users: list[tuple[str, str]] = [(user.full_name, user.login) for user in list_users]

    await dialog_manager.start(
        state=CompanyAdminSG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.RESET_STACK,
        data={
            StDataConst.list_projects.value: projects,
            StDataConst.list_users.value: users
        }
    )


async def btn_next_or_end(message: Message,
                          widget: ManagedTextInput,
                          dialog_manager: DialogManager,
                          text: str) -> None:
    dialog_data = dialog_manager.dialog_data
    await message.delete()
    if dialog_data.get(DgDataConst.finished_key.value, False):
        await dialog_manager.switch_to(CompanyAdminAddEditUserSG.PREVIEW,
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
        await dialog_manager.switch_to(CompanyAdminAddEditUserSG.INPUT_LOGIN,
                                       show_mode=ShowMode.EDIT)
    else:
        widget_data[WgDataConst.user_login.value] = login
        widget_data[WgDataConst.err_uniq_login.value] = False
        await dialog_manager.next(show_mode=ShowMode.EDIT)


async def error_login(message: Message,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      error: ValueError):
    await dialog_manager.switch_to(state=CompanyAdminAddEditUserSG.INPUT_LOGIN,
                                   show_mode=ShowMode.EDIT)
    await message.delete()


async def error_password(message: Message,
                         widget: ManagedTextInput,
                         dialog_manager: DialogManager,
                         error: ValueError):
    await dialog_manager.switch_to(state=CompanyAdminAddEditUserSG.INPUT_PASSWORD,
                                   show_mode=ShowMode.EDIT)
    await message.delete()


async def btn_back(callback: CallbackQuery,
                   widget: Any,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_delete(callback: CallbackQuery,
                     widget: Any,
                     dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data or {}
    middleware_data = dialog_manager.middleware_data

    tg_id = int(dialog_manager.event.from_user.id)
    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    support_user: SupportSessionUser = online_users.get(tg_id)
    company_id: int = int(support_user.get('company_id'))

    user_uuid = str(start_data[StDataConst.user_uuid.value])
    user_login = start_data[StDataConst.user_login.value]

    role_id = start_data.get(StDataConst.user_role_id.value, None)
    if role_id and role_id == 4:
        user_uuid = start_data[StDataConst.user_uuid.value]

        await query.delete_viewer_by_id(user_id=UUID(user_uuid))

        await web_delete_viewer(
            logger=logger,
            user_id=user_uuid,
            callback=callback
        )
    else:
        await query.deactivate_user_by_login(
            login=user_login,
            user_uuid=UUID(user_uuid)
        )
        await web_delete_manager(
            logger=logger,
            user_id=user_uuid,
            callback=callback
        )

    await back_to_company_admin(
        dialog_manager=dialog_manager,
        company_id=company_id
    )


async def btn_confirm(callback: CallbackQuery,
                      widget: Any,
                      dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data or {}
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    tg_id = int(dialog_manager.event.from_user.id)
    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    support_user: SupportSessionUser = online_users.get(tg_id)
    company_id: int = int(support_user.get('company_id'))

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
    user.role_id = int(start_data.get(StDataConst.user_role_id.value, 2))
    user.company_id = company_id

    edit_user = widget_data.get(WgDataConst.user_edit.value, False)

    if edit_user:
        await query.update_other_user_by_login(
            login=login,
            full_name=username,
            password=hashed_password
        )

        await web_update_user(
            logger=logger,
            login=login,
            callback=callback
        )

    else:
        await query.add_user(user=user)
        await web_add_user(
            logger=logger,
            user_login=login,
            callback=callback
        )

    await back_to_company_admin(dialog_manager=dialog_manager,
                                company_id=company_id)
