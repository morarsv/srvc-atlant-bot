import logging
from uuid import UUID
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from bot.state.dialog_state import AtlantAdministrationSG, ProjectsSG, ViewersSG, CompanyAdminSG
from bot.database.models import Users, Projects
from bot.database import query
from bot.lexicon.constants.constant import (PoolingConstant as poolConst,
                                            StartDataConstant as StDataConst)
from bot.support_models.models import SupportSessionUser


logger = logging.getLogger(__name__)


async def btn_to_atlant_administrator(callback: CallbackQuery,
                                      button: Button,
                                      dialog_manager: DialogManager) -> None:
    await dialog_manager.start(show_mode=ShowMode.EDIT,
                               state=AtlantAdministrationSG.PREVIEW,
                               mode=StartMode.NORMAL)


async def btn_to_administrator(callback: CallbackQuery,
                               button: Button,
                               dialog_manager: DialogManager) -> None:
    middleware_data = dialog_manager.middleware_data
    tg_id = int(callback.from_user.id)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    user_data: SupportSessionUser = online_users.get(tg_id)
    company_id: int = int(user_data.get('company_id'))

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


async def btn_to_project(callback: CallbackQuery,
                         button: Button,
                         dialog_manager: DialogManager) -> None:
    middleware_data = dialog_manager.middleware_data
    tg_id = int(callback.from_user.id)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    user: SupportSessionUser = online_users.get(tg_id)
    user_uuid: UUID = user['user_uuid']
    role_id: int = user['role_id']

    # list_projects: list[Projects] = await query.get_list_projects_by_user_uuid(user_uuid=user_uuid)

    # projects = [(p.title, p.id) for p in list_projects]

    await dialog_manager.start(
        show_mode=ShowMode.EDIT,
        state=ProjectsSG.PREVIEW,
        mode=StartMode.NORMAL,
        data={
            StDataConst.user_uuid.value: str(user_uuid),
            # StDataConst.list_projects.value: projects,
            StDataConst.user_role_id.value: role_id
        }
    )


async def btn_to_viewers(callback: CallbackQuery,
                         button: Button,
                         dialog_manager: DialogManager) -> None:
    middleware_data = dialog_manager.middleware_data
    tg_id = int(callback.from_user.id)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    manager: SupportSessionUser = online_users.get(tg_id)
    user_uuid: UUID = manager['user_uuid']
    company_id: int = manager['company_id']

    list_users: list[Users] = await query.get_viewers_by_manager_id(manager_id=user_uuid)
    users = [(user.full_name, user.login) for user in list_users]
    await dialog_manager.start(
        state=ViewersSG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.RESET_STACK,
        data={
            StDataConst.list_viewers.value: users,
            StDataConst.manager_uuid.value: str(user_uuid),
            StDataConst.company_id.value: company_id
        }
    )
